import os
import stat
from configparser import ConfigParser
from typing import Tuple

import paramiko

config = ConfigParser()
config.read('config.ini')


class Host:

    def __init__(self, host_key):
        self.host_key = host_key
        self.ssh_host = config.get(host_key, 'ssh_host')
        self.ssh_port = int(config.get(host_key, 'ssh_port'))
        self.ssh_user = config.get(host_key, 'ssh_user')
        self.ssh_pass = config.get(host_key, 'ssh_pass')
        # ssh 远程ssh的连接
        self.client = paramiko.SSHClient()

    def connect(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(hostname=self.ssh_host, port=self.ssh_port, username=self.ssh_user, password=self.ssh_pass)
        pass

    def close(self):
        self.client.close()

    def with_sftp(self, callback):
        with self.client.open_sftp() as sftp:
            callback(sftp)

    def get_file(self, remote_path, local_path):
        self._get_file_list(remote_path, local_path, self.client.open_sftp())

    def _get_file_list(self, remote_path, local_path, sftp):
        attr = sftp.stat(remote_path)
        if stat.S_ISDIR(attr.st_mode):
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            for f in sftp.listdir(remote_path):
                self._get_file_list(os.path.join(remote_path, f), os.path.join(local_path, f), sftp)
        else:
            sftp.get(remote_path, local_path)
            print(remote_path, ' - successed')

    def put_file(self, local_file, remote_file):
        # TODO
        pass

    def exe_commands(self, commands, callback=None):
        for command in commands:
            print(f'[{self.ssh_user}@{self.ssh_host} ~]#' + command)
            (stdin, stdout, stderr) = self.client.exec_command(command, get_pty=True)

            while not stdout.channel.exit_status_ready():
                line = stdout.readline()
                if line:
                    print(f'[{self.ssh_user}@{self.ssh_host} ~]#' + line, end='')
                    if callback:
                        callback({'command': command, 'line': line})
                if stdout.channel.exit_status_ready():
                    break
