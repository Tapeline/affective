from collections.abc import Callable
from affective import Affects, Raise


def try_or_raise[T](
    fn: Callable[[], T], fallback: T
) -> Affects[T, Raise[Exception]]:
    try:
        val = fn()
    except Exception as exc:
        yield from Raise.error(exc)
        return fallback
    else:
        return val


def transform_exceptions(f):
    def wrapper(*args, **kwargs):
        try:
            return (yield from f(*args, **kwargs))
        except Exception as exc:
            return (yield from Raise.error(exc))
    return wrapper
