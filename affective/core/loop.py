from typing import Any

from affective.core.effects import Raise, Perform
from affective.core.handlers import (
    OperationHandlerCollection,
    OperationHandler,
)
from affective.core.continuation import RunningContinuation


class UnhandledEffect(Exception):
    def __init__(self, effect: Perform):
        super().__init__(
            f"Effect handler for {effect.effect_type.__qualname__} not found"
        )
        self.effect = effect


def handle(
    ctx: OperationHandlerCollection | OperationHandler,
    cont: RunningContinuation,
    effect: Perform | None = None,
) -> Any:
    if isinstance(ctx, OperationHandler):
        ctx = OperationHandlerCollection({ctx.operation: ctx.func})
    if effect is None:
        try:
            effect = next(cont)
        except StopIteration as stop:
            return stop.value
    while True:
        if not isinstance(effect, Perform):
            raise TypeError(f"Unknown yield: {effect}")
        if effect.effect_type in ctx.handlers:
            def after(effect_result: Any) -> Any:
                try:
                    eff = cont.send(effect_result)
                except StopIteration as stop:
                    return stop.value
                return_value = yield from handle(ctx, cont, eff)
                return return_value

            ret = yield from handle(
                ctx, ctx.handlers[effect.effect_type](
                    after, *effect.effect_args, **effect.effect_kwargs
                )
            )
            return ret
        else:
            effect_result = yield effect
            try:
                effect = cont.send(effect_result)
            except StopIteration as stop:
                return stop.value
            return_value = yield from handle(ctx, cont, effect)
            return return_value


def run(cont: RunningContinuation) -> Any:
    try:
        effect = next(cont)
        while True:
            if not isinstance(effect, Perform):
                raise TypeError(f"Unknown yield: {effect}")
            if effect.effect_type == Raise.error:
                raise effect.effect_args[0]
            else:
                raise UnhandledEffect(effect)
    except StopIteration as stop:
        return stop.value
