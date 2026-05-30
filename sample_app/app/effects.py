from affective import operation, Effect

from sample_app.app.domain import User


class UserStorage(Effect):
    @staticmethod
    @operation
    def read_user(name: str) -> User: ...

    @staticmethod
    @operation
    def save_user(user: User) -> None: ...
