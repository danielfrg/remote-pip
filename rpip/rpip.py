from __future__ import absolute_import, unicode_literals

from pssh import ParallelSSHClient

from .output import Output


class RemotePip(ParallelSSHClient):

    def __init__(self, hosts, pip_path='/usr/bin/pip', *args, **kwargs):
        self.pip_path = pip_path
        self.output = None
        super(RemotePip, self).__init__(hosts, *args, **kwargs)

    def install(self, pkgs, upgrade=False):
        cmd = self.generate_install_cmd(pkgs=pkgs, upgrade=upgrade)
        output = self.run_command(cmd)
        self.output = Output.from_pssh_dict(output)
        return self.output

    def generate_install_cmd(self, pkgs, upgrade=False):
        cmd = '{} install '.format(self.pip_path)

        if isinstance(pkgs, unicode):
            pkgs = [pkgs]
        cmd += ' '.join(pkgs)

        if upgrade:
            cmd += ' -U'
        return cmd


if __name__ == '__main__':
    hosts = ['54.210.23.215', '52.91.174.90', '54.172.180.200', '52.91.58.145']
    import paramiko
    key = paramiko.RSAKey.from_private_key_file('/Users/drodriguez/.ssh/drodriguez.pem')

    rpip = RemotePip(hosts, user='ubuntu', pkey=key, pip_path='/opt/anaconda/bin/pip')
    print rpip.generate_install_cmd(pkgs='requests')
    print rpip.install(pkgs='requests')
