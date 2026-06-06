from collections.abc import Callable, Generator
from typing import Any, ParamSpec, TypeAlias

# bcz mkdocstrings does not understand PEP695

RunningContinuation: TypeAlias = Generator[Any, Any, Any]
_ExpectsInput = ParamSpec("_ExpectsInput")
Continuation: TypeAlias = Callable[_ExpectsInput, RunningContinuation]
