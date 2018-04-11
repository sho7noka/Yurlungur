# -*- coding: utf-8 -*-
from yurlungur.core.wrapper import YMObject
from yurlungur.tool import util

meta = YMObject()
util.make_completer(meta.module)
__all__ = ["meta"]