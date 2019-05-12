# -*- coding: utf-8 -*-
import yurlungur
from yurlungur.core import app, env


class YException(NotImplementedError):
    """
    >>> raise NotImplementedError(app.application)
    """
    pass


class YMObject(object):
    """command wrapper for any application"""

    if env.Substance():
        from yurlungur.adapters import substance as sd
        graph = sd.graph
        manager = sd.manager

    if env.Davinci():
        resolve = env.__import__("DaVinciResolveScript").scriptapp("Resolve")
        if resolve:
            manager = resolve.GetProjectManager()
            fusion = resolve.Fusion()

    if env.Unreal():
        from yurlungur.adapters import ue4
        editor = ue4.EditorUtil()
        assets = ue4.GetEditorAssetLibrary()
        levels = ue4.GetEditorLevelLibrary()
        tools = ue4.tools

    def __getattr__(self, item):
        try:
            from inspect import getmembers
        except ImportError:
            setattr(yurlungur, item, getattr(app.application, item))
            return getattr(app.application, item)

        for cmd, _ in getmembers(app.application):
            if cmd == item:
                setattr(
                    yurlungur, cmd,
                    (lambda str: dict(getmembers(app.application))[str])(cmd)
                )
                return getattr(yurlungur, item)

        # TODO self.eval(item)
        return getattr(yurlungur, item, False)

    def eval(self, script):
        if env.Maya():
            import maya.mel as mel
            return mel.eval(script)
        if env.Houdini():
            return app.application.hscript(script)
        if env.Max():
            import MaxPlus
            return MaxPlus.Core.EvalMAXScript(script)
        if env.Davinci() and self.resolve:
            self.fusion.GetCurrentComp().Execute(script)
        if env.Photoshop():
            return app.application.DoJavascript(script)

        raise YException

    @property
    def module(self):
        return app.application


class MetaObject(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaObject, cls).__new__(cls, name, bases, attrs)


class MetaAttr(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaAttr, cls).__new__(cls, name, bases, attrs)


# Dynamic Class
_YObject = MetaObject("YObject", (object,), {"__doc__": MetaObject.__doc__})
_YAttr = MetaAttr("YAttr", (object,), {"__doc__": MetaAttr.__doc__})
_YVector = _YMatrix = _YColor = OM = object

if env.Maya():
    import maya.api.OpenMaya as OM

    _YVector = type('_YVector', (OM.MVector,), dict())
    _YMatrix = type('_YMatrix', (OM.MMatrix,), dict())
    _YColor = type('_YColor', (OM.MColor,), dict())

    meta = YMObject()
    if hasattr(meta, "loadPlugin"):
        for plugin in "fbxmaya.mll", "AbcImport.mll", "AbcExport.mll":
            meta.loadPlugin(plugin, qt=1)

elif env.Houdini() or env.Unreal():
    meta = YMObject()

    _YVector = type('_YVector', (
        meta.Vector if hasattr(meta, "Vector") else meta.Vector3,
    ), dict())

    _YMatrix = type('_YMatrix', (
        meta.Matrix if hasattr(meta, "Matrix") else meta.Matrix4,
    ), dict())

    _YColor = type('_YColor', (meta.Color,), dict())

elif env.Blender():
    import mathutils

    _YVector = type('_YVector', (mathutils.Vector,), dict())
    _YMatrix = type('_YMatrix', (mathutils.Matrix,), dict())
    _YColor = type('_YColor', (mathutils.Color,), dict())

elif env.Substance():
    meta = YMObject()

    # _YVector = type('_YVector', (meta.SDValueVector,), dict())
    # _YMatrix = type('_YMatrix', (meta.SDValueMatrix,), dict())
    # _YColor = type('_YColor', (meta.SDValueColorRGBA,), dict())

elif env.Nuke():
    import _nukemath

    _YVector = type('_YVector', (_nukemath.Vector3,), dict())
    _YMatrix = type('_YMatrix', (_nukemath.Matrix4,), dict())

elif env.Max():
    import MaxPlus

    _YVector = type('_YVector', (MaxPlus.Point3,), dict())
    _YMatrix = type('_YMatrix', (MaxPlus.Matrix3,), dict())
    _YColor = type('_YColor', (MaxPlus.Color,), dict())
