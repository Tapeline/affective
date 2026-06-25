from collections.abc import Callable

from affective import (
    Affects,
    run,
    Raise,
    handle,
    EffectGen,
)
from affective.std.stdio import Console, default_stdio_handler


def do_smth() -> Affects[str, Raise[Exception] | Console]:
    for _ in range(1, 10):
        yield from Console.write("Working\n")
    yield from Raise.error(Exception("Uh oh"))
    for _ in range(1, 10):
        yield from Console.write("Continue working\n")
    return "Result"


def force_continue[R](f: EffectGen[R]) -> Affects[R, Console]:
    def handle_error(
        k: Callable[[None], EffectGen[R]], err: Exception
    ) -> EffectGen[R]:
        yield from Console.write("Forcing resumption\n")
        return (yield from k(None))

    return (yield from handle(f, {Raise.error: handle_error}))


def main() -> Affects[None, Console]:
    result = yield from force_continue(do_smth())
    yield from Console.write(result)


if __name__ == "__main__":
    run(handle(main(), default_stdio_handler))
