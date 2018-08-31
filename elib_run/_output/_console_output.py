# coding=utf-8
"""
Dummy config for printing out output of sub-process to the console using click
"""

import click

from elib_run._output._output import register_hooks


def _error(msg):
    click.secho(msg, err=True, fg='red')


def _info(msg):
    click.secho(msg, fg='magenta')


def _success(msg):
    click.secho(msg, fg='green')


def _process_output(msg):
    click.secho(msg, fg='cyan')


def register_console_hooks() -> None:
    """
    Registers simple console hooks
    """
    register_hooks(
        info_hooks=_info,
        error_hooks=_error,
        success_hooks=_success,
        process_output_hooks=_process_output,
    )
