from typing import Any

from affective import Effect, Affects, Raise, operation, Continuation, handler


class Files(Effect):
    @operation
    def write(path: str, contents: bytes) -> Affects[
        None, Raise[PermissionError]
    ]: ...

    @operation
    def read(path: str) -> Affects[
        bytes, Raise[PermissionError] | Raise[FileNotFoundError]
    ]: ...


@handler(Files.write)
def _handle_default_write(
    then: Continuation[[None]],
    path: str,
    contents: bytes
) -> Affects[Any]:
    def h():
        try:
            with open(path, "wb") as f:
                f.write(contents)
        except Exception as exc:
            yield from Raise.error(exc)
        ret = yield from then(None)
        return ret
    return (yield from then(h))


@handler(Files.read)
def _handle_default_read(
    then: Continuation[[bytes]],
    path: str,
) -> Affects[Any]:
    def h():
        try:
            f = open(path, "rb")
            contents = f.read()
            f.close()
        except Exception as exc:
            yield from Raise.error(exc)
        else:
            ret = yield from then(contents)
            return ret
    return (yield from then(h))


default_files_handler = _handle_default_read + _handle_default_write
