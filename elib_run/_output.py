# coding=utf-8
import typing
from collections import defaultdict

_HOOKS: typing.DefaultDict[str, typing.List[callable]] = defaultdict(lambda: list())


def _add_hook(func_name: str, hook: callable):
    _HOOKS.setdefault(func_name, []).append(hook)


def _run_hooks(func_name: str, msg: str):
    for hook in _HOOKS[func_name]:
        hook(msg)


def cmd_start(msg: str):
    _run_hooks('cmd_start', msg)


def cmd_end(msg: str):
    _run_hooks('cmd_end', msg)


def info(msg: str):
    _run_hooks('info', msg)


def error(msg: str):
    _run_hooks('error', msg)


def std_out(msg: str):
    _run_hooks('std_out', msg)


def std_err(msg: str):
    _run_hooks('std_err', msg)


def register_hook_cmd_start(hook: callable):
    _add_hook('cmd_start', hook)


def register_hook_cmd_end(hook: callable):
    _add_hook('cmd_end', hook)


def register_hook_error(hook: callable):
    _add_hook('error', hook)


def register_hook_info(hook: callable):
    _add_hook('info', hook)


def register_hook_std_out(hook: callable):
    _add_hook('std_out', hook)


def register_hook_std_err(hook: callable):
    _add_hook('std_err', hook)
