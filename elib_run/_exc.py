# coding=utf-8
import typing


class ELIBRunError(Exception):
    """Base exception for the elib_run package"""


class ExecutableNotFoundError(ELIBRunError):
    """Raised when an executable is not found"""

    def __init__(self, exe_name: str, msg: typing.Optional[str] = None):
        self.exe_name = exe_name
        super(ExecutableNotFoundError, self).__init__(f'executable not found: {exe_name} ({msg})')
