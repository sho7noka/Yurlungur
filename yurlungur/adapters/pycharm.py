"""
import pydevconsole;
pydevconsole.py --mode=client --port=53567

# https://pleiades.io/help/pycharm/remote-debugging-with-product.html
"""

import os
import sys
import importlib
import types
import platform

from yurlungur.tool.rpc import remote_debug_listen

try:
    if platform.system() == "Windows":
        ext = os.path.join(os.getenv("PROGRAMFILES"), "JetBrains")
        pyext = list(filter(lambda x: x.startswith("PyCharm"), os.listdir(ext)))
        path = os.path.join(ext, pyext[-1])
        if not os.path.exists(path):
            path = "%USERPROFILE%\\AppData\\Local\\JetBrains\\Toolbox\\apps\\PyCharm-P\\ch-0"
            pyext = list(filter(lambda x: not os.path.isdir(x), os.listdir(path)))
            path = os.path.join(path, pyext[-1])
    elif platform.system() == "Darwin":
        path = "/Applications/PyCharm.app/Contents"
        if not os.path.exists(path):
            path = os.path.join(os.getenv("HOME"), "Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0")
            pyext = list(filter(lambda x: not x.startswith("."), os.listdir(path)))
            path = os.path.join(path, pyext[-1], "PyCharm.app/Contents")
    else:
        path = "/opt/usr"

    egg_path = os.path.join(path, "debug-eggs/pydevd-pycharm.egg").replace(os.sep, "/")
    sys.path.append(egg_path)

    sys.modules[__name__] = importlib.import_module("pydevd_pycharm")
    setattr(sys.modules[__name__], "remote_debug", remote_debug_listen)
    setattr(sys.modules[__name__], "enable", True)

except:
    sys.modules[__name__] = types.ModuleType("pydevd_pycharm")
    setattr(sys.modules[__name__], "enable", False)
