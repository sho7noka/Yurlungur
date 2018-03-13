import sys
assert sys.version_info > (2, 6), ('yurlungur currently requires Python 2.6')

from core import *
from util import *
from qtutil import *

nopyc

__all__ = []
__version__ = "0.1"

version = __version__