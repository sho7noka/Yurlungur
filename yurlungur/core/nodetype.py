# -*- coding: utf-8 -*-
import ctypes
import fnmatch
import inspect

from yurlungur.core import env
from yurlungur.core.proxy import YNode
from yurlungur.tool.meta import meta


class _NodeType(object):
    def __getattr__(self, item):
        if hasattr(meta, "types"):
            nodes = fnmatch.filter(dir(meta.types), str(item))
        else:
            nodes = self.findNodes(item)

        for node in nodes:
            setattr(self, str(item), YNode(node))

        return YNode(item)

    def findNodes(self, pattern):
        if hasattr(meta, "listNodeTypes"):
            # http://help.autodesk.com/cloudhelp/2016/JPN/Maya-Tech-Docs/CommandsPython/shadingNode.html
            categories = [
                "geometry", "camera", "light", "utility",
                "color", "shader", "texture", "rendering", "postprocess"
            ]
            # meta.allNodeTypes(ia=1)
            for category in categories:
                yield fnmatch.filter(meta.listNodeTypes(category), pattern)

        if hasattr(meta, "nodeTypes"):
            for category in meta.nodeTypeCategories().keys():
                yield fnmatch.filter(
                    meta.nodeTypeCategories()[category].nodeTypes().keys(),
                    pattern
                )


class OpenGL(object):
    """openGL wrapper"""

    def __getattr__(self, item):
        def _getGL(mod):
            for cmd, _ in inspect.getmembers(mod):
                if fnmatch.fnmatch(item, "".join(["*", cmd])):
                    setattr(
                        self, cmd,
                        (lambda str: dict(inspect.getmembers(mod))[str])(cmd)
                    )
                    return getattr(self, item)

        _tmp = []

        if env.Maya():
            from maya import OpenMayaRender as _mgl
            _tmp.extend(_mgl, _mgl.MHardwareRenderer.theRenderer().glFunctionTable())

        if env.Blender():
            import bgl
            _tmp.extend(bgl)

        for gl in _tmp:
            if _getGL(gl):
                return _getGL(gl)

        try:
            from OpenGL import GL as gl
            return gl
        except ImportError:
            return ctypes.cdll.OpenGL32


YType = _NodeType()
