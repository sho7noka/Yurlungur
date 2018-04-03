# -*- coding: utf-8 -*-
from cmath import *
from ctypes import *
from operator import *

# numpy is available on Houdini and Blender.
try:
    import numpy as nm
except ImportError:
    pass
    # logging.log("numpy is not available".format())


class YVector(Structure):
    pass

class YMatrix3(Structure):
    pass

class YMatrix4(Structure):
    pass