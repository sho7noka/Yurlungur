# -*- coding: utf-8 -*-
from yurlungur.core.app import application
from yurlungur.core.proxy import YNode, YAttr
from yurlungur.tool.math import YVector, YMatrix, YColor
from yurlungur.core.enviroment import Maya, Houdini, Unreal

if Maya():
    from yurlungur.core.wrapper import OM


class Builder(object):
    """
    http://help.autodesk.com/view/MAYAUL/2017/JPN/?guid=__py_ref_class_open_maya_1_1_m_fn_mesh_html
    http://www.sidefx.com/docs/houdini/hom/hou/Geometry.html
    """

    def geometry(self):
        if Maya():
            dag = OM.MGlobal.getSelectionListByName("polySurfaceShape1").getDagPath(0)
            mesh = OM.MFnMesh(dag)
        elif Houdini():
            mesh = hou.node("polySurfaceShape1").geometry()

        return YNode

    def camera(self):
        if Maya():
            obj = OM.MGlobal.getSelectionListByName("cameraShape1").getDagPath(0)
            camera = OM.MFnCamera(obj)

        return YAttr


class Shader(object):
    def material(self):
        pass

    def light(self):
        pass

    def texture(self):
        pass
