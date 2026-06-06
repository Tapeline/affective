import json
import os
from typing import Any

from affective import handler, Continuation, Affects
from affective.std.http import Http, HttpResponse
from sample_app.app.effects import MemeFetcher

API_KEY = os.environ.get("API")


@handler(MemeFetcher.get_joke)
def handle_get_joke(
    then: Continuation[[str]],
) -> Affects[Any, Http]:
    response: HttpResponse = yield from Http.request(
        "GET", "https://api.api-ninjas.com/v1/jokes",
        headers={"X-Api-Key": API_KEY}
    )
    if response.status_code != 200:
        joke = "No joke for you, sorry"
    else:
        joke =  json.loads(response.data.decode("utf-8"))[0]["joke"]
    ret = yield from then(joke)
    return ret
