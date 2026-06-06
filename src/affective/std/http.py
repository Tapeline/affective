from dataclasses import dataclass
from logging import Handler
from typing import Any

try:
    from aiohttp.web_response import Response
    from aiohttp import ClientSession
except ImportError as exc:
    raise ImportError(
        "Cannot use Http effects without [aiohttp] extra"
    ) from exc

from affective import Async, Effect, handler, operation, Continuation, Affects


@dataclass
class HttpResponse:
    status_code: int
    data: bytes
    headers: dict[str, str]


class Http(Effect):
    @operation
    def request(
        method: str,
        url: str,
        params: str | dict[str, Any] | None = None,
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        timeout_s: float | None = None,
    ) -> Affects[HttpResponse]:
        ...


@handler(Http.request)
def _async_request_handler(
    then: Continuation[[HttpResponse]],
    method: str,
    url: str,
    params: str | dict[str, Any] | None = None,
    data: Any | None = None,
    headers: dict[str, str] | None = None,
    timeout_s: float | None = None,
) -> Affects[Any, Async]:
    async def _do() -> HttpResponse:
        async with (
            ClientSession() as session,
            session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                timeout=timeout_s,
                raise_for_status=False,
            ) as response
        ):
            response_data = await response.read()
            return HttpResponse(
                status_code=response.status,
                data=response_data,
                headers={
                    header: value
                    for header, value in response.headers.items()
                },
            )

    result = yield from Async.wait(_do())
    ret = yield from then(result)
    return ret


async_http_handler = _async_request_handler
