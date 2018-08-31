# coding=utf-8

from collections import defaultdict

import pytest
from mockito import mock, verifyNoMoreInteractions, verifyNoUnwantedInteractions, verifyStubbedInvocationsAreUsed, when

# noinspection PyProtectedMember
from elib_run._output import _output


@pytest.fixture(autouse=True)
def _reset_hooks():
    _output._HOOKS = defaultdict(lambda: list())


@pytest.mark.filterwarnings
@pytest.mark.parametrize(
    'func',
    (
        _output.info,
        _output.error,
        _output.process_output,
        _output.success,
    )
)
def test_empty_hooks(func, capsys):
    with pytest.warns(UserWarning):
        func('test message')
    captured = capsys.readouterr()
    assert '' == captured.out
    assert '' == captured.err


@pytest.mark.parametrize(
    'func_name',
    ('error', 'info', 'success', 'process_output')
)
def test_single_hook_run(func_name):
    mock_ = mock()
    when(mock_).called('test message')
    _output._HOOKS[func_name] = [mock_.called]
    getattr(_output, func_name)('test message')
    verifyNoMoreInteractions()
    verifyNoUnwantedInteractions()
    verifyStubbedInvocationsAreUsed()


def test_single_hook_to_list():
    assert [print] == _output._single_hook_to_list(print)
    assert [print, print] == _output._single_hook_to_list([print, print])


@pytest.mark.parametrize(
    'value',
    (10, 10.05, True, None, 'test', ['list'], {'key': 'value'})
)
def test_single_hook_to_list_wrong_type(value):
    with pytest.raises(TypeError):
        _output._single_hook_to_list(value)
    with pytest.raises(TypeError):
        _output._single_hook_to_list([value, value])


def test_add_hook():
    assert not _output._HOOKS
    _output._add_hook('test_func', print)
    assert _output._HOOKS['test_func'] == [print]


def test_register_hooks():
    info_hook = mock()
    error_hook = mock()
    success_hook = mock()
    process_hook = mock()
    when(_output)._add_hook('info', info_hook)
    when(_output)._add_hook('error', error_hook)
    when(_output)._add_hook('success', success_hook)
    when(_output)._add_hook('process_output', process_hook)
    _output.register_hooks(
        info_hooks=info_hook,
        error_hooks=error_hook,
        success_hooks=success_hook,
        process_output_hooks=process_hook
    )
    verifyStubbedInvocationsAreUsed()
    verifyNoMoreInteractions()
    verifyNoUnwantedInteractions()


def test_register_hooks_partial():
    info_hook = mock()
    when(_output)._add_hook('info', info_hook)
    _output.register_hooks(
        info_hooks=info_hook,
    )
    verifyStubbedInvocationsAreUsed()
    verifyNoMoreInteractions()
    verifyNoUnwantedInteractions()
