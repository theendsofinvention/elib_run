# coding=utf-8

import pathlib
import typing
import time

import dataclasses
import sarge


@dataclasses.dataclass
class RunContext:
    exe_path: pathlib.Path
    capture: sarge.Capture
    failure_ok: bool
    mute: bool
    args_list: typing.List[str]
    paths: typing.Optional[typing.Iterable[str]]
    cwd: str
    timeout: float
    process_output_chunks: typing.List[str] = dataclasses.field(default_factory=list, repr=False)
    result_buffer: str = dataclasses.field(default='', repr=False)
    filters: typing.Optional[typing.Iterable[str]] = None
    return_code: int = -1
    start_time: int = 0
    console_encoding: str = 'utf8'

    def start_process(self) -> None:
        """
        Starts the process defined by this context
        """
        self.start_time = time.monotonic()
        self.command.run(async_=True)

    @property
    def process_timed_out(self) -> bool:
        """
        :return: True if the process timed out
        :rtype: bool
        """
        return time.monotonic() - self.start_time > self.timeout

    @property
    def process_finished(self) -> bool:
        """
        :return: True if a given process is done running
        :rtype: bool
        """
        return self.command.poll() is not None

    @property
    def process_output_as_str(self) -> str:
        """
        Returns process output so far

        :return: process output
        :rtype: str
        """
        return '\n'.join(self.process_output_chunks)

    @property
    def exe_path_as_str(self) -> str:
        """
        Returns executable path as a string

        :return: executable path
        :rtype: str
        """
        return str(self.exe_path.absolute())

    @property
    def absolute_cwd_as_str(self) -> str:
        """
        :return: absolute working dir
        :rtype: str
        """
        return str(pathlib.Path(self.cwd).absolute())

    @property
    def cmd_as_string(self) -> str:
        """
        Returns a concatenation of executable & args as a string

        :return: command
        :rtype: str
        """
        cmd = ' '.join((self.exe_path_as_str, ' '.join(self.args_list)))
        return f'"{cmd}" in "{self.absolute_cwd_as_str}"'

    @property
    def exe_short_name(self) -> str:
        """
        Returns executable short name

        :return: executable short name
        :rtype: str
        """
        return self.exe_path.name

    @property
    def command(self) -> sarge.Command:
        """
        Returns sarge.Command instance, creating it if necessary

        :return: sarge.Command object
        :rtype: sarge.Command
        """
        if not hasattr(self, '_command'):
            # print('self.exe_path_as_str', self.exe_path_as_str, type(self.exe_path_as_str))
            # print('self.args_list', self.args_list, type(self.args_list))
            command = sarge.Command(
                [self.exe_path_as_str] + self.args_list,
                stdout=self.capture,
                stderr=self.capture,
                shell=False,
                cwd=self.cwd,
                # executable=self.exe_path_as_str,
            )
            setattr(self, '_command', command)
        return getattr(self, '_command')
