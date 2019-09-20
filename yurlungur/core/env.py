# -*- coding: utf-8 -*-
import sys

try:
    import os
    import functools
    import platform
except ImportError:
    pass


def __config__(file):
    """
    Maya.env / usersetup.mel
    init_unreal.py
    setup.ms
    nuke.py
    substance
    photoshop.py
    """
    with open(file, "w") as f:
        f.write("")
    return


def __import__(name, globals=None, locals=None, fromlist=None):
    # Fast path: see if the module has already been imported.
    try:
        return sys.modules[name]
    except KeyError:
        pass

    if platform.python_implementation() == "IronPython":
        import clr
        clr.AddReferenceByPartialName(name)

    try:
        if "DaVinci" in name:
            if platform.system() == "Windows":
                resolve = "%PROGRAMDATA%\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules"
            if platform.system() == "Darwin":
                resolve = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
            if platform.system() == "Linux":
                resolve = "/opt/resolve/Developer/Scripting/Modules"

            sys.path.append(resolve)
            name = "DaVinciResolveScript"

    except NameError:
        pass

    try:
        import imp
    except ImportError:
        from importlib import import_module
        return import_module(name)

    try:
        fp, pathname, description = imp.find_module(name)
        return imp.load_module(name, fp, pathname, description)
    except ImportError:
        return False


def Maya(func=None):
    if func is None:
        return "maya" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "maya" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Houdini(func=None):
    if func is None:
        return __import__("hou")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("hou"):
            return func(*args, **kwargs)

    return wrapper


def Substance(func=None):
    if func is None:
        return "Substance" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Substance" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Max(func=None):
    if func is None:
        return "3dsmax" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "3dsmax" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Unreal(func=None):
    if func is None:
        return "UE4" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "UE4" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Photoshop(func=None):
    if func is None:
        try:
            from yurlungur.adapters import photoshop
            return photoshop.app.isRunning()
        except Exception:
            return False

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            from yurlungur.adapters import photoshop
            if photoshop.app.isRunning():
                return func(*args, **kwargs)
            else:
                raise WindowsError
        except Exception:
            return False

    return wrapper


def Nuke(func=None):
    if func is None:
        return "Nuke" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Nuke" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Davinci(func=None):
    if func is None:
        return __import__("DaVinciResolveScript")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("DaVinciResolveScript"):
            return func(*args, **kwargs)

    return wrapper


def C4D(func=None):
    if func is None:
        return "Cinema 4D" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "Cinema 4D" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Blender(func=None):
    if func is None:
        return "blender" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "blender" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def installed(app):
    _app = app.lower()

    if _app == "maya":
        return os.path.exists(_Maya())
    if _app == "houdini":
        return os.path.exists(_Houdini())
    if _app == "unreal":
        return os.path.exists(_Unreal())
    if _app == "blender":
        return os.path.exists(_Blender())
    if _app == "max":
        return os.path.exists(_Max())
    if _app == "substance":
        return os.path.exists(_Substance())
    if _app == "photoshop":
        return os.path.exists(_Photoshop())
    if _app == "c4d":
        return os.path.exists(_Cinema4D())

    return False


def Qt(func=None):
    try:
        import yurlungur.Qt as Qt
        is_Qt = any([Qt])
    except ImportError:
        return False

    if func is None:
        return is_Qt

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if is_Qt:
            return func(*args, **kwargs)

    return wrapper


def Numpy(func=None):
    try:
        import numpy as nm
        is_numpy = True
    except ImportError:
        return False

    if func is None:
        return nm

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if is_numpy:
            return func(*args, **kwargs)

    return wrapper


def _Maya():
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Autodesk/Maya2018",
        "Darwin": "/Applications/Autodesk/maya2018/Maya.app/Contents",
    }
    return os.environ.get("MAYA_LOCATION") or d[platform.system()]


def _Houdini():
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Side Effects Software/Houdini Houdini17.5.173/bin",
        "Darwin": "/Applications/Houdini/Houdini17.5.173/Frameworks/Houdini.framework/Versions/Current/Resources/bin",
    }
    return os.environ.get("HIP") or d[platform.system()]


def _Substance():
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Side Effects Software/Houdini 16.5.323/bin",
        "Darwin": "/Applications/Substance Designer.app/Contents",
    }
    return d[platform.system()]


def _Photoshop():
    d = {
        "Windows": "C:/Program Files/Adobe/Adobe Photoshop CC 2019",
        "Darwin": "/Applications/Photoshop.app/Contents",
    }
    return d[platform.system()]


def _Max():
    return os.environ.get("ADSK_3DSMAX_X64_2019") or "C:/Program Files/Autodesk/3ds Max 2019"


def _Blender():
    d = {
        "Linux": "",
        "Windows": "C:/Program Files/Blender Foundation/Blender",
        "Darwin": "/Applications/Blender2.8/blender.app/Contents/MacOS/blender"
    }
    return d[platform.system()]


def _Unreal():
    d = {
        "Linux": "",
        "Windows": "C:/Program Files/Epic Games/UE_4.20/Engine/Binaries/Win64",
        "Darwin": ""
    }
    return d[platform.system()]


def _Cinema4D():
    d = {
        "Linux": "",
        "Windows": "C:/Cinema/R21/c4dpy.exe",
        "Darwin": "/Applications/Maxon Cinema 4D R21/c4dpy.app/Contents/MacOS/c4dpy"
    }
    return d[platform.system()]
