# coding=utf-8

import click
import pytest
from mockito import verify, when

# noinspection PyProtectedMember
from elib_run._output import _console_output


@pytest.fixture(autouse=True)
def _stub_click_secho():
    when(click).secho(...)
    yield


@pytest.mark.parametrize(
    'func,kwargs',
    (
        (_console_output._error, dict(err=True, fg='red')),
        (_console_output._info, dict(fg='magenta')),
        (_console_output._success, dict(fg='green')),
        (_console_output._process_output, dict(fg='cyan')),
    )
)
def test_raw(func, kwargs):
    func('test_msg')
    verify(click).secho('test_msg', **kwargs)


def test_hooks():
    when(_console_output).register_hooks(...)
    _console_output.register_console_hooks()
    verify(_console_output).register_hooks(
        info_hooks=_console_output._info,
        error_hooks=_console_output._error,
        success_hooks=_console_output._success,
        process_output_hooks=_console_output._process_output,
    )
