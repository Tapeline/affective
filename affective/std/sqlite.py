import sqlite3
from typing import Any

from affective import operation, errors
from affective.core.effects import Effect


class SQLiteDB(Effect):
    @operation
    @errors(sqlite3.Error)
    def connect(self, path: str) -> None: ...

    @operation
    @errors(sqlite3.Error)
    def execute(
        self, query: str, params: tuple[Any, ...] = ()
    ) -> list[tuple[Any, ...]]: ...

    @operation
    @errors(sqlite3.Error)
    def close(self) -> None: ...


