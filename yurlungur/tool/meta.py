# -*- coding: utf-8 -*-
from yurlungur.core.wrapper import YMObject
from yurlungur.core import util

meta = YMObject()
modules = util.__make_completer(meta.module)

__all__ = ["meta"]

# add completer
# for mod in modules:
#     __all__.append(mod)
