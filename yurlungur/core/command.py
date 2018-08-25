# -*- coding: utf-8 -*-
from yurlungur.core import env
from yurlungur.core.proxy import YNode, YFile
from yurlungur.tool.meta import meta

__all__ = ["file", "cmd", "UndoGroup"]


class UndoGroup(object):
    def __init__(self, label):
        self.label = label

    def __enter__(self):
        if env.Maya():
            meta.undoInfo(ock=1)
            return self
        elif env.Blender():
            self.undo = meta.context.user_preferences.edit.use_global_undo
            meta.context.user_preferences.edit.use_global_undo = False

    def __exit__(self, exc_type, exc_value, traceback):
        if env.Maya():
            meta.undoInfo(cck=1)
        elif env.Blender():
            meta.context.user_preferences.edit.use_global_undo = self.undo


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
        return cls(meta.eval("FBXImport -file {0};".format(*args)))


def _fbxExporter(cls, *args, **kwargs):
    return cls(meta.eval("FBXExportInAscii -v true; FBXExport -f \"{}\" -s;".format(*args)))


file = YFile()
cmd = Command()

# Monkey-Patch
if env.Maya():
    for plugin in "fbxmaya.mll", "AbcImport.mll", "AbcExport.mll":
        meta.loadPlugin(plugin, qt=1)

    YFile.abcImporter = _alembicImporter
    YFile.abcExporter = _alembicExporter
    YFile.fbxImporter = _fbxImporter
    YFile.fbxExporter = _fbxExporter

    Command.ls = _ls
    Command.rm = _rm
    Command.glob = _glob
    Command.select = _select

if env.Houdini():
    UndoGroup = meta.undos.group

    YFile.abcImporter = _alembicImporter
    YFile.fbxImporter = _fbxImporter

    Command.ls = _ls
    Command.rm = _rm
    Command.glob = _glob
    Command.select = _select

if env.Blender():
    YFile.abcImporter = _alembicImporter
    YFile.fbxImporter = _fbxImporter

if env.Unreal():
    UndoGroup = meta.ScopedEditorTransaction
