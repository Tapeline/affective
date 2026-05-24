import sys
from collections.abc import Callable

from affective.core.effects import effect, Effect
from affective.core.handlers import Handler, EffectHandlerFunc
from affective.core.continuation import Continuation


@effect
class ReadStdin(Effect[str]):
    ...


@effect
class WriteStdin(Effect[None]):
    text: str


RWStdio = ReadStdin | WriteStdin


def default_stdout_writer(
    eff: WriteStdin, then: Callable[[None], Continuation]
) -> Continuation:
    sys.stdout.write(eff.text)
    sys.stdout.flush()
    ret = yield from then(None)
    return ret


def default_stdin_reader(
    eff: ReadStdin, then: Callable[[str], Continuation]
) -> Continuation:
    ret = yield from then(sys.stdin.readline().removesuffix("\n"))
    return ret


default_stdio_handler = Handler(default_stdout_writer, default_stdin_reader)
