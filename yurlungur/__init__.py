from __future__ import print_function, unicode_literals, absolute_import

__all__ = []
__version__ = "0.9.5"

import sys

assert sys.version_info > (2, 7), ('yurlungur currently requires Python 2.7 later')
sys.dont_write_bytecode = True

from yurlungur.core import * # noQA
from yurlungur.tool.math import (
    YVector, YColor, YMatrix
)
from yurlungur.tool.util import (
    cache, trace, timer
)
from yurlungur.tool import ui
from yurlungur.tool.meta import meta
from yurlungur.adapters import *  # noQA

# info
name = __name__
version = __version__