from __future__ import print_function, unicode_literals, absolute_import
from logging import basicConfig, getLogger, StreamHandler, DEBUG
from yurlungur.core import *  # noQA
from yurlungur.tool.math import *  # noQA
from yurlungur.tool.util import *  # noQA
from yurlungur.tool.meta import meta
import sys

__all__ = []
__version__ = "0.9"

name = __name__
version = __version__
sys.dont_write_bytecode = True
assert sys.version_info > (2, 6), ('yurlungur currently requires Python 2.6')

basicConfig(level=DEBUG)
logger = getLogger(name)
handle = StreamHandler()
logger.addHandler(handle)
