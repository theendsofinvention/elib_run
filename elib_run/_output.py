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


def _run_hooks(func_name: str, msg: str):
    for hook in _HOOKS[func_name]:
        hook(msg)


def cmd_start(msg: str):
    """
    Happens at the start of a command

    :param msg: message to pass along
    :type msg: str
    """
    _run_hooks('cmd_start', msg)


def cmd_end(msg: str):
    """
    Happens at the end of a command

    :param msg: message to pass along
    :type msg: str
    """
    _run_hooks('cmd_end', msg)


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

    :param msg: message to pass along
    :type msg: str
    """
    _run_hooks('error', msg)


def std_out(msg: str):
    """
    Outputs a message to stdout

    :param msg: message to pass along
    :type msg: str
    """
    _run_hooks('std_out', msg)


def std_err(msg: str):
    """
    Outputs a message to stderr

    :param msg: message to pass along
    :type msg: str
    """
    _run_hooks('std_err', msg)


def register_hook_cmd_start(hook: typing.Callable):
    """
    Register a hook for cmd_start

    :param hook: function to call
    :type hook: callable
    """
    _add_hook('cmd_start', hook)


def register_hook_cmd_end(hook: typing.Callable):
    """
    Register a hook for cmd_end

    :param hook: function to call
    :type hook: callable
    """
    _add_hook('cmd_end', hook)


def register_hook_error(hook: typing.Callable):
    """
    Register a hook for error

    :param hook: function to call
    :type hook: callable
    """
    _add_hook('error', hook)


def register_hook_info(hook: typing.Callable):
    """
    Register a hook for info

    :param hook: function to call
    :type hook: callable
    """
    _add_hook('info', hook)


def register_hook_std_out(hook: typing.Callable):
    """
    Register a hook for std_out

    :param hook: function to call
    :type hook: callable
    """
    _add_hook('std_out', hook)


def register_hook_std_err(hook: typing.Callable):
    """
    Register a hook for std_err

    :param hook: function to call
    :type hook: callable
    """
    _add_hook('std_err', hook)
