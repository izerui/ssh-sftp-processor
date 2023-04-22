import concurrent
import os
import stat
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
from multiprocessing.pool import ThreadPool

import paramiko
from paramiko.sftp_client import SFTPClient

from utils import log_time

config = ConfigParser()
config.read('config.ini')


class Host:

    def __init__(self, host_key):
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

    @log_time
    def get_file(self, remote_path, local_path):
        # self._get_file_list(remote_path, local_path, self.client.open_sftp())
        with concurrent.futures.ThreadPoolExecutor(max_workers=6, thread_name_prefix='sftp_') as executor:
            self._get_file_list(remote_path, local_path, executor)
            executor.shutdown()

    def _get_file_list(self, remote_path, local_path, executor):
        sftp = self.client.open_sftp()
        attr = sftp.stat(remote_path)
        if stat.S_ISDIR(attr.st_mode):
            if not os.path.exists(local_path):
                os.makedirs(local_path)
            for f in sftp.listdir(remote_path):
                self._get_file_list(os.path.join(remote_path, f), os.path.join(local_path, f), executor)
        else:
            # self._down_file(remote_path, local_path, sftp)
            executor.submit(self._down_file, remote_path, local_path)
        sftp.close()

    def _down_file(self, remote_path, local_path):
        sftp = self.client.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
        print(remote_path, ' - successed')

    def put_file(self, local_file, remote_file):
        with self.client.open_sftp() as sftp:
            sftp.put(local_file, remote_file)
