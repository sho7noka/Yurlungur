# -*- coding: utf-8 -*-
import functools
import os
import platform
import sys


def __import__(name, globals=None, locals=None, fromlist=None):
    # Fast path: see if the module has already been imported.
    try:
        return sys.modules[name]
    except KeyError:
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


def Qt(func=None):
    try:
        import yurlungur.Qt as Qt
        isQt = any([Qt])
    except ImportError:
        return False

    if func == None:
        return isQt

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if isQt:
            return func(*args, **kwargs)

    return wrapper


def Numpy(func=None):
    try:
        import numpy as nm
        isNpy = True
    except ImportError:
        return False

    if func == None:
        return isNpy

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if isNpy:
            return func(*args, **kwargs)

    return wrapper


def Windows(func=None):
    if func == None:
        return platform.system() == "Windows"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Windows":
            return func(*args, **kwargs)

    return wrapper


def Linux(func=None):
    if func == None:
        return platform.system() == "Linux"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Linux":
            return func(*args, **kwargs)

    return wrapper


def MacOS(func=None):
    if func == None:
        return platform.system() == "Darwin"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Darwin":
            return func(*args, **kwargs)

    return wrapper


def Maya(func=None):
    if func == None:
        return "maya" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "maya" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Houdini(func=None):
    if func == None:
        return __import__("hou")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __import__("hou"):
            return func(*args, **kwargs)

    return wrapper


def Unreal(func=None):
    if func == None:
        return "UE4" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "UE4" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Unity(func=None):
    if func == None:
        return

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "UE4" in sys.executable:
            return func(*args, **kwargs)

    return wrapper



def Blender(func=None):
    if func == None:
        return "blender" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "blender" in sys.executable:
            return func(*args, **kwargs)

    return wrapper


def Max(func=None):
    if func == None:
        return "3dsmax" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "3dsmax" in sys.executable:
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
    return False


def _Maya():
    """find Maya app"""
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Autodesk/Maya2017",
        "Darwin": "/Applications/Autodesk/maya2017/Maya.app/Contents",
    }
    return os.environ.get("MAYA_LOCATION") or d[platform.system()]


def _Houdini():
    """find Houdini app"""
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Side Effects Software/Houdini 16.5.323/bin",
        "Darwin": "/Applications/Houdini/Houdini16.5.473/Houdini.app/Contents",
    }
    return os.environ.get("HIP") or d[platform.system()]


def _Max():
    """find 3dsMax app"""
    return os.environ.get("ADSK_3DSMAX_X64_2018") or "C:/Program Files/Autodesk/3ds Max 2018"


def _Blender():
    """find Blender app"""
    d = {
        "Linux": "",
        "Windows": "C:/Program Files/Blender Foundation/Blender",
        "Darwin": "/Applications/Blender/blender.app/Contents/MacOS/blender"
    }
    return d[platform.system()]


def _Unreal():
    d = {
        "Linux": "",
        "Windows": "C:/Program Files/Epic Games/UE_4.20/Engine/Binaries/Win64",
        "Darwin": ""
    }
    return d[platform.system()]


MayaBin = _Maya()
HoudiniBin = _Houdini()
BlenderBin = _Blender()

__all__ = [
    "Windows", "Linux", "MacOS",
    "Maya", "Houdini", "Blender",
    "MayaBin", "HoudiniBin", "BlenderBin"
]
