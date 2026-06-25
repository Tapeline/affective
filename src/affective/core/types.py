from dataclasses import dataclass
from collections.abc import Mapping, Sequence, Callable, Generator
from typing import Any, Annotated, Concatenate


@dataclass
class Perform:
    """A request to perform an effect of specific type."""
    type: Any
    args: Sequence[Any]
    kwargs: Mapping[str, Any]


type Yielded = tuple[Perform, Handler]
type EffectGen[ReturnT] = Generator[Yielded, Any, ReturnT]
type Affects[ReturnT, Effects = None] = Annotated[EffectGen[ReturnT], Effects]
type Handler = dict[Any, Callable[Concatenate[Callable[[Any], Any], ...], Generator[Yielded, Any, Any]]]
type Continue[WithT] = Callable[[WithT], EffectGen[Any]]