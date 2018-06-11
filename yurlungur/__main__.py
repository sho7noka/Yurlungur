# -*- coding: utf-8 -*-
import sys
import os
import inspect

# settings
sys.dont_write_bytecode = True
local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
if not local in sys.path:
    sys.path.append(local)

if __name__ == "__main__":
    from yurlungur.core.standalone import _cli
    _cli(sys.argv[1:])
