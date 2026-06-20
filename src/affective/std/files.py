from typing import Any

from affective import Effect, Affects, Raise, operation, Continuation, handler


class Files:
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
    path: str,
    contents: bytes
) -> Affects[None]:
    try:
        with open(path, "wb") as f:
            f.write(contents)
    except PermissionError as exc:
        yield from Raise.error(exc)


@handler(Files.read)
def _handle_default_read(
    path: str,
) -> Affects[bytes]:
    try:
        with open(path, "rb") as f:
            contents = f.read()
    except PermissionError as exc:
        yield from Raise.error(exc)
    else:
        return contents


default_files_handler = _handle_default_read + _handle_default_write
