# coding=utf-8

import string

import pytest
import sarge
from hypothesis import given, strategies as st
from mockito import mock, verify, when

# noinspection PyProtectedMember
from elib_run import _run
# noinspection PyProtectedMember
from elib_run._exc import ExecutableNotFoundError

_RUN_FUNC = _run.run


@pytest.fixture(name='sarge_proc')
def _command():
    exe = mock()
    exe.name = 'some_random.exe'
    command = mock()
    command.returncode = 0
    capture = mock()
    # when(_run).find_executable(...).thenRaise(RuntimeError)
    when(_run).find_executable('some_random').thenReturn(exe)
    when(_run).cmd_start(...)
    when(_run).cmd_end(...)
    when(_run).info(...)
    when(_run).error(...)
    when(_run).std_out(...)
    when(_run).std_err(...)
    when(sarge).Command(...).thenReturn(command)
    when(sarge).Capture().thenReturn(capture)
    when(command).run(...)
    yield command, capture


@given(text=st.text(alphabet=string.printable))
def test_filter_line_raw(text):
    assert _run.filter_line(text, None) == text


def test_filter_line():
    text = 'some random text'
    assert _run.filter_line(text, None) == text
    assert _run.filter_line(text, ['some']) is None
    assert _run.filter_line(text, [' some']) == text
    assert _run.filter_line(text, ['some ']) is None
    assert _run.filter_line(text, ['random']) is None
    assert _run.filter_line(text, [' random']) is None
    assert _run.filter_line(text, ['random ']) is None
    assert _run.filter_line(text, [' random ']) is None
    assert _run.filter_line(text, ['text']) is None
    assert _run.filter_line(text, [' text']) is None
    assert _run.filter_line(text, [' text ']) == text


def test_exe_not_found():
    when(_run).find_executable(...).thenReturn(None)
    with pytest.raises(ExecutableNotFoundError):
        _RUN_FUNC('some_random')


def test_basic(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'test output').thenReturn(None)
    output, returncode = _RUN_FUNC('some_random')
    assert returncode is 0
    assert 'test output' == output


@pytest.mark.parametrize(
    'input_,output',
    [
        (b'test', 'test'),
        (b'test\n', 'test'),
        (b'test\n\n', 'test'),
        (b'test\n\ntest', 'test\n\ntest'),
        (b'test\n\ntest\n', 'test\n\ntest'),
        (b'test\n\ntest\n\n', 'test\n\ntest'),
    ]
)
def test_output(sarge_proc, input_, output):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(input_).thenReturn(None)
    # process.out = input_
    out, code = _RUN_FUNC('some_random')
    verify(_run).info('some_random.exe -> 0')
    verify(_run, times=0).cmd_start(...)
    verify(_run, times=0).cmd_end(...)
    verify(_run, times=0).std_err(...)
    verify(_run).std_out(output)
    verify(_run, times=0).error(...)
    assert code == 0
    assert out == output


def test_mute_output(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'output').thenReturn(None)
    out, code = _RUN_FUNC('some_random', mute=True)
    verify(_run, times=0).info(...)
    verify(_run, times=0).error(...)
    verify(_run).cmd_end(' -> 0')
    verify(_run, times=0).std_err(...)
    verify(_run, times=0).std_out(...)
    assert code == 0
    assert out == 'output'


def test_multi_line_output(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'output').thenReturn(b'test').thenReturn(None)
    out, code = _RUN_FUNC('some_random', mute=True)
    verify(_run, times=0).info(...)
    verify(_run, times=0).error(...)
    verify(_run).cmd_end(' -> 0')
    verify(_run, times=0).std_err(...)
    verify(_run, times=0).std_out(...)
    assert code == 0
    assert 'output\ntest' == out


def test_filter_as_str(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'output').thenReturn(b'test').thenReturn(None)
    out, code = _RUN_FUNC('some_random', mute=True, filters='test')
    verify(_run, times=0).info(...)
    verify(_run, times=0).error(...)
    verify(_run).cmd_end(' -> 0')
    verify(_run, times=0).std_err(...)
    verify(_run, times=0).std_out(...)
    assert code == 0
    assert 'output' == out


def test_filter_as_list(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'output').thenReturn(b'test').thenReturn(None)
    out, code = _RUN_FUNC('some_random', filters=['output', 'test'])
    verify(_run).info('some_random.exe -> 0')
    verify(_run, times=0).cmd_start(...)
    verify(_run, times=0).cmd_end(...)
    verify(_run, times=0).std_err(...)
    verify(_run, times=0).std_out(...)
    verify(_run, times=0).error(...)
    assert code == 0
    assert '' == out


def test_no_output(sarge_proc):
    command, capture = sarge_proc
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(None)
    out, code = _RUN_FUNC('some_random')
    verify(_run).info('some_random.exe -> 0')
    verify(_run, times=0).cmd_start(...)
    verify(_run, times=0).cmd_end(...)
    verify(_run, times=0).std_err(...)
    verify(_run, times=0).std_out(...)
    verify(_run, times=0).error(...)
    assert code == 0
    assert out == ''


def test_error(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'some error').thenReturn(None)
    out, code = _RUN_FUNC('some_random', failure_ok=True, filters=['test'])
    verify(_run, times=0).cmd_start(...)
    verify(_run, times=0).cmd_end(...)
    verify(_run, times=0).std_err(...)
    verify(_run).std_out('some error')
    verify(_run).error('command failed: some_random.exe -> 1')
    assert code == 1
    assert out == 'some error'


def test_error_muted_process(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'some error').thenReturn(None)
    out, code = _RUN_FUNC('some_random', failure_ok=True, filters=['test'], mute=True)
    verify(_run).cmd_start(...)
    verify(_run).cmd_end(...)
    verify(_run).std_err('some_random.exe error:\nsome error')
    verify(_run, times=0).std_out(...)
    verify(_run).error('command failed: some_random.exe -> 1')
    assert code == 1
    assert out == 'some error'


def test_error_no_result(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(None)
    out, code = _RUN_FUNC('some_random', failure_ok=True)
    verify(_run, times=0).cmd_start(...)
    verify(_run, times=0).cmd_end(...)
    verify(_run, times=0).std_err(...)
    verify(_run, times=0).std_out(...)
    verify(_run).error('command failed: some_random.exe -> 1')
    assert code == 1
    assert out == ''


def test_error_muted(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(None)
    out, code = _RUN_FUNC('some_random', failure_ok=True, mute=True)
    verify(_run, times=0).info(...)
    verify(_run).cmd_start(...)
    verify(_run).cmd_end('')
    verify(_run).std_err(...)
    verify(_run, times=0).std_out(...)
    verify(_run).error('command failed: some_random.exe -> 1')
    assert code == 1
    assert out == ''


def test_failure(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'error').thenReturn(None)
    with pytest.raises(SystemExit):
        _RUN_FUNC('some_random')
    verify(_run, times=0).cmd_start(...)
    verify(_run, times=0).cmd_end(...)
    verify(_run, times=0).std_err(...)
    verify(_run).std_out('error')
    verify(_run).error('command failed: some_random.exe -> 1')


def test_failure_muted(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 1
    when(command).poll().thenReturn(0)
    when(capture).readline(...).thenReturn(b'error').thenReturn(None)
    with pytest.raises(SystemExit):
        _RUN_FUNC('some_random', mute=True)
    verify(_run).cmd_start(...)
    verify(_run).cmd_end(...)
    verify(_run).std_err('some_random.exe error:\nerror')
    verify(_run, times=0).std_out(...)
    verify(_run).error('command failed: some_random.exe -> 1')


def test_polling(sarge_proc):
    command, capture = sarge_proc
    command.returncode = 0
    when(command).poll().thenReturn(None).thenReturn(None).thenReturn(True)
    when(capture).readline(...).thenReturn(b'out1').thenReturn(b'out2').thenReturn(b'out3').thenReturn(None)
    out, code = _RUN_FUNC('some_random')
    assert code is 0
    assert 'out1\nout2\nout3' == out


def test_process_timeout(sarge_proc):
    command, _ = sarge_proc
    when(command).poll().thenReturn(None)
    with pytest.raises(SystemExit):
        _RUN_FUNC('some_random', timeout=0.1)


def test_without_args():
    out, code = _RUN_FUNC('echo')
    assert code is 0
    assert '' == out


def test_with_args():
    out, code = _RUN_FUNC('echo test')
    assert code is 0
    assert 'test' == out
