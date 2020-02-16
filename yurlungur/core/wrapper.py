# -*- coding: utf-8 -*-
import yurlungur
from yurlungur.core import app, env


class MetaObject(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaObject, cls).__new__(cls, name, bases, attrs)


class MetaAttr(type):
    def __new__(cls, name, bases, attrs):
        return super(MetaAttr, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def add(self):
        pass

    @staticmethod
    def rmv(self):
        pass


class YMObject(object):
    """command wrapper for any application"""

    if env.Photoshop():
        from yurlungur.adapters import photoshop as ps
        doc = ps.Document()._doc

    if env.UE4():
        from yurlungur.adapters import ue4
        editor = ue4.EditorUtil()
        assets = ue4.GetEditorAssetLibrary()
        levels = ue4.GetEditorLevelLibrary()
        tools = ue4.tools

    if env.Unity():
        from yurlungur.adapters import unity
        editor = unity.UnityEditor
        engine = unity.UnityEngine

    if env.Substance():
        from yurlungur.adapters import substance as sd
        graph = sd.graph
        manager = sd.manager

    if env.C4D():
        doc = app.application.documents.GetActiveDocument()

    if env.Davinci():
        resolve = env.__import__("DaVinciResolveScript").scriptapp("Resolve")
        if resolve:
            fusion = resolve.Fusion()
            manager = resolve.GetProjectManager()

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

        return getattr(yurlungur, item, False)

    @property
    def module(self):
        return app.application

    def eval(self, script):
        if env.Maya():
            import maya.mel as mel
            return mel.eval(script)

        if env.Photoshop():
            return app.application.DoJavascript(script)

        if env.Houdini():
            return app.application.hscript(script)

        if env.Max():
            import MaxPlus
            return MaxPlus.Core.EvalMAXScript(script)

        if env.Davinci() and self.resolve:
            return self.fusion.GetCurrentComp().Execute(script)

        if env.Unity():
            from yurlungur.adapters import unity
            return unity.EvalScript(script)


# Dynamic Class
_YObject = MetaObject("YObject", (object,), {"__doc__": MetaObject.__doc__})
_YAttr = MetaAttr("YAttr", (object,), {"__doc__": MetaAttr.__doc__, "add": MetaAttr.add, "rmv": MetaAttr.rmv})
_YVector = _YMatrix = _YColors = OM = object

if env.Maya():
    import maya.api.OpenMaya as OM

    _YVector = type('_YVector', (OM.MVector,), dict())
    _YMatrix = type('_YMatrix', (OM.MMatrix,), dict())
    _YColors = type('_YColors', (OM.MColor,), dict())

    from yurlungur.tool.meta import meta

    if hasattr(meta, "loadPlugin"):
        for plugin in "fbxmaya.mll", "AbcImport.mll", "AbcExport.mll":
            meta.loadPlugin(plugin, qt=1)

elif env.Houdini() or env.UE4() or env.Unity():
    _YVector = type('_YVector', (
        app.application.Vector if hasattr(app.application, "Vector") else app.application.Vector3,
    ), dict())

    if env.Unity():
        pass
        # _YMatrix = type('_YMatrix', (app.application.Matrix4x4), dict())
    else:
        _YMatrix = type('_YMatrix', (
            app.application.Matrix if hasattr(app.application, "Matrix") else app.application.Matrix4,
        ), dict())

    _YColors = type('_YColors', (app.application.Color,), dict())

elif env.Substance():
    _YVector = type('_YVector', (app.application.SDValueVector,), dict())
    _YMatrix = type('_YMatrix', (app.application.SDValueMatrix,), dict())
    _YColors = type('_YColors', (app.application.SDValueColorRGBA,), dict())

elif env.Max():
    import MaxPlus

    _YVector = type('_YVector', (MaxPlus.Point3,), dict())
    _YMatrix = type('_YMatrix', (MaxPlus.Matrix3,), dict())
    _YColors = type('_YColors', (MaxPlus.Color,), dict())

elif env.Nuke():
    import _nukemath

    _YVector = type('_YVector', (_nukemath.Vector3,), dict())
    _YMatrix = type('_YMatrix', (_nukemath.Matrix4,), dict())

elif env.Blender():
    import mathutils

    _YVector = type('_YVector', (mathutils.Vector,), dict())
    _YMatrix = type('_YMatrix', (mathutils.Matrix,), dict())
    _YColors = type('_YColors', (mathutils.Color,), dict())
