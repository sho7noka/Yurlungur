# -*- coding: utf-8 -*-
import yurlungur
from yurlungur.core.app import application
from yurlungur.core import env


class MultiObject(object):
    """
    command wrapper for any application
    """
    if env.Photoshop():
        from yurlungur.adapters import photoshop as ps
        doc = ps.Document()._doc

    if env.Unreal():
        from yurlungur.adapters import unreal
        editor = unreal.EditorUtil()
        assets = unreal.GetEditorAssetLibrary()
        levels = unreal.GetEditorLevelLibrary()
        tools = unreal.tools

    if env.Substance():
        from yurlungur.adapters import substance_designer as sd
        graph = sd.graph
        manager = sd.manager

    if env.C4D():
        doc = application.documents.GetActiveDocument()

    if env.Davinci():
        resolve = env.__import__("DaVinciResolveScript").scriptapp("Resolve")
        if resolve:
            fusion = resolve.Fusion()

            v = resolve.GetVersion()
            if v[0] >= 17 and v[1] >= 2:
                is_fusion = resolve.GetCurrentPage() == "fusion"
            else:
                is_fusion = not fusion.CurrentComp is None
            del v

            if not is_fusion:
                from yurlungur.adapters import davinci

    def __getattr__(self, item):
        try:
            from inspect import getmembers

        except ImportError:
            setattr(yurlungur, item, getattr(application, item))
            return getattr(application, item)

        for cmd, _ in getmembers(application):
            if cmd == item:
                setattr(
                    yurlungur, cmd,
                    (lambda str: dict(getmembers(application))[str])(cmd)
                )
                return getattr(yurlungur, item)

        return getattr(yurlungur, item, False)

    def eval(self, script):
        """
        eval script for
        mel, hscript, tcl, lua, unreal command, unity C#, mxs, substance js and photoshop jsx.

        Args:
            script:

        Returns:

        """
        if env.Maya():
            import maya.mel as mel
            return mel.eval(script)

        if env.Houdini():
            return application.hscript(script)

        if env.Nuke():
            return application.tcl(script)

        if env.Davinci() and self.resolve:
            return self.fusion.Execute(script)

        if env.Unreal():
            from yurlungur.adapters import unreal
            return unreal.execute_console_command(script)

        if env.Max():
            return application.runtime.execute(script)

        if env.Painter():
            return application.js.evaluate(script)

        if env.Photoshop():
            return application.DoJavascript(script)

        if env.Modo():
            import lx
            return lx.eval(script)

    @property
    def module(self):
        return application


class MetaObject(type):
    """"""
    __doc__ = """
    base class
    """

    def __new__(cls, name, bases, attrs):
        return super(MetaObject, cls).__new__(cls, name, bases, attrs)

    @staticmethod
    def add(self):
        pass

    @staticmethod
    def rmv(self):
        pass


# Dynamic Class
YObject = MetaObject("YObject", (object,),
                     {"__doc__": MetaObject.__doc__,
                      "add": MetaObject.add, "rmv": MetaObject.rmv})


class BaseActor(object):
    """flat"""
    def instantiate(self):
        pass

    def destroy(self):
        pass

    def id(self):
        pass

    # transform
    # component


class BaseNLE(object):
    """hierarchy"""
    def index(self):
        pass

    def duration(self):
        pass

    def render(self):
        pass

    # track


class BaseNode(object):
    """
    parent children inout
    """
    def parent(self):
        pass

    def connect(self):
        pass

    def input(self):
        pass

    # attribute