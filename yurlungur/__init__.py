from __future__ import print_function, unicode_literals, division
import sys
assert sys.version_info > (2, 6), ('yurlungur currently requires Python 2.6')
sys.dont_write_bytecode = True

from yurlungur.core import *  # noQA
from yurlungur.tool.math import *  # noQA
from yurlungur.tool.util import *  # noQA
from yurlungur.tool.meta import meta

nopyc  # do not make pyc

__all__ = []
__version__ = "0.9"
__name__ = "Yurlungur"

name = __name__
version = __version__
