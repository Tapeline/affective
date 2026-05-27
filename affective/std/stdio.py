import sys
from collections.abc import Callable

from affective import operation, handler
from affective.core.effects import Effect
from affective.core.continuation import Continuation


class Console(Effect):
    @operation
    def read(self) -> str: ...

    @operation
    def write(self, text: str) -> None: ...


@handler(Console.write)
def default_stdout_writer(
    then: Callable[[None], Continuation], text: str
) -> Continuation:
    sys.stdout.write(text)
    sys.stdout.flush()
    ret = yield from then(None)
    return ret


@handler(Console.read)
def default_stdin_reader(
    then: Callable[[str], Continuation]
) -> Continuation:
    ret = yield from then(sys.stdin.readline().removesuffix("\n"))
    return ret


default_stdio_handler = default_stdout_writer + default_stdin_reader

