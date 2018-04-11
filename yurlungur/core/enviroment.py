# -*- coding: utf-8 -*-
import os
import sys
import platform
import functools


def Windows(func=None):
    if func == None:
        return platform.system() == "Windows"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Windows":
            func(*args, **kwargs)
    return wrapper


def Linux(func=None):
    if func == None:
        return platform.system() == "Linux"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Linux":
            func(*args, **kwargs)
    return wrapper


def MacOS(func=None):
    if func == None:
        return platform.system() == "Darwin"

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() == "Darwin":
            func(*args, **kwargs)
    return wrapper


def Maya(func=None):
    if func == None:
        return "maya" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "maya" in sys.executable:
            func(*args, **kwargs)

    return wrapper


def Houdini(func=None):
    if func == None:
        return "houdini" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "houdini" in sys.executable:
            func(*args, **kwargs)

    return wrapper


def Unreal(func=functools.wraps):
    if func == None:
        return "UE4" in sys.executable

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if "UE4" in sys.executable and func != None:
            func(*args, **kwargs)
        return "UE4" in sys.executable

    return wrapper


def _Maya():
    """find Maya app"""
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Autodesk/Maya2017",
        "Darwin": "/Applications/Autodesk/maya2017/Maya.app/Contents",
    }
    maya = os.environ.get("MAYA_LOCATION") or d[platform.system()]
    assert os.path.getsize(maya)
    return maya


def _Houdini():
    """find Houdini app"""
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Side Effects Software",
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