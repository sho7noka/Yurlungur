# -*- coding: utf-8 -*-
import sys
import inspect

from math import *  # noQA
from ctypes import *  # noQA
from operator import *  # noQA
from colorsys import *  # noQA
from functools import *  # noQA

import yurlungur.core.app

# numpy is available on Houdini and Blender.
try:
    import numpy as nm
except ImportError:
    pass


# @total_ordering
class YVector(Structure):
    _fields_ = [
        ("x", c_int),
        ("y", c_int),
        ("z", c_int)
    ]

    def __eq__(self, other):
        return True

    def identify(self):
        return

    def dot_poduct(a, b, norm=False):
        if norm:  # 正規化オプション
            a = normalize(a)
            b = normalize(b)
        dot = (a[0] * b[0]) + (a[1] * b[1])
        return dot

    def normalize(a):
        length = length(a)
        return [a[0] / length, a[1] / length]

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)


# @total_ordering
class YMatrix3(Structure):
    pass


# @total_ordering
class YMatrix4(Structure):
    pass


class YColor(object):
    pass


__all__ = map(lambda x: x[0], inspect.getmembers(sys.modules[__name__], inspect.isclass))
