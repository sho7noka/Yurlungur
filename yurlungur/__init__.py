from __future__ import print_function, unicode_literals, division
import sys
assert sys.version_info > (2, 6), ('yurlungur currently requires Python 2.6')

from yurlungur.core import *
from yurlungur.tools.util import *
from yurlungur.tools.qtutil import *
from yurlungur.tools.meta import meta

__all__ = []
__version__ = "0.1"
__name__ = "Yurlungur"

name = __name__
version = __version__