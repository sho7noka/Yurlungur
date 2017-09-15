
import importlib

try:
    import maya.cmds as cmds
    import maya.mel as mel
    import OpenMaya as maya

except:
    print "Import error"

try:
    import pymxs
    import MaxPlus

except:
    print 1


import os

# os.path.join("").replace("\\", "/")

class Wrapper(object):
    def __init__(self):
        pass

    def setAttr(self, value):
        pass

    def eval(self, text):
        mel.eval(text)
        MaxPlus.Core.EvalMAXScript(text)
        # exec()