# -*- coding: utf-8 -*-
import sys
import inspect
import cmath

from yurlungur.core.wrapper import (
    _YVector, _YMatrix, _YColor
)
from yurlungur.core.env import Numpy, Blender

if Numpy():
    import numpy as np
else:
    pass


class YVector(_YVector):
    def __init__(self, *args, **kwargs):
        if Blender():
            super(YVector, self).__init__()
            self.vector = [self.x, self.y, self.z]
        else:
            super(YVector, self).__init__(*args, **kwargs)
            self.vector = args

    @Numpy
    def array(self):
        return np.array(self.vector, dtype=np.float16)

    def identify(self):
        return

    def dot(self, a, b, norm=False):
        if norm:  # 正規化オプション
            a = self.normalize(a)
            b = self.normalize(b)
        dot = (a[0] * b[0]) + (a[1] * b[1])
        return dot

    def cross(self, a, b):
        return

    @Numpy
    def normalize(self, a):
        length = self.length(a)
        return [a[0] / length, a[1] / length]

    def length(self):
        return cmath.sqrt(self.x ** 2 + self.y ** 2)


class YMatrix(_YMatrix):
    def __init__(self, *args, **kwargs):
        super(YMatrix, self).__init__(*args, **kwargs)


class YColor(_YColor):
    def __init__(self, *args, **kwargs):
        super(YColor, self).__init__(*args, **kwargs)


__all__ = map(lambda x: x[0], inspect.getmembers(sys.modules[__name__], inspect.isclass))
