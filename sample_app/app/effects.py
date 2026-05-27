from affective import effect, Effect

from sample_app.app.domain import User




@effect
class SaveUser(Effect[None]):
    user: User


@effect
class ReadUser(Effect[User | None]):
    name: str
