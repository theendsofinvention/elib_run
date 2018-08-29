# coding=utf-8
"""
Manages runners
"""
import pathlib
import shlex
import sys
import typing
import time

import sarge

from elib_run._exc import ExecutableNotFoundError
from elib_run._find_exe import find_executable
from elib_run._monitor_running_process import monitor_running_process
from elib_run._output import error
from elib_run._run_context import RunContext

_DEFAULT_PROCESS_TIMEOUT = float(60)


def check_error(context: RunContext) -> int:
    """
    Runs after a sub-process exits

    Checks the return code; if it is different than 0, then a few things happen:

        - if the process was muted ("mute" is True), the process output is printed anyway
        - if "failure_ok" is True (default), then a SystemExist exception is raised

    :param context: run context
    :type context: _RunContext
    :return: process return code
    :rtype: int
    """
    context.result_buffer += context.cmd_as_string
    if context.return_code != 0:
        context.result_buffer += f' -> command failed: {context.return_code}'

        if not context.failure_ok:
            error(context.result_buffer)
            error(repr(context))

            if context.mute:
                error(f'{context.exe_short_name} output:\n{context.process_output_as_str}')
            sys.exit(context.return_code)
    else:
        context.result_buffer += f' -> success: {context.return_code}'

    error(context.result_buffer)
    return context.return_code


def _sanitize_filters(
    filters: typing.Optional[typing.Union[typing.Iterable[str], str]]
) -> typing.Optional[typing.Iterable[str]]:
    if filters and isinstance(filters, str):
        return [filters]
    if filters:
        if not hasattr(filters, '__iter__'):
            raise TypeError(f'expected an iterable, got {type(filters)} instead')
        for index, item in enumerate(filters):
            if not isinstance(item, str):
                raise TypeError(f'item at position {index} is not a string: {type(item)}')
    return filters


def _parse_cmd(cmd: str, *paths: str) -> typing.Tuple[pathlib.Path, typing.List[str]]:
    try:
        exe_name, args = cmd.split(' ', maxsplit=1)
    except ValueError:
        # cmd has no argument
        exe_name, args = cmd, ''
    exe_path: pathlib.Path = find_executable(exe_name, *paths)

    if not exe_path:
        raise ExecutableNotFoundError(exe_name)

    args_list = shlex.split(args)

    return exe_path, args_list


def run(cmd: str,
        *paths: str,
        cwd: str = '.',
        mute: bool = False,
        filters: typing.Optional[typing.Union[typing.Iterable[str], str]] = None,
        failure_ok: bool = False,
        timeout: float = _DEFAULT_PROCESS_TIMEOUT,
        ) -> typing.Tuple[str, int]:
    """
    Executes a command and returns the result

    Args:
        cmd: command to execute
        paths: paths to search executable in
        cwd: working directory (defaults to ".")
        mute: if true, output will not be printed
        filters: gives a list of partial strings to filter out from the output (stdout or stderr)
        failure_ok: if False (default), a return code different than 0 will exit the application
        timeout: sub-process timeout

    Returns: command output
    """

    filters = _sanitize_filters(filters)

    exe_path, args_list = _parse_cmd(cmd, *paths)

    context = RunContext(
        exe_path=exe_path,
        capture=sarge.Capture(),
        failure_ok=failure_ok,
        mute=mute,
        args_list=args_list,
        paths=paths,
        cwd=cwd,
        timeout=timeout,
        filters=filters,
    )

    if mute:
        context.result_buffer += f'RUNNING: {context.cmd_as_string}'
    else:
        error(f'RUNNING: {context.cmd_as_string}')

    context.start_process()

    monitor_running_process(context)

    check_error(context)

    return context.process_output_as_str, context.return_code


if __name__ == '__main__':

    import os

    # t = os.system('chcp > text.text')
    # print(t)
    # exit(0)

    from click import secho
    from elib_run._output import register_hooks

    def _error(msg):
        secho(msg, err=True, fg='red')
        # print('error', msg)

    def _info(msg):
        secho(msg, fg='green')
        # print('info', msg)

    def _process_output(msg):
        secho(msg, fg='cyan')

    # register_hook_error(_error)
    # register_hook_info(_info)
    # register_hook_process_output(_process_output)
    register_hooks(_info, _error, _process_output)

    # out, code = run('chcp', cwd=r'F:\DEV\elib_run', mute=True)
    out, code = run('safety check', cwd=r'F:\DEV\elib_run')
    # print(code, out)
