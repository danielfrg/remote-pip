from __future__ import absolute_import, unicode_literals

# Fix error message: Exception KeyError ... in <module 'threading' ...
import sys
if 'threading' in sys.modules:
    del sys.modules['threading']
import gevent
import gevent.socket
import gevent.monkey
gevent.monkey.patch_all()
# END

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

    def uninstall(self, pkgs):
        cmd = self.generate_uninstall_cmd(pkgs=pkgs)
        output = self.run_command(cmd)
        self.output = Output.from_pssh_dict(output)
        return self.output

    def generate_uninstall_cmd(self, pkgs):
        cmd = '{} uninstall '.format(self.pip_path)

        if isinstance(pkgs, unicode):
            pkgs = [pkgs]
        cmd += ' '.join(pkgs)

        cmd += ' -y'
        return cmd

    def freeze(self):
        cmd = self.generate_freeze_cmd()
        output = self.run_command(cmd)
        self.output = Output.from_pssh_dict(output)
        return self.output

    def generate_freeze_cmd(self):
        cmd = '{} freeze'.format(self.pip_path)
        return cmd

    def list(self):
        cmd = self.generate_list_cmd()
        output = self.run_command(cmd)
        self.output = Output.from_pssh_dict(output)
        return self.output

    def generate_list_cmd(self):
        cmd = '{} list'.format(self.pip_path)
        return cmd

    def show(self, pkgs):
        cmd = self.generate_show_cmd(pkgs=pkgs)
        output = self.run_command(cmd)
        self.output = Output.from_pssh_dict(output)
        return self.output

    def generate_show_cmd(self, pkgs):
        cmd = '{} show '.format(self.pip_path)

        if isinstance(pkgs, unicode):
            pkgs = [pkgs]
        cmd += ' '.join(pkgs)
        return cmd
