"""
https://docs.substance3d.com/sddoc/debugging-plugins-using-visual-studio-code-172825679.html
https://help.autodesk.com/view/MAXDEV/2021/ENU/?guid=Max_Python_API_tutorials_creating_the_dialog_html
https://jurajtomori.wordpress.com/2018/06/13/debugging-python-in-vfx-applications/
https://developers.maxon.net/docs/Cinema4DPythonSDK/html/manuals/introduction/python_c4dpy.html
https://github.com/Barbarbarbarian/Blender-VScode-Debugger/blob/master/Blender_VScode_Debugger.py
https://www.sidefx.com/ja/docs/houdini18.0/hom/hou/ShellIO
"""
import os
import importlib
import sys
import types

from yurlungur.core.deco import Windows, Mac
from yurlungur.tool.rpc import remote_debug_listen

try:
    path = "/usr/bin"
    if Windows():
        path = os.getenv("USERPROFILE")
    if Mac():
        path = os.getenv("HOME")
    ext = os.path.join(path, ".vscode/extensions")
    pyext = list(filter(lambda x: x.startswith("ms-python.python"), os.listdir(ext)))
    mspy = os.path.join(ext, pyext[-1], "pythonFiles/lib/python").replace(os.sep, "/")
    sys.path.append(mspy)

    sys.modules[__name__] = importlib.import_module("debugpy")
    setattr(sys.modules[__name__], "remote_debug", remote_debug_listen)
    setattr(sys.modules[__name__], "enable", True)

except:
    sys.modules[__name__] = types.ModuleType("vscode")
    setattr(sys.modules[__name__], "enable", False)
