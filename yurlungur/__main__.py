from __future__ import absolute_import
import sys
sys.dont_write_bytecode = True

from core.standalone import _cli

if __name__ == "__main__":
    _cli(sys.argv[1:])