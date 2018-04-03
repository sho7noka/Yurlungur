# -*- coding: utf-8 -*-
import os
import platform
import functools

__all__ = [
    "Windows", "Linux", "MacOS",
    "Maya", "Houdini", "Max", "Blender"
]


def Windows():
    return platform.system() == "Windows"


def Linux():
    return platform.system() == "Linux"


def MacOS():
    return platform.system() == "Darwin"


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
        "Linux" : "" ,
        "Windows" : "C:/Program Files/Blender Foundation/Blender",
        "Darwin" : "/Applications/Blender/blender.app/Contents/MacOS/blender"
    }
    return d[platform.system()]


Maya = _Maya()
Houdini = _Houdini()
Max = _Max()
Blender = _Blender()