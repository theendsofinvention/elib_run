# coding=utf-8
"""
Top-level package for elib_run.
"""

from pkg_resources import DistributionNotFound, get_distribution

from ._exc import ELIBRunError, ExecutableNotFoundError
from ._find_exe import find_executable
from ._output import register_hooks
from ._run import run

try:
    __version__ = get_distribution('elib_run').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'

__author__ = """etcher"""
__email__ = 'etcher@daribouca.net'

__all__ = ['run', 'register_hooks', 'find_executable',
           'ELIBRunError', 'ExecutableNotFoundError']
