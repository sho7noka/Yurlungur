# -*- coding: utf-8 -*-
import sys
sys.dont_write_bytecode = True
del sys

from yurlungur.core import *            # noQA
from yurlungur.tool.standalone import * # noQA
from yurlungur.tool.patch import *      # noQA

__version__ = "0.9.8"
name = __name__
version = __version__
