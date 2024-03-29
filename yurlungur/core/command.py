# -*- coding: utf-8 -*-
import fnmatch
import types
import importlib
from functools import partial, wraps

from yurlungur.core import vars
from yurlungur.core.proxy import Node, Attribute, File
from yurlungur.tool.meta import meta

__all__ = [
    "cmd", "node", "attr", "file", "vars"
]

u"""
node ベースのアプリだとコマンド化されずに
まとまったAPIで読み込みを行う必要があるので
ここでコマンドにしておく

runtimecommand 化
"""

_CMDS_ = {}


class Command(object):
    """
    >>> def pydef1():
    >>>     return True
    >>> Command.register(pydef1)
    >>> # or
    >>> @Command.register
    >>> def pydef2():
    >>>     return False
    >>> # result
    >>> yurlungur.cmd.pydef1()
    """

    def __getattr__(self, item):
        return _CMDS_[item]

    # @wraps(func)
    @staticmethod
    def register(func):
        p = partial(meta.eval, func)
        m = types.ModuleType(func)
        if _CMDS_.has_key(func):
            _CMDS_.update(func, p)  # cmd.func()
        else:
            _CMDS_.update(func, m)  # cmd.func

    @classmethod
    def list(cls):
        return [obj for obj in dir(cls) if not obj.startswith("_")]

    @staticmethod
    def unregister():
        _CMDS_.clear()

def _Bake(cls, *args, **kwargs):
    """"""

# Monkey-Patch for attribute
attr = Attribute()
Attribute.create = None
Attribute.delete = None


def _rm(cls, *args):
    for obj in args:
        try:
            node = cls(obj.name)
            node.delete()
        except:
            pass


def _ls(cls, *args, **kwargs):
    gen = []
    if getattr(meta, "SDNode", False):
        return
    if getattr(meta, "ls", False):
        gen = meta.ls(*args, **kwargs)
    if getattr(meta, "hda", False):
        gen = meta.pwd().allItems()
    if getattr(meta, "data", False):
        return
    if getattr(meta, "uclass", False):
        return
    if getattr(meta, "knob", False):
        return
    if getattr(meta, "C4DAtom", False):
        return
    if getattr(meta, "fusion", False):
        return
    if getattr(meta, "runtime", False):
        gen = meta.runtime.objects
    if getattr(meta, "doc", False):
        return
    if getattr(meta, "SceneObject", False):
        gen = meta.getAllObjects()
    if getattr(meta, "textureset", False):
        return
    return (cls(obj) for obj in gen)


def _glob(cls, *args, **kwargs):
    if getattr(meta, "SDNode", False):
        return
    if getattr(meta, "ls", False):
        gen = meta.ls(*args, **kwargs)
    if getattr(meta, "hda", False):
        gen = meta.pwd().glob(*args, **kwargs)
    if getattr(meta, "data", False):
        return
    if getattr(meta, "uclass", False):
        return
    if getattr(meta, "knob", False):
        return
    if getattr(meta, "C4DAtom", False):
        return
    if getattr(meta, "fusion", False):
        gen = meta.fusion.GetCurrentComp().GetToolList(*args)
    if getattr(meta, "runtime", False):
        gen = meta.runtime.objects
    if getattr(meta, "doc", False):
        return
    if getattr(meta, "SceneObject", False):
        return
    if getattr(meta, "textureset", False):
        return
    return tuple(cls(obj) for obj in gen)


def _select(cls, *args, **kwargs):
    if getattr(meta, "select", False):
        return (cls(obj) for obj in meta.ls(sl=True))

    if getattr(meta, "hda", False):
        return (cls(obj.path()) for obj in meta.selectedNodes(args))

    if getattr(meta, "SDNode", False):
        context = meta.sd_app.getUIMgr()
        return (
            cls(node.getDefinition().getLabel())
            for node in context.getCurrentGraphSelection()
        )

    if getattr(meta, "runtime", False):
        if meta.runtime.execute("$") == meta.runtime.execute("$selection", False):
            return (cls(obj.name) for obj in meta.runtime.execute("$ as array"))
        else:
            return cls(meta.runtime.execute("$"))

    if getattr(meta, "data", False):
        return (cls(obj.name) for obj in meta.context.selected_objects)

    if getattr(meta, "C4DAtom", False):
        if len(args) == 0 and len(kwargs) == 0:
            meta.doc.SetActiveObject(meta.doc.SearchObject(args[0]), meta.SELECTION_NEW)
        return meta.doc.GetActiveObject().GetName()

    if getattr(meta, "knob", False):
        return (cls(node.name) for node in meta.selectedNodes())

    if getattr(meta, "doc", False):
        try:
            return cls(meta.doc.ActiveLayer.name)
        except AttributeError:
            return cls(meta.doc.currentLayer().name())

    if getattr(meta, "uclass", False):
        return (
            cls(asset.get_name())
            for asset in meta.editor.get_selected_assets()
        )

    if getattr(meta, "Debug", False):
        return (cls(go.name) for go in meta.editor.Selection.gameObjects)

    if getattr(meta, "SceneObject", False):
        return (cls(obj.name) for obj in meta.getSelectedObjects())


def _usdImporter(*args, **kwargs):
    """
    Maya      Python3 / USD InOut / internal
    Houdini   Python3 / USD InOut / internal
    Designer  Python3 / USD In    / usdcore
    Blender   Python3 / USD InOut / internal
    Unreal    Python3 / USD InOut / internal
    Nuke      Python2 / USD In    /
    Davinci   Python3 / USD In    / usdcore
    Cinema4D  Python3 / USD InOut / 
    Marmoset  Python3 / USD InOut /
    Painter   Python3 / USD InOut /
    3dsMax    Python3 / USD InOut /
    Modo      Python2 / USD InOut /

    https://community.foundry.com/discuss/topic/153415/extend-active-scenegraph?mode=Post&postID=1205506
    """

    if getattr(meta, "mayaUSDImport", False):
        meta.loadPlugin('mayaUsdPlugin', qt=True)
        meta.mayaUSDImport(file=args[0])
        return File(args[0])

    if getattr(meta, "hda", False):
        usd = meta.node('/obj/lopimport1').createNode("usdimport")
        usd.parm("filepath1").set(args[0])
        usd.parm("reload").pressButton()
        return File(args[0]) or Node(usd.name)

    if getattr(meta, "sbs", False):
        current = meta.graph.getPackage().getFilePath()
        ip = meta.sdresourcescene.SDResourceScene.sNewFromFile(current, args[0], meta.sdresource.EmbedMethod.Linked)
        return File(ip.getFilePath())
    
    if getattr(meta, "data", False):
        meta.ops.wm.usd_import(*args, **kwargs)
        return 

    if getattr(meta, "uclass", False):
        data = meta.AutomatedAssetImportData()
        data.set_editor_property('filenames', *args)
        for k, v in kwargs:
            data.set_editor_property(k, v)
        factory = meta.USDSceneImportFactory()
        data.set_editor_property('factory', factory)
        return meta.tools.import_assets_automated(data)

    if getattr(meta, "knob", False):
        geo = meta.createNode("ReadGeo")
        # TODO: scenegraph tab?
        geo["file"].setValue(args[0])
        geo["reload"].execute()
        return File(args[0]) or Node(geo.name)

    if getattr(meta, "C4DAtom", False):
        ImportId = 1055178
        plug = meta.plugins.FindPlugin(ImportId, meta.PLUGINTYPE_SCENELOADER)
        data = dict()
        plug.Message(meta.MSG_RETRIEVEPRIVATEDATA, data)

        usdImport = data.get("imexporter", None)
        usdImport[meta.USDIMPORTER_KEEPBRIDGEOPEN] = True
        usdImport[meta.USDIMPORTER_CAMERAS] = True
        usdImport[meta.USDIMPORTER_LIGHTS] = True
        usdImport[meta.USDIMPORTER_GEOMETRY] = True
        usdImport[meta.USDIMPORTER_NORMALS] = meta.USDIMPORTER_NORMALS_PHONG  # USDIMPORTER_NORMALS_NONE / USDIMPORTER_NORMALS_VERTEX
        usdImport[meta.USDIMPORTER_PHONG_ANGLE] = 40
        usdImport[meta.USDIMPORTER_UV] = True
        usdImport[meta.USDIMPORTER_DISPLAYCOLOR] = True

        meta.documents.MergeDocument(meta.documents.GetActiveDocument(), args[0],
                                     meta.SCENEFILTER_OBJECTS | meta.SCENEFILTER_MATERIALS, None)
        meta.EventAdd()
        return File(args[0])
    
    if getattr(meta, "fusion", False):
        meta.fusion.GetCurrentComp().Lock()
        im = meta.fusion.GetCurrentComp().AddTool("uLoader")
        im.ImportFile = args[0]
        # meta.eval("comp:Render({Tool = comp.%s})" % im.Name)
        meta.fusion.GetCurrentComp().Unlock()
        return Node(im.Name)

    if getattr(meta, "textureset", False):
        return meta.project.create(*args, **kwargs)

    if getattr(meta, "SceneObject", False):
        return meta.importModel(args[0])


def _usdExporter(*args, **kwargs):
    """_summary_

    Returns:
        _type_: _description_
    """    

    if getattr(meta, "mayaUSDExport", False):
        meta.loadPlugin('mayaUsdPlugin', qt=True)
        meta.mayaUSDExport(
            file=args[0]
            # chaser=['alembic'],
            # chaserArgs=[
            #     ('alembic', 'primvarprefix', 'ABC_,ABC2_=customPrefix_,ABC3_=,ABC4_=customNamespace:'),]
        )
        return File(args[0])

    if getattr(meta, "hda", False):
        usd = meta.node("/obj/lopimport1").createNode("usdexport")
        usd.parm('lopoutput').set(args[0])
        usd.parm('execute').pressButton()
        return File(args[0]) or Node(usd.name)

    if getattr(meta, "sbs", False):
        from yurlungur.adapters import substance_designer as sd
        c = meta.sbs.sdmodelgraphexporter.SDModelGraphExporter.sNew()
        c.exportModelGraph(sd.graph, args[0])
        return 
    
    if getattr(meta, "data", False):
        return File(partial(meta.ops.wm.usd_export, filepath=args[0])(**kwargs))

    if getattr(meta, "C4DAtom", False):
        usdExportId = 1055179
        plug = meta.plugins.FindPlugin(usdExportId, meta.PLUGINTYPE_SCENESAVER)
        data = dict()
        plug.Message(meta.MSG_RETRIEVEPRIVATEDATA, data)

        usdExport = data.get("imexporter", None)
        usdExport[meta.USDEXPORTER_FILEFORMAT] = meta.USDEXPORTER_FILEFORMAT_USDC if args[0].endswith(".usdc", False) else meta.USDEXPORTER_FILEFORMAT_USDA
        usdExport[meta.USDEXPORTER_ZIP] = args[0].endswith(".usdz")
        usdExport[meta.USDEXPORTER_CAMERAS] = True
        usdExport[meta.USDEXPORTER_LIGHTS] = True
        usdExport[meta.USDEXPORTER_GEOMETRY] = True
        usdExport[meta.USDEXPORTER_NORMALS] = True
        usdExport[meta.USDEXPORTER_UV] = True
        usdExport[meta.USDEXPORTER_DISPLAYCOLOR] = True
        usdExport[meta.USDEXPORTER_VERTEXCOLORS] = True

        meta.documents.SaveDocument(meta.documents.GetActiveDocument(), args[0], meta.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, usdExportId)
        return File(args[0])

    if getattr(meta, "textureset", False):
        meta.js.evaluate("alg.project.exportMesh()")
        meta.js.evaluate("alg.mapexport.exportMesh()")
        return meta.export.export_project_textures(**kwargs)
    
    if getattr(meta, "SceneObject", False):
        if meta.getToolbagVersion() > 4060:
            return meta.exportSceneUSD(args[0], **kwargs)


class _NodeType(object):
    """
    >>> blur = yurlungur.node.Blur()
    >>> blur = yurlungur.Node().create("Blur")
    """

    def __getattr__(self, item):
        if getattr(meta, "types", False):
            nodes = fnmatch.filter(dir(meta.types), str(item))
        else:
            nodes = self.findNodes(item)

        for node in nodes:
            setattr(self, str(item), Node(node))

        return Node(item)

    def findNodes(self, pattern):
        if getattr(meta, "listNodeTypes", False):
            # http://help.autodesk.com/cloudhelp/2016/JPN/Maya-Tech-Docs/CommandsPython/shadingNode.html
            categories = ["geometry", "camera", "light",
                          "utility", "color", "shader",
                          "texture", "rendering", "postprocess"]

            # meta.allNodeTypes(ia=1)
            for category in categories:
                yield fnmatch.filter(meta.listNodeTypes(category), pattern)

        if getattr(meta, "hda", False):
            for category in meta.nodeTypeCategories().keys():
                yield fnmatch.filter(
                    meta.nodeTypeCategories()[category].nodeTypes().keys(),
                    pattern
                )

        if getattr(meta, "knob", False):
            yield


# Monkey-Patch for node
node = Node()

Node.ls = _ls
Node.sel = _select
Node.rm = _rm
Node.glob = _glob

# Monkey-Patch for file
file = File()
File.usd = types.ModuleType("usd")
File.usd.enable = False

if list(filter(lambda x: getattr(meta, x, False), ["hda", "uclass", "C4DAtom", "ls", "knob", "data"])):
    File.usd.enable = True
    File.usd.Import = _usdImporter
    File.usd.Export = _usdExporter

try:
    from pxr import Usd
    File.usd.enable = True
    File.usd = Usd
except ImportError:
    pass

# Monkey-Patch for command
cmd = Command()
Command.bake = _Bake
