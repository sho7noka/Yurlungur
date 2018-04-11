# -*- coding: utf-8 -*-
from proxy import *
import enviroment as env


class Command(object):
    @staticmethod
    def register(func):
        pass

    @staticmethod
    def remove(func):
        pass


def _ls(cls):
    return meta.ls()


def _rm(cls):
    return


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
    pass


def _fbxExporter(cls, *args, **kwargs):
    import maya.mel
    return cls(mel.eval("FBXExportInAscii -v true; FBXExport -f \"{}\" -s;".format(*args)))


# Monkey-Patch
if env.Maya():
    try:
        for plugin in ["fbxmaya.mll", "AbcImport.mll", "AbcExport.mll"]:
            meta.loadPlugin(plugin, qt=1)
    except:
        pass

    file = YFile()
    YFile.abcImporter = _alembicImporter
    YFile.abcExporter = _alembicExporter
    YFile.fbxImporter = _fbxImporter
    YFile.fbxExporter = _fbxExporter

    cmd = Command()
    Command.ls = _ls
    Command.pwd = _pwd

if env.Houdini():
    file = YFile()
    YFile.abcImporter = _alembicImporter
    YFile.abcExporter = _alembicExporter

if env.Unreal():
    file = YFile()
    YFile.abcImporter = _alembicImporter
    YFile.fbxImporter = _fbxImporter

__all__ = ["file", "cmd", "Command"]
