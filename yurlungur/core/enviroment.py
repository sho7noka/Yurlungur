# -*- coding: utf-8 -*-
import os
import platform

__all__ = [
    "Windows", "Linux", "MacOS",
    "Maya", "Houdini", "Max",
]


def Windows():
    return platform.system() == "Windows"


def Linux():
    return platform.system() == "Linux"


def MacOS():
    return platform.system() == "Darwin"


def _Maya():
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Autodesk/Maya2017",
        "Darwin": "/Applications/Autodesk/maya2017/Maya.app/Contents",
    }
    return os.environ.get("MAYA_LOCATION") or d[platform.system()]


def _Houdini():
    d = {
        "Linux": "/usr/autodesk/maya2017-x64",
        "Windows": "C:/Program Files/Side Effects Software",
        "Darwin": "/Applications/Side Effects Software/maya2017/Houdini.app/Contents",
    }
    return os.environ.get("HIP") or d[platform.system()]


def _Max():
    return os.environ.get("ADSK_3DSMAX_X64_2018") or "C:/Program Files/Autodesk/3ds Max 2018"


Maya = _Maya()
Houdini = _Houdini()
Max = _Max()