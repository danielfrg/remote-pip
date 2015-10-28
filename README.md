# Remote pip

Install python packages using pip in remote hosts.

## Installation

`pip install rpip`

## Usage

`rpip` is a basic CLI that has the basic `pip` commands: `install`, `uninstall`,
`freeze`, `list` and `show`
and follows the same API as `pip` with some extra options:

- Hosts (`--hosts/-h`) is the only required option. It can be IPs for example
but can also be defined in you ssh config file (`~/.ssh/config`)
for easier reference without passing the other options
- User (`--user/-u`) is the username to ssh into the hosts
- Private key (`--pkey/-k`) to ssh into the hosts
- Pip Path (`--pip-path/-p`), useful to manage packages in multiple virtual
environments. Default: `/usr/bin/pip`

Examples:

```bash
$ rpip install requests -h myhost1
$ rpip install requests boto -h myhost1,myhost2,myhost3

# Using IPs (no ssh config file)
$ rpip uninstall requests -h 127.0.0.1 -u ubuntu -k ~/.ssh/mykey.pem
$ rpip uninstall requests boto -h 127.0.0.1,127.0.0.2 -u ubuntu -k ~/.ssh/mykey.pem

# In an virutalenv
$ rpip install requests boto -h myhost1 -p /opt/anaconda/bin/pip
```
