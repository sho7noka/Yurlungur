# -*- coding: utf-8 -*-
import sys
from yurlungur.core.env import __import__


def exApplication(module=""):
    if module == "photoshop":
        from yurlungur.adapters import photoshop

        application = photoshop.app

    elif __import__(module):
        application = __import__(module)

    else:
        from yurlungur.tool import standalone

        application = standalone

    return application


application = sys.executable

if "maya" in application:
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif "3dsmax" in application:
    import pymxs

    application = pymxs

elif "blender" in application:
    import bpy

    application = bpy

elif "Substance" in application:
    import sd.api as sdapi

    application = sdapi

elif "MarvelousDesigner" in application:
    from MarvelousDesigner import MarvelousDesigner

    application = MarvelousDesigner()
    application.initialize()

elif "UE4Editor" in application:
    import unreal

    application = unreal

elif "Nuke" in application:
    import nuke

    application = nuke

elif __import__("DaVinciResolveScript"):
    import DaVinciResolveScript

    application = DaVinciResolveScript

else:
    import platform

    if platform.python_implementation() == "IronPython":
        import clr

        clr.AddReferenceByPartialName("UnityEngine")
        import UnityEngine

        application = UnityEngine
    else:
        application = exApplication("photoshop")

__all__ = ["application", "exApplication"]


class YException(NotImplementedError):
    """
    >>> raise NotImplementedError(application)
    """
    pass
