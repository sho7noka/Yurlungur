# -*- coding: utf-8 -*-
from proxy import *
import enviroment as env


def ls(self):
    print "_ls"
    return


def glob(self):
    return


def cd(self):
    return


def root(self):
    return


def pwd(self):
    return


def select(self, *args):
    return


def _alembicImporter(self, *args, **kwargs):
    """
    >>> f = YFile()
    >>> YFile.new_method = new_method
    >>> print f.new_method("new")
    """
    if hasattr(meta, "AbcImport"):
        return meta.AbcImport(*args, **kwargs)


def _alembicExporter(self, *args, **kwargs):
    if hasattr(meta, "AbcExport"):
        return meta.AbcExport(*args, **kwargs)



def _fbxImporter(self, *args, **kwargs):
    pass


def _fbxExporter(self, *args, **kwargs):
    import maya.mel; mel.eval("FBXExportInAscii -v true; FBXExport -f \"{}\" -s;".format(*args))


# Monkey-Patch
if env.Maya():
    # for plugin in ["fbxmaya.mll", "AbcImport.mll", "AbcExport.mll"]:
    #     meta.loadPlugin(plugin, qt=1)

    abc = YFile("aaa")
    YFile.importer = _alembicImporter
    YFile.exporter = _alembicExporter

    fbx = YFile("bbb")
    YFile.importer = _fbxImporter
    YFile.exporter = _fbxExporter

if env.Houdini():
    abc = YFile("aaa")
    YFile.importer = _alembicImporter
    YFile.exporter = _alembicExporter

if env.Unreal():
    abc = YFile("aaa")
    YFile.importer = _alembicImporter

    fbx = YFile("bbb")
    YFile.importer = _fbxImporter
