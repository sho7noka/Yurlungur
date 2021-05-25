"""
import pydevconsole;
pydevconsole.py --mode=client --port=53567

# https://pleiades.io/help/pycharm/remote-debugging-with-product.html
"""

import os
import sys as __sys
import importlib
import types

from yurlungur.core.deco import Windows, Mac
from yurlungur.tool.rpc import remote_debug_listen

try:
    path = "/opt/usr"

    if Windows():
        ext = os.path.join(os.getenv("PROGRAMFILES"), "JetBrains")
        pyext = list(filter(lambda x: x.startswith("PyCharm"), os.listdir(ext)))
        path = os.path.join(ext, pyext[-1])
        if not os.path.exists(path):
            path = "%USERPROFILE%\\AppData\\Local\\JetBrains\\Toolbox\\apps\\PyCharm-P\\ch-0"
            pyext = list(filter(lambda x: not os.path.isdir(x), os.listdir(path)))
            path = os.path.join(path, pyext[-1])
    if Mac():
        path = "/Applications/PyCharm.app/Contents"
        if not os.path.exists(path):
            path = os.path.join(os.getenv("HOME"), "Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0")
            pyext = list(filter(lambda x: not x.startswith("."), os.listdir(path)))
            path = os.path.join(path, pyext[-1], "PyCharm.app/Contents")

    egg_path = os.path.join(path, "debug-eggs/pydevd-pycharm.egg").replace(os.sep, "/")
    __sys.path.append(egg_path)

    __sys.modules[__name__] = importlib.import_module("pydevd_pycharm")
    setattr(__sys.modules[__name__], "remote_debug", remote_debug_listen)
    setattr(__sys.modules[__name__], "enable", True)

except:
    __sys.modules[__name__] = types.ModuleType("pydevd_pycharm")
    setattr(__sys.modules[__name__], "enable", False)
