import sys
from collections.abc import Callable

from affective import operation, handler
from affective.core.effects import Effect
from affective.core.continuation import Continuation, RunningContinuation


class Console(Effect):
    @staticmethod
    @operation
    def read() -> str: ...

    @staticmethod
    @operation
    def write(text: str) -> None: ...


@handler(Console.write)
def default_stdout_writer(
    then: Continuation[[None]], text: str
) -> RunningContinuation:
    sys.stdout.write(text)
    sys.stdout.flush()
    ret = yield from then(None)
    return ret


@handler(Console.read)
def default_stdin_reader(
    then: Continuation[[str]]
) -> RunningContinuation:
    ret = yield from then(sys.stdin.readline().removesuffix("\n"))
    return ret


default_stdio_handler = default_stdout_writer + default_stdin_reader

