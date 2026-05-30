from mypy.plugin import Plugin

from affective.mypy_ext.plugin import AffectivePlugin


def plugin(version: str) -> type[Plugin]:
    if not version.startswith("2."):
        raise ValueError("Cannot run Affective with mypy < 2.0.0")
    return AffectivePlugin
