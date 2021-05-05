import os
import sys
import importlib

from yurlungur.core.deco import Windows, Mac

if Windows():
    ext = os.path.join(os.getenv("PROGRAMFILES"), "JetBrains")
    pyext = list(filter(lambda x: x.startswith("PyCharm"), os.listdir(ext)))
    path = os.path.join(ext, pyext[-1])
if Mac():
    path = "/Applications/PyCharm.app/Contents"
    path = "/Users/shosumioka/Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/211.7142.13/PyCharm.app/Contents"

egg_path = os.path.join(path, "debug-eggs/pydevd-pycharm.egg").replace(os.sep, "/")
sys.path.append(egg_path)

# import pydevconsole;
# pydevconsole.py --mode=client --port=53567

# https://pleiades.io/help/pycharm/remote-debugging-with-product.html
try:
    pycharm = importlib.import_module("pydevd_pycharm")
    pycharm.remote_debug = _listen
except ModuleNotFoundError:
    pass
