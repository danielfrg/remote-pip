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
        items = sorted(self.items(), key=lambda x: x[1], reverse=True)
        for key, grouped in itertools.groupby(items, key=lambda x: x[1]):
            groups.append((list(item[0] for item in grouped), key))
        groups = sorted(groups, key=lambda x: len(x[0]), reverse=True)
        return groups
