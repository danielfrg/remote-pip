from __future__ import absolute_import, unicode_literals

import itertools


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

    def groupby(self):
        groups = []
        for key, grouped in itertools.groupby(self, key=lambda node: self[node]):
            groups.append((list(grouped), key))
        return groups

    def groupby_exit_code(self):
        groups = []
        for key, grouped in itertools.groupby(self, key=lambda node: self[node]['exit_code']):
            groups.append((list(grouped), key))
        return groups
