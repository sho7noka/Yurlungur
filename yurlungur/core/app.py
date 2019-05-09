# -*- coding: utf-8 -*-
import sys
from yurlungur.core.env import __import__

application = sys.executable


def exApplication(module=""):
    if module == "photoshop":
        if not __import__("comtypes"):
            import pip
            if getattr(pip, 'main', False):
                pip.main(['install', "comtypes"])
            else:
                from pip import _internal
                _internal.main(['install', "comtypes"])

        from comtypes.client import GetActiveObject, CreateObject
        try:
            application = GetActiveObject('Photoshop.Application')
        except WindowsError:
            application = CreateObject("Photoshop.Application")

    elif __import__(module):
        application = __import__(module)
    else:
        from yurlungur.tool import standalone
        application = standalone

    return application


if "maya" in application:
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif "Substance" in application:
    import sd.api as sdapi

    application = sdapi

elif "MarvelousDesigner" in application:
    from MarvelousDesigner import MarvelousDesigner

    application = MarvelousDesigner()

elif "3dsmax" in application:
    import pymxs

    application = pymxs

elif "blender" in application:
    import bpy

    application = bpy

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

    if platform.python_implementation() == 'IronPython':
        import clr
        clr.AddReferenceByPartialName('UnityEngine')
        import UnityEngine

        application = UnityEngine
    else:
        if platform.system() != "Windows":
            assert "Sorry, macOS is not availabale."
        application = exApplication("photoshop")

__all__ = ["application", "exApplication"]
