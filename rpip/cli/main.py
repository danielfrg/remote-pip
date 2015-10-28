from __future__ import absolute_import, unicode_literals

from functools import update_wrapper

import click
import paramiko

import rpip
from rpip import RemotePip

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def default_options(func):
    @click.option('--hosts', '-h', 'hosts', required=True, help='Comma separated hosts')
    @click.option('--user', '-u', 'user', required=False, help='Username to ssh')
    @click.option('--pkey', '-k', 'pkey', required=False, help='Path to the private key', type=click.Path(exists=True, resolve_path=True))
    @click.option('--pip-path', '-p', 'pip_path', required=False, help='Path to the pip binary in the remote nodes', default='/usr/bin/pip')
    @click.pass_context
    def new_func(ctx, hosts, user, pkey, pip_path, *args, **kwargs):
        hosts = hosts.split(',')

        if pkey:
            pkey = paramiko.RSAKey.from_private_key_file(pkey)

        ctx.obj['client'] = RemotePip(hosts=hosts, user=user, pkey=pkey, pip_path=pip_path)
        return ctx.invoke(func, *args, **kwargs)

    return update_wrapper(new_func, func)


def start():
    cli(obj={})


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(prog_name='Remote pip', version=rpip.__version__)
@click.pass_context
def cli(ctx):
    ctx.obj = {}


@cli.command(short_help='Install packages')
@click.argument('packages', nargs=-1)
@default_options
@click.pass_context
def install(ctx, packages):
    client = ctx.obj['client']
    output = client.install(pkgs=packages)

    groups = output.groupby()
    for group in groups:
        nodes = group[0]
        output = group[1]
        click.echo('Response from (x{}) nodes:'.format(len(nodes)))
        if output['stdout'] != '':
            err = output['exit_code'] != 0
            click.echo(output['stdout'], err=err)
        if output['stderr'] != '':
            click.echo(output['stderr'], err=True)


@cli.command(short_help='Uninstall packages')
@click.argument('packages', nargs=-1)
@default_options
@click.pass_context
def uninstall(ctx, packages):
    client = ctx.obj['client']
    output = client.uninstall(pkgs=packages)

    groups = output.groupby()
    for group in groups:
        nodes = group[0]
        output = group[1]
        click.echo('Response from (x{}) nodes:'.format(len(nodes)))
        if output['stdout'] != '':
            err = output['exit_code'] != 0
            click.echo(output['stdout'], err=err)
        if output['stderr'] != '':
            click.echo(output['stderr'], err=True)


@cli.command(short_help='Output installed packages in requirements format')
@default_options
@click.pass_context
def freeze(ctx):
    client = ctx.obj['client']
    output = client.freeze()

    groups = output.groupby()
    for group in groups:
        nodes = group[0]
        output = group[1]
        click.echo('Response from (x{}) nodes:'.format(len(nodes)))
        if output['stdout'] != '':
            err = output['exit_code'] != 0
            click.echo(output['stdout'], err=err)
        if output['stderr'] != '':
            click.echo(output['stderr'], err=True)


@cli.command(short_help='List installed packages')
@default_options
@click.pass_context
def list(ctx):
    client = ctx.obj['client']
    output = client.list()

    groups = output.groupby()
    for group in groups:
        nodes = group[0]
        output = group[1]
        click.echo('Response from (x{}) nodes:'.format(len(nodes)))
        if output['stdout'] != '':
            err = output['exit_code'] != 0
            click.echo(output['stdout'], err=err)
        if output['stderr'] != '':
            click.echo(output['stderr'], err=True)


@cli.command(short_help='Show information about installed packages')
@click.argument('packages', nargs=-1)
@default_options
@click.pass_context
def show(ctx, packages):
    client = ctx.obj['client']
    output = client.show(pkgs=packages)

    groups = output.groupby()
    for group in groups:
        nodes = group[0]
        output = group[1]
        click.echo('Response from (x{}) nodes:'.format(len(nodes)))
        if output['stdout'] != '':
            err = output['exit_code'] != 0
            click.echo(output['stdout'], err=err)
        if output['stderr'] != '':
            click.echo(output['stderr'], err=True)

if __name__ == '__main__':
    start()
