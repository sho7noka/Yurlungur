# -*- coding: utf-8 -*-
from yurlungur.core import env
from yurlungur.tool.meta import meta
from yurlungur.core.proxy import YObject, YNode, YFile

file = cmd = object


class Command(object):
    @staticmethod
    def register(func):
        pass

    @staticmethod
    def unregister(func):
        pass

    @classmethod
    def list(cls):
        return [obj for obj in dir(cls) if not obj.startswith("_")]


def _ls(cls, *args, **kwargs):
    gen = meta.ls(*args, **kwargs) if hasattr(meta, "ls") else meta.pwd().allItems()
    return tuple(YNode(obj) for obj in gen)


def _rm(cls, *args):
    for obj in args:
        YNode(obj).delete()


def _glob(cls, *args, **kwargs):
    gen = meta.ls(*args, **kwargs) if hasattr(meta, "ls") else meta.pwd().glob(*args, **kwargs)
    return tuple(YNode(obj) for obj in gen)


def _select(cls, *args, **kwargs):
    if hasattr(meta, "select"):
        meta.select(*args, **kwargs)
    
    if hasattr(meta, "root"):
        for node in meta.nodes(args):
            node.setSelected(True, **kwargs)


def _alembicImporter(cls, *args, **kwargs):
    """
    >>> f = YFile()
    >>> YFile.new_method = new_method
    >>> print f.new_method("new")
    """
    if hasattr(meta, "AbcImport"):
        return cls(meta.AbcImport(*args, **kwargs))

    if hasattr(meta, "root"):
        geo = yr.YNode("obj").create("geo")
        abc = geo.create("alembic")
        abc.fileName.set(*args)
        return cls(*args)


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
    Command.glob = _glob
    Command.select = _select

if env.Houdini():
    file = YFile()
    YFile.abcImporter = _alembicImporter
    YFile.fbxImporter = _fbxImporter

    cmd = Command()
    Command.ls = _ls
    Command.rm = _rm
    Command.glob = _glob
    Command.select = _select

if env.Unreal():
    file = YFile()
    YFile.abcImporter = _alembicImporter
    YFile.fbxImporter = _fbxImporter

    cmd = Command()

__all__ = ["file", "cmd", "Command"]
