# coding=utf-8
"""
Passes output of the elib_run package to hooked functions
"""
import typing
from collections import defaultdict

# pylint: disable=unnecessary-lambda
_HOOKS: typing.DefaultDict[str, typing.List[typing.Callable]] = defaultdict(lambda: list())


def _add_hook(func_name: str, hook: typing.Callable):
    _HOOKS.setdefault(func_name, []).append(hook)


def _run_hooks(func_name: str, msg: str, force: bool = False):
    if force and not _HOOKS[func_name]:
        print(msg)
    else:
        for hook in _HOOKS[func_name]:
            hook(msg)


def info(msg: str):
    """
    Regular information message

    :param msg: message to pass along
    :type msg: str
    """
    _run_hooks('info', msg)


def error(msg: str):
    """
    Error message

    If no hook is defined for error messages, then they will be printed anyway

    :param msg: message to pass along
    :type msg: str
    """
    _run_hooks('error', msg, force=True)


def print_process_output(msg: str):
    """
    Process output

    If no hook is defined for error messages, then they will be printed anyway

    :param msg: message to pass along
    :type msg: str
    """
    _run_hooks('process_output', msg, force=True)


def _single_hook_to_list(hook: typing.Optional[typing.Union[typing.Callable, typing.List[typing.Callable]]]
                         ) -> typing.List[typing.Callable]:
    if isinstance(hook, list):
        return hook

    return [hook]


_HOOKS_ARG_TYPE = typing.Optional[typing.Union[typing.Callable, typing.List[typing.Callable]]]


def register_hooks(info_hooks: _HOOKS_ARG_TYPE = None,
                   error_hooks: _HOOKS_ARG_TYPE = None,
                   process_output_hooks: _HOOKS_ARG_TYPE = None,
                   ) -> None:
    """
    Registers hooks for the elib_run package output

    :param info_hooks: function to call for regular output
    :type info_hooks: typing.Optional[typing.Union[typing.Callable, typing.List[typing.Callable]]]
    :param error_hooks: function to call for important output
    :type error_hooks: typing.Optional[typing.Union[typing.Callable, typing.List[typing.Callable]]]
    :param process_output_hooks: function to call for process output (stderr + stdout)
    :type process_output_hooks: typing.Optional[typing.Union[typing.Callable, typing.List[typing.Callable]]]
    """
    for hook_name in ('info', 'error', 'process_output'):
        local_ = locals()[hook_name + '_hooks']
        if local_:
            hook_list: list = _single_hook_to_list(local_)
            for hook_callable in hook_list:
                _add_hook(hook_name, hook_callable)
