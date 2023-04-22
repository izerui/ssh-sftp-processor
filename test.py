import unittest

from remote import Host


class TestTable(unittest.TestCase):

    def setUp(self):
        self.hosts = []

    def tearDown(self) -> None:
        for host in self.hosts:
            host.close()

    def _host(self, host_key):
        host = Host(host_key)
        host.connect()
        self.hosts.append(host)
        return host

    def test_join_k8s(self):
        self._host('master201').exe_commands(['kubeadm token create --print-join-command'],
                                         lambda t: self._host('node204').exe_commands([t['line']]))

    def test_init_k8s_node(self):
        my_host = self._host('node212')
        commands = [
            'systemctl stop firewalld.service',
            'systemctl disable firewalld.service',
            'yum -y install ntpdate',
            'ntpdate -u pool.ntp.org',
            'date',
            'echo "192.168.1.163  harbor.yj2025.com" >> /etc/hosts',
            'echo "192.168.1.201  apiserver.local" >> /etc/hosts',
            'echo "127.0.0.1   $(hostname)" >> /etc/hosts',
            'cat /etc/hosts',
            'export REGISTRY_MIRROR=https://ustc-edu-cn.mirror.aliyuncs.com',
            'curl -sSL https://file.yj2025.com/install_kubelet.sh | sh -s 1.20.12',
        ]
        my_host.exe_commands(commands)