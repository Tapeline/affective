from collections.abc import Callable, Generator
from typing import Any

type Continuation[**ExpectsInput] = Callable[ExpectsInput, RunningContinuation]
type RunningContinuation = Generator[Any, Any, Any]
