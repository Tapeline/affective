from typing import cast, Any
from collections.abc import Generator
from affective.core.types import Affects, Perform, EffectGen
from affective.core.effects import Raise, Async


class UnhandledEffect(Exception):
    """Thrown directly when an effect is not handled by any context."""
    def __init__(self, effect: Perform):
        super().__init__(
            f"Effect handler for {effect.type.__qualname__} not found"
        )
        self.effect = effect


def handle[R](
    gen: EffectGen[R],
    ctx: Any,
    resume_with: Any = None
) -> EffectGen[R]:
    """
    Run effectful with handlers.
    
    Any unhandled effect will be yielded outwards.

    """
    while True:
        # TODO: refactor as trampoline
        try:
            eff, add_ctx = gen.send(resume_with)
        except StopIteration as stop:
            return cast(R, stop.value)
        if eff.type in ctx:
            handler = ctx[eff.type](
                lambda res: handle(gen, ctx, res), 
                *eff.args,
                **eff.kwargs
            )
            return (yield from handle(handler, ctx | add_ctx))
        else:
            resume_with = yield eff, ctx | add_ctx
            continue


def run[R](gen: EffectGen[R]) -> R:
    """Run effectful as main."""
    while True:
        try:
            eff, _ = gen.send(None)
        except StopIteration as stop:
            return cast(R, stop.value)
        if not isinstance(eff, Perform):
            raise TypeError(f"Unknown yield: {eff}")
        if eff.type == Raise.error:
            raise eff.args[0]
        else:
            raise UnhandledEffect(eff)


async def arun[R](gen: EffectGen[R]) -> R:
    """Run effectful as main asynchronously."""
    resume_with = None
    while True:
        try:
            eff, ctx = gen.send(resume_with)
        except StopIteration as stop:
            return cast(R, stop.value)
        if not isinstance(eff, Perform):
            raise TypeError(f"Unknown yield: {eff}")
        if eff.type == Raise.error:
            raise eff.args[0]
        elif eff.type == Async.wait:
            try:
                resume_with = await eff.args[0]
            except Exception as exc:
                raise NotImplementedError
                # TODO: somehow continue handling with this exc
        else:
            raise UnhandledEffect(eff)
