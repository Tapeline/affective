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
    try:
        with open(path, "wb") as f:
            f.write(contents)
    except PermissionError as exc:
        yield from Raise.error(exc)
    ret = yield from then(None)
    return ret


@handler(Files.read)
def _handle_default_read(
    then: Continuation[[bytes]],
    path: str,
) -> Affects[Any]:
    try:
        with open(path, "rb") as f:
            contents = f.read()
    except PermissionError as exc:
        yield from Raise.error(exc)
    else:
        ret = yield from then(contents)
        return ret


default_files_handler = _handle_default_read + _handle_default_write
