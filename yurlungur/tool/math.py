# -*- coding: utf-8 -*-
import sys
import cmath
import inspect

from yurlungur.tool.meta import meta
from yurlungur.core.wrapper import (
    _YVector, _YMatrix, _YColor, OM
)
from yurlungur.core.env import Numpy

if Numpy():
    import numpy as nm
    import requests


class YVector(_YVector):
    def __init__(self, *args, **kwargs):
        super(YVector, self).__init__(*args, **kwargs)

    def __getitem__(self, index):
        return [
            super(YVector, self).x(),
            super(YVector, self).y(),
            super(YVector, self).z()][index]

    def identify(self):
        return

    def dot_poduct(self, a, b, norm=False):
        if norm:  # 正規化オプション
            a = self.normalize(a)
            b = self.normalize(b)
        dot = (a[0] * b[0]) + (a[1] * b[1])
        return dot

    @Numpy
    def normalize(self, a):
        length = self.length(a)
        return [a[0] / length, a[1] / length]

    def length(self):
        return cmath.sqrt(self.x ** 2 + self.y ** 2)


class YMatrix(_YMatrix):
    def __init__(self, *args, **kwargs):
        super(YMatrix, self).__init__(*args, **kwargs)

    def __getitem__(self, index):
        return [
            super(YMatrix, self).x(),
            super(YMatrix, self).y(),
            super(YMatrix, self).z()][index]


class YColor(_YColor):
    def __init__(self, *args, **kwargs):
        super(YColor, self).__init__(*args, **kwargs)

    def __getitem__(self, index):
        return [
            super(YColor, self).x(),
            super(YColor, self).y(),
            super(YColor, self).z()][index]

    @property
    def r(self):
        pass

    @property
    def g(self):
        pass

    @property
    def b(self):
        pass


__all__ = map(lambda x: x[0], inspect.getmembers(sys.modules[__name__], inspect.isclass))