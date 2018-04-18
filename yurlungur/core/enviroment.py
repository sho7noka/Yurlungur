# -*- coding: utf-8 -*-
import os
import sys
import platform
import functools


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
        return True
    except ImportError:
        return False


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
        return "houdini" in sys.executable or "hindie" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "houdini" in sys.executable or "hindie" in sys.executable:
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


def installed(app):
    if app == "maya":
        return os.path.getsize(_Maya())
    if app == "houdini":
        return os.path.getsize(_Houdini())
    if app == "unreal":
        return os.path.getsize(_Unreal())
    if app == "blender":
        return os.path.getsize(_Blender())
    if app == "max":
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
        "Darwin": "/Applications/houdini/Houdini.app/Contents",
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
        "Windows": "C:/Program Files/Epic Games/UE_4.19/Engine/Binaries/Win64",
        "Darwin": ""
    }
    return d[platform.system()]


MayaBin = _Maya()
HoudiniBin = _Houdini()
UnrealBin = _Unreal()

__all__ = [
    "Windows", "Linux", "MacOS",
    "Maya", "Houdini", "Unreal",
    "MayaBin", "HoudiniBin", "UnrealBin"
]
