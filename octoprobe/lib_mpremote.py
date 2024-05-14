import logging
from typing import Self

from mpremote.main import State

from mpremote.transport_serial import SerialTransport, TransportError

logger = logging.getLogger(__file__)


class ExceptionMpRemote(Exception):
    pass


class ExceptionCmdFailed(ExceptionMpRemote):
    pass


class ExceptionTransport(ExceptionMpRemote):
    pass


class MpRemote:
    def __init__(self, tty: str, baudrate=115200):
        self.state = State()
        self.state.transport = SerialTransport(tty, baudrate=baudrate)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def exec_raw(self, cmd: str, follow=True) -> str:
        """
        Derived from mpremote.commands.do_exec / do_execbuffer
        """
        self.state.ensure_raw_repl()
        self.state.did_action()

        try:
            self.state.transport.exec_raw_no_follow(cmd)
            if follow:
                # ret, ret_err = state.transport.follow(timeout=None, data_consumer=stdout_write_bytes)
                ret, ret_err = self.state.transport.follow(timeout=None)
                if ret_err:
                    logger.warning(ret_err)
                    raise ExceptionCmdFailed(ret_err)
        except TransportError as er:
            logger.warning(er)
            raise ExceptionTransport(er) from er

        return ret.decode("utf-8")

    def close(self):
        self.state.transport.close()
