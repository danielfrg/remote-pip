from __future__ import absolute_import, unicode_literals

from functools import update_wrapper

import click


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def default_options(func):
    @click.option('--hosts',
                  '-h',
                  'hosts',
                  required=True,
                  help='Comma separated hosts',)
    @click.pass_context
    def new_func(ctx, hosts, *args, **kwargs):
        ctx.obj['client'] = 'shit'
        return ctx.invoke(func, *args, **kwargs)

    return update_wrapper(new_func, func)


def start():
    cli(obj={})


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    ctx.obj = {}


@cli.command(short_help='Install pip packages in remote nodes')
@default_options
@click.pass_context
def install(ctx):
    client = ctx.obj['client']

if __name__ == '__main__':
    start()
