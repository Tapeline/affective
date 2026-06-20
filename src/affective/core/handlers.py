from collections.abc import Callable, Generator
from dataclasses import dataclass
from typing import Any, Concatenate


from affective.core.types import Perform

@dataclass
class OperationHandlerCollection:
    """A collection of handlers."""
    
    handlers: dict[Any, Callable[
        ...,
        Generator[Perform, Any, Any]
    ]]

    def __add__(
        self, other: Any
    ) -> "OperationHandlerCollection":
        match other:
            case OperationHandler(op, func):
                return OperationHandlerCollection(self.handlers | {op: func})
            case OperationHandlerCollection(handlers):
                return OperationHandlerCollection(handlers | self.handlers)
            case None:
                return self
            case _:
                return NotImplemented

    def __radd__(self, other: Any) -> "OperationHandlerCollection":
        return self.__add__(other)


@dataclass
class OperationHandler[**P = ..., R = Any]:
    operation: Any
    func: Callable[
        Concatenate[Callable[[R], Generator[Any, Any, Any]], P],
        Generator[Perform, Any, R]
    ]

    def __add__(self, other: Any) -> "OperationHandlerCollection":
        match other:
            case OperationHandler(op, func):
                return OperationHandlerCollection(
                    {op: func, self.operation: self.func}
                )
            case _:
                return NotImplemented

