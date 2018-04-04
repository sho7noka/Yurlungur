# -*- coding: utf-8 -*-
import sys
import inspect
from cmath import *      # noQA
from ctypes import *     # noQA
from operator import *   # noQA
from colorsys import *   # noQA
from functools import total_ordering

# numpy is available on Houdini and Blender.
try:
    import numpy as nm
except ImportError:
    pass
    # logging.log("numpy is not available".format())

# @total_ordering
class YVector(Structure):
    def __eq__(self, other):
        return True
    
# @total_ordering
class YMatrix3(Structure):
    pass

# @total_ordering
class YMatrix4(Structure):
    pass

class YColor(object):
    pass


__all__ = map(lambda x:x[0],inspect.getmembers(sys.modules[__name__],inspect.isclass))