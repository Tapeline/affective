from typing import Any

from affective.core.effects import Effect, Yield
from affective.core.handlers import Handler
from affective.core.continuation import Continuation


class UnhandledEffect(Exception):
    def __init__(self, effect: Effect[Any]):
        super().__init__(f"Effect handler for {effect.__class__} not found")
        self.effect = effect


def handle(
    ctx: Handler,
    cont: Continuation,
    effect: Effect[Any] | None = None
) -> Any:
    if not effect:
        try:
            effect = next(cont)
        except StopIteration as stop:
            return stop.value
    while True:
        if isinstance(effect, Yield):
            try:
                effect = cont.send(None)
            except StopIteration as e:
                return e.value
        elif effect.__class__ in ctx.handlers:
            def after(effect_result: Any) -> Any:
                try:
                    eff = cont.send(effect_result)
                except StopIteration as stop:
                    return stop.value
                return_value = yield from handle(ctx, cont, eff)
                return return_value
            return_value = yield from ctx.handlers[effect.__class__](
                effect, after
            )
            return return_value
        else:
            effect_result = yield effect
            try:
                effect = cont.send(effect_result)
            except StopIteration as stop:
                return stop.value
            return_value = yield from handle(ctx, cont, effect)
            return return_value


def run(cont: Continuation) -> Any:
    try:
        effect = next(cont)
        while True:
            match effect:
                case Yield():
                    effect = cont.send(None)
                case _:
                    raise UnhandledEffect(effect)
    except StopIteration as stop:
        return stop.value
