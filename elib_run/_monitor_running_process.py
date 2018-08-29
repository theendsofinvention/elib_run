# coding=utf-8


import sys
import time

from elib_run._capture_output import capture_output_from_running_process
from elib_run._output import error
from elib_run._run_context import RunContext
from elib_run._exc import ProcessTimeoutError


def monitor_running_process(context: RunContext):
    """
    Runs an infinite loop that waits for the process to either exit on its or time out

    Captures all output from the running process

    :param context: run context
    :type context: RunContext
    """
    while True:
        capture_output_from_running_process(context)

        if context.process_finished:
            context.return_code = context.command.returncode
            break

        if context.process_timed_out:
            raise ProcessTimeoutError(
                exe_name=context.exe_short_name,
                timeout=context.timeout,
            )
