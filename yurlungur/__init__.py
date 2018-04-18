from __future__ import print_function, unicode_literals, absolute_import
import sys
assert sys.version_info > (2, 7), ('yurlungur currently requires Python 2.7 later')
sys.dont_write_bytecode = True

# open yurlungur
import yurlungur
from yurlungur.core import *        # noQA
# from yurlungur.tool.math import *   # noQA
from yurlungur.tool.util import *   # noQA
from yurlungur.tool.meta import meta

__all__ = []
__version__ = "0.9.1"
name = __name__
version = __version__

# logger
from logging import basicConfig, getLogger, StreamHandler, DEBUG
basicConfig(level=DEBUG)
logger = getLogger(name)
handle = StreamHandler()
logger.addHandler(handle)
