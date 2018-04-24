# -*- coding: utf-8 -*-
from yurlungur.core import env
from yurlungur.tool.meta import meta
from yurlungur.core.proxy import YObject, YNode, YFile

__all__ = ["file", "cmd", "Command"]

file = cmd = object


class Command(object):
    @staticmethod
    def register(func):
        pass

    @staticmethod
    def remove(func):
        pass

    @staticmethod
    def list(cls):
        pass


def _ls(cls, *args, **kwargs):
    gen = meta.ls(*args, **kwargs) if hasattr(meta, "ls") else meta.root.allItems()
    return tuple(YNode(obj) for obj in gen)


def _rm(cls, *args):
    for obj in args:
        YNode(obj).delete()


def _glob(cls):
    return


def _cd(cls):
    return


def _root(cls):
    return


def _pwd(cls):
    return


def _parent(cls, *args, **kwargs):
    return


def _children(cls, *args, **kwargs):
    return


def _select(cls, *args):
    return


def _alembicImporter(cls, *args, **kwargs):
    """
    >>> f = YFile()
    >>> YFile.new_method = new_method
    >>> print f.new_method("new")
    """
    if hasattr(meta, "AbcImport"):
        return cls(meta.AbcImport(*args, **kwargs))


def _alembicExporter(cls, *args, **kwargs):
    if hasattr(meta, "AbcExport"):
        return cls(meta.AbcExport(*args, **kwargs))


def _fbxImporter(cls, *args, **kwargs):
    if hasattr(meta, "importFBX"):
        return meta.importFBX(*args, **kwargs)
    else:
        return cls(mel.eval("FBXImport -file {0};".format(*args)))


def _fbxExporter(cls, *args, **kwargs):
    return cls(mel.eval("FBXExportInAscii -v true; FBXExport -f \"{}\" -s;".format(*args)))


# Monkey-Patch
if env.Maya():
    import maya.mel

    for plugin in ["fbxmaya.mll", "AbcImport.mll", "AbcExport.mll"]:
        meta.loadPlugin(plugin, qt=1)

    file = YFile()
    YFile.abcImporter = _alembicImporter
    YFile.abcExporter = _alembicExporter
    YFile.fbxImporter = _fbxImporter
    YFile.fbxExporter = _fbxExporter

    cmd = Command()
    Command.ls = _ls
    Command.rm = _rm

if env.Houdini():
    file = YFile()
    YFile.fbxImporter = _fbxImporter

    cmd = Command()
    Command.ls = _ls
    Command.rm = _rm

if env.Unreal():
    file = YFile()
    YFile.abcImporter = _alembicImporter
    YFile.fbxImporter = _fbxImporter

    cmd = Command()
