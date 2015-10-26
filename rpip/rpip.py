from pssh import ParallelSSHClient


class RemotePip(ParallelSSHClient):

    def __init__(self, hosts, pip_path='/usr/bin/pip', *args, **kwargs):
        self.pip_path = pip_path
        super(RemotePip, self).__init__(hosts, *args, **kwargs)

    def install(self, pkgs, upgrade=False):
        cmd = self.generate_install_cmd(pkgs=pkgs, upgrade=upgrade)
        output = self.run_command(cmd)
        return Output.from_pssh_dict(output)

    def generate_install_cmd(self, pkgs, upgrade=False):
        cmd = '{} install '.format(self.pip_path)

        if isinstance(pkgs, str):
            pkgs = [pkgs]
        cmd += ' '.join(pkgs)

        if upgrade:
            cmd += ' -U'
        return cmd


class Output(dict):

    @classmethod
    def from_pssh_dict(cls, output):
        self = cls()
        for host, values in output.iteritems():
            self[host] = {}
            self[host]['exit_code'] = values['exit_code']
            stdout = ''
            for line in values['stdout']:
                stdout += line + '\n'
            self[host]['stdout'] = stdout.strip()

            stderr = ''
            for line in values['stderr']:
                stderr += line + '\n'
            self[host]['stderr'] = stderr.strip()
        return self

    def __init__(self):
        pass

if __name__ == '__main__':
    hosts = ['54.210.23.215', '52.91.174.90', '54.172.180.200', '52.91.58.145']
    import paramiko
    key = paramiko.RSAKey.from_private_key_file('/Users/drodriguez/.ssh/drodriguez.pem')

    rpip = RemotePip(hosts, user='ubuntu', pkey=key, pip_path='/opt/anaconda/bin/pip')
    print rpip.generate_install_cmd(pkgs='requests')
    print rpip.install(pkgs='requests')
