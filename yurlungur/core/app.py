# -*- coding: utf-8 -*-
import sys
from yurlungur.core.env import __import__

application = sys.executable

if "maya" in application:
    import maya.cmds as cmds

    application = cmds

elif __import__("hou"):
    import hou

    application = hou

elif "Substance" in application:
    import sd.api as sdapi

    application = sdapi

elif "3dsmax" in application:
    import pymxs

    application = pymxs

elif "UE4Editor" in application:
    import unreal

    application = unreal

elif "Nuke" in application:
    import nuke

    application = nuke

elif "Cinema 4D" in application:
    import c4d

    application = c4d

elif "Blender" in application:
    import bpy

    application = bpy

elif "MarvelousDesigner" in application:
    import MarvelousDesigner.MarvelousDesigner

    application = MarvelousDesigner.MarvelousDesigner()
    application.initialize()

else:
    from yurlungur.tool import standalone

    application = standalone


class YException(NotImplementedError):
    """
    >>> raise NotImplementedError(application)
    """
    pass
