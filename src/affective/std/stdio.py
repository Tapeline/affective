import sys
from typing import Any

from affective import operation, handler, Effect, Affects
from affective.core.continuation import Continuation, RunningContinuation


class Console(Effect):
    @operation
    def read() -> Affects[str]: ...

    @operation
    def write(text: str) -> Affects[None]: ...


@handler(Console.write)
def default_stdout_writer(
    then: Continuation[[None]], text: str
) -> Affects[Any]:
    def h():
        sys.stdout.write(text)
        sys.stdout.flush()
        ret = yield from then(None)
        return ret
    return (yield from then(h))


@handler(Console.read)
def default_stdin_reader(
    then: Continuation[[str]]
) -> Affects[Any]:
    def h():
        ret = yield from then(sys.stdin.readline().removesuffix("\n"))
        return ret
    return (yield from then(h))


default_stdio_handler = default_stdout_writer + default_stdin_reader
