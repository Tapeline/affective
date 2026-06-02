from typing import Callable, Optional

from mypy.plugin import Plugin, ClassDefContext
from mypy.nodes import Decorator


def abstractise_effects(ctx: ClassDefContext) -> None:
    for stmt in ctx.cls.defs.body:
        if isinstance(stmt, Decorator):
            stmt.func.abstract_status = 1


class AffectivePlugin(Plugin):
    def get_base_class_hook(self, fullname: str) -> Optional[
        Callable[[ClassDefContext], None]
    ]:
        if fullname == "affective.core.effects.Effect":
            return abstractise_effects
        return None
