import sys

from affective import operation, handler, Affects
from affective.core.decorators import const_handler
from affective.core.effects import Effect


class Console(Effect):
    @operation
    def read() -> Affects[str]: ...

    @operation
    def write(text: str) -> Affects[None]: ...


@const_handler(Console.write)
def default_stdout_writer(text: str) -> None:
    sys.stdout.write(text)
    sys.stdout.flush()


@const_handler(Console.read)
def default_stdin_reader() -> str:
    return sys.stdin.readline().removesuffix("\n")


default_stdio_handler = default_stdout_writer | default_stdin_reader
