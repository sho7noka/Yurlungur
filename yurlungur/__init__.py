# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import sys

sys.dont_write_bytecode = True

from yurlungur.core import *  # noQA
from yurlungur.tool.standalone import *  # noQA
from yurlungur.tool.patch import *  # noQA

__version__ = "0.9.8"
name = __name__
version = __version__

del sys
