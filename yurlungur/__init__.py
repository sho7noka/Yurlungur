import sys

assert sys.version_info > (2, 7), ('yurlungur currently requires Python 2.7 later')
sys.dont_write_bytecode = True

from yurlungur.core import *  # noQA
from yurlungur.tool import ui

__all__ = []
__version__ = "0.9.6"

# info
name = __name__
version = __version__

del sys
