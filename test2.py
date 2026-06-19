from collections.abc import Sequence
from dataclasses import dataclass
from functools import reduce
from typing import Any


@dataclass
class Perform:
    type: Any
    args: Sequence[Any]


# Effectful function yields effects
# Handle is an effectful function that yields some effects that
# the handled function yields

# gen is the generator
# .send -- resume with some value
# returns yielded effect and accumulated context for context-aware handling
# ctx -- dict of eff_type -> handler

# handler is an effectful function that may:
# - yield some effects
# - call some other effectful functions
# - resume computation from the point where it stopped
#   and yielded effect this handler handles

def handle(gen, ctx, resume_with = None):
    while True:
        try:
            eff, add_ctx = gen.send(resume_with)
        except StopIteration as stop:
            return stop.value
        if eff.type in ctx:
            handler = ctx[eff.type](lambda res: handle(gen, ctx, res), *eff.args)
            return (yield from handle(handler, ctx | add_ctx))
        else:
            resume_with = yield eff, ctx | add_ctx
            continue
    return resume_with


def perform(t, *a):
    return (yield Perform(t, a), {})


def file_read_handler(k, filename):
    try:
        with open(filename) as f:
            return (yield from k(f.read()))
    except Exception as e:
        return (yield from perform("raise", e))


def parse_file(filename):
    data = yield from perform("read", filename)
    return data.split()


def read_or_empty(filename):
    def catch(k, err):
        return (yield from k([]))
    return (yield from handle(parse_file(filename), {"raise": catch}))


def main():
    x = handle(read_or_empty("test.txt"), {"read": file_read_handler})
    try:
        x = next(x)
    except StopIteration as e:
        print(e.value)


if __name__ == "__main__":
    main()
