import sys
from typing import Any

from affective import operation, handler, Continue, Affects


class Console:
    @operation
    def read() -> Affects[str]: ...

    @operation
    def write(text: str) -> Affects[None]: ...


@handler(Console.write)
def default_stdout_writer(text: str) -> Affects[None]:
    sys.stdout.write(text)
    sys.stdout.flush()


@handler(Console.read)
def default_stdin_reader() -> Affects[str]:
    return sys.stdin.s().removesuffix("\n")


default_stdio_handler = default_stdout_writer + default_stdin_reader
