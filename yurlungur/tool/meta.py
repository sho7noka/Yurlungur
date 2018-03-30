from yurlungur.core.wrapper import YMObject
from yurlungur.tool import util

__all__ = ["meta"]

meta = YMObject()
util.make_completer(meta.module)