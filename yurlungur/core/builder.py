# -*- coding: utf-8 -*-
from yurlungur.core.app import application
from yurlungur.core.proxy import YNode, YAttr
from yurlungur.tool.math import YVector, YMatrix, YColor
from yurlungur.core.env import Maya, Houdini, Unreal
from yurlungur.core.wrapper import OM


class Builder(object):
    """
    http://help.autodesk.com/view/MAYAUL/2017/JPN/?guid=__py_ref_class_open_maya_1_1_m_fn_mesh_html
    http://www.sidefx.com/docs/houdini/hom/hou/Geometry.html
    """

    def geometry(self):
        pass

    def camera(self):
        pass

    def light(self):
        pass


class Shader(object):
    def material(self):
        pass

    def texture(self):
        pass

    def renderer(self):
        pass
