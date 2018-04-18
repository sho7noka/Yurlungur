# -*- coding: utf-8 -*-
import sys
import inspect
from math import sqrt

from yurlungur.tool.meta import meta
from yurlungur.core.wrapper import (
    _YVector, _YMatrix, _YColor
)

try:
    import maya.api.OpenMaya as OM
except ImportError:
    pass


# @total_ordering
class YVector(_YVector):
    def __init__(self):
        super(YVector, self).__init__()

    def __eq__(self, other):
        return True

    def identify(self):
        return

    def dot_poduct(self, a, b, norm=False):
        if norm:  # 正規化オプション
            a = self.normalize(a)
            b = self.normalize(b)
        dot = (a[0] * b[0]) + (a[1] * b[1])
        return dot

    def normalize(self, a):
        length = self.length(a)
        return [a[0] / length, a[1] / length]

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)


class YMatrix(_YMatrix):
    def __init__(self):
        super(YMatrix, self).__init__()


class YColor(_YColor):
    def __init__(self):
        super(YColor, self).__init__()

        if hasattr(meta, "Color"):
            self.color = meta.Color()
        else:
            self.color = OM.MColor()

    @property
    def r(self):
        return self.color[0]

    @property
    def g(self):
        return self.color[1]

    @property
    def b(self):
        return self.color[2]


__all__ = map(lambda x: x[0], inspect.getmembers(sys.modules[__name__], inspect.isclass))
