# -*- coding: utf-8 -*-
from ..qtutil import *

application = QCoreApplication.applicationName().lower()

if "maya" in application:
    from maya import cmds, mel, OpenMaya

    application = cmds

elif "houdini" in application:
    import hou

    application = hou

elif "max" in application:
    import pymxs

    on = True
    off = False
    application = pymxs

else:
    import standalone

    application = standalone

#
try:
    import bpy

    application = "bpy"
except:
    pass

try:
    # import
    application = arnold
except:
    pass

try:
    import pysbs

    application = pysbs
except:
    pass

try:
    import c4d

    application = c4d
except:
    pass
