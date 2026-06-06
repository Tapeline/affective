from affective import operation, Effect

from sample_app.app.domain import User


class UserStorage(Effect):
    @operation
    def read_user(name: str) -> User | None: ...

    @operation
    def save_user(user: User) -> None: ...


class MemeFetcher(Effect):
    @operation
    def get_joke() -> str: ...
