from dataclasses import dataclass
from collections.abc import Mapping, Sequence, Callable, Generator
from typing import Any, Annotated


type ContYield = tuple[Perform, OperationHandlerCollection | None]


"""An alias for a convenient effectful function annotation."""
type Affects[ReturnT, Effects = None, SendT = Any] = Annotated[
    Generator[ContYield, SendT, ReturnT], Effects
]


@dataclass
class Perform:
    """A request to perform an effect of specific type."""
    type: Any
    args: Sequence[Any]
    kwargs: Mapping[str, Any]

    
type Continue[InputT] = Callable[[InputT], Generator[ContYield, Any, Any]]
