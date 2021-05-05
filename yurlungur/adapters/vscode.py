import os
import importlib
import sys

from yurlungur.core.deco import Windows, Mac
from yurlungur.tool.rpc import remote_debug_listen

if Windows():
    path = os.getenv("USERPROFILE")
if Mac():
    path = os.getenv("HOME")

ext = os.path.join(path, ".vscode/extensions")
pyext = list(filter(lambda x: x.startswith("ms-python.python"), os.listdir(ext)))
mspy = os.path.join(ext, pyext[-1], "pythonFiles/lib/python")
sys.path.append(mspy)

try:
    vscode = importlib.import_module("debugpy")
    vscode.remote_debug = remote_debug_listen
except (ModuleNotFoundError, IndexError):
    pass
