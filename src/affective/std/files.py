from affective import Affects, Raise, operation, handler
from affective.core.effects import Effect


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
    path: str,
    contents: bytes
) -> Affects[None, Raise]:
    try:
        with open(path, "wb") as f:
            f.write(contents)
    except PermissionError as exc:
        yield from Raise.error(exc)


@handler(Files.read)
def _handle_default_read(
    path: str,
) -> Affects[bytes, Raise]:
    try:
        with open(path, "rb") as f:
            contents = f.read()
    except Exception as exc:
        yield from Raise.error(exc)
        return b""
    else:
        return contents


default_files_handler = _handle_default_read | _handle_default_write
