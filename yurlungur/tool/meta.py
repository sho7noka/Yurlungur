# -*- coding: utf-8 -*-
from yurlungur.core.wrapper import YMObject
from yurlungur.tool import util

meta = YMObject()
modules = util.__make_completer(meta.module)

__all__ = ["meta"]

# for mod in modules:
#     __all__.append(mod)
