from collections.abc import Callable, Sequence
from typing import Any
import inspect

from affective.core.effects import Effect
from affective.core.continuation import Continuation

type EffectHandlerFunc[EffectResultT, EffectT: Effect[Any]] = Callable[
    [
        EffectT,
        Callable[[EffectResultT], Continuation]
    ],
    Continuation
]


class HandlerImproperlyConfigured(Exception):
    def __init__(self, handler: Callable[..., Any]) -> None:
        super().__init__(
            f"Handler {handler.__qualname__} is improperly configured. "
            f"First positional parameter should accept an effect"
        )
        self.handler = handler


class Handler:
    def __init__(self, *handlers: EffectHandlerFunc[Any] | "Handler") -> None:
        self.handlers: dict[type[Effect[Any]], EffectHandlerFunc[Any]] = {}
        for handler in handlers:
            match handler:
                case Handler():
                    for effect, handler in handler.handlers.items():
                        self.handlers[effect] = handler
                case _:
                    effect_t = _resolve_effect_t(handler)
                    self.handlers[effect_t] = handler


def _resolve_effect_t(handler: Callable[..., Any]) -> type[Any]:
    first_positional = next(
        (
            param for param in inspect.signature(handler).parameters.values()
            if param.kind in {inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD}
        ), None
    )
    if not first_positional:
        raise HandlerImproperlyConfigured(handler)
    return first_positional.annotation
