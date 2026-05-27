from affective import operation, Effect

from sample_app.app.domain import User


class UserStorage(Effect):
    @operation
    def read_user(self, name: str) -> User: ...

    @operation
    def save_user(self, user: User) -> None: ...
