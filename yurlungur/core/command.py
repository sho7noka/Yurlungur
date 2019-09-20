# -*- coding: utf-8 -*-

try:
    from functools import partial
except ImportError:
    pass

from yurlungur.core.proxy import YNode, YFile
from yurlungur.tool.meta import meta
from yurlungur.core.app import YException

__all__ = ["file", "cmd"]


class Command(object):
    """plugin system"""
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

    if hasattr(meta, "hda"):
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

    if hasattr(meta, "hda"):
        geo = yr.YNode("obj").create("geo")
        abc = geo.create("alembic")
        abc.fileName.set(*args)
        return cls(*args)

    if hasattr(meta, "runtime"):
        importer = partial(meta.runtime.importFile, args[0], meta.runtime.Name("noPrompt"), using='AlembicImport')
        if importer(**kwargs):
            return args[0]

    if hasattr(meta, 'uclass'):
        data = unreal.AutomatedAssetImportData()
        data.set_editor_property('filenames', *args)
        for k, v in kwargs:
            data.set_editor_property(k, v)
        meta.tools.import_assets_automated(data)

    raise YException


def _alembicExporter(cls, *args, **kwargs):
    if hasattr(meta, "AbcExport"):
        return cls(meta.AbcExport(*args, **kwargs))

    if hasattr(meta, "runtime"):
        export = partial(meta.runtime.exportFile, args[0], meta.runtime.Name("noPrompt"), using='AlembicExport')
        if export(**kwargs):
            return args[0]

    raise YException


def _fbxImporter(cls, *args, **kwargs):
    if hasattr(meta, "importFBX"):
        return meta.importFBX(*args, **kwargs)

    if hasattr(meta, "runtime"):
        importer = partial(meta.runtime.importFile, args[0], meta.runtime.Name("noPrompt"), using='FBXIMPORTER')
        if importer(**kwargs):
            return args[0]

    if hasattr(meta, 'uclass'):
        data = unreal.AutomatedAssetImportData()
        data.set_editor_property('filenames', *args)
        for k, v in kwargs:
            data.set_editor_property(k, v)
        factory = unreal.FbxSceneImportFactory()
        data.set_editor_property('factory', factory)

        meta.tools.import_assets_automated(data)

    if hasattr(meta, 'eval'):
        return cls(meta.eval("FBXImport -file {0};".format(*args)))

    raise YException


def _fbxExporter(cls, *args, **kwargs):
    if hasattr(meta, "runtime"):
        export = partial(meta.runtime.exportFile, args[0], meta.runtime.Name("noPrompt"), using='FBXEXPORTER')
        if export(**kwargs):
            return args[0]

    if hasattr(meta, 'eval'):
        return cls(meta.eval("FBXExportInAscii -v true; FBXExport -f \"{}\" -s;".format(*args)))

    raise YException


def _gltfImporter(cls, *args, **kwargs):
    pass


def _gltfExporter(cls, *args, **kwargs):
    pass


def _usdImporter(cls, *args, **kwargs):
    pass


def _usdExporter(cls, *args, **kwargs):
    pass


# Monkey-Patch
file = YFile()
YFile.abcImporter = _alembicImporter
YFile.abcExporter = _alembicExporter
YFile.fbxImporter = _fbxImporter
YFile.fbxExporter = _fbxExporter
# YFile.gltfImporter = _gltfImporter
# YFile.gltfExporter = _gltfExporter
# YFile.usdImporter = _usdImporter
# YFile.usdExporter = _usdExporter

cmd = Command()
Command.ls = _ls
Command.rm = _rm
Command.glob = _glob
Command.select = _select
