# coding=utf-8
from collections import defaultdict

import pytest
from mockito import mock, verify

# noinspection PyProtectedMember
from elib_run import _output


@pytest.mark.parametrize(
    'cmd_name',
    ('info', 'error', 'std_out', 'std_err', 'cmd_start', 'cmd_end')
)
def test_output(cmd_name):
    msg = 'some message'
    _output._HOOKS = defaultdict(lambda: list())
    register_func = getattr(_output, f'register_hook_{cmd_name}')
    hook = mock()
    register_func(hook.call)
    output_func = getattr(_output, cmd_name)
    output_func(msg)
    verify(hook).call(msg)
