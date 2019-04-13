# -*- coding: utf-8 -*-
import os
import sys
import inspect
from functools import partial, total_ordering

from yurlungur.core.wrapper import (
    YException, _YObject, _YAttr, OM
)
from yurlungur.tool.math import (
    YVector, YColor, YMatrix
)
from yurlungur.tool.meta import meta
from yurlungur.tool.util import trace


class YObject(_YObject):
    """base class
    >>> obj = YObject("pCone")
    >>> obj("cone")
    """

    def __init__(self, item):
        self.item = item

    def __repr__(self):
        if hasattr(meta, "SDNode"):
            return "id: " + self.name
        else:
            return self.name

    @property
    def name(self):
        if hasattr(meta, "SDNode"):
            return self.id
        else:
            return self.item

    @property
    def id(self):
        if hasattr(meta, "SDNode"):
            node_id = ""
            for node in meta.graph.getNodes():
                d = node.getDefinition()
                if d.getId() == self.item or d.getLabel() == self.item or node.getIdentifier() == self.item:
                    node_id = node.getIdentifier()
                    break
            return node_id if node_id else meta.graph.getIdentifier()

        if hasattr(meta, "ls"):
            return meta.ls(self.name, uuid=1)[0] or 0

        if hasattr(meta, "hda"):
            return meta.node(self.name).sessionId() or 0

        if hasattr(meta, "runtime"):
            return meta.runtime.getnodebyname(self.name).gbufferChannel or 0

        if hasattr(meta, "data"):
            return meta.data.objects[self.name].id_data or 0

        if hasattr(meta, "knob"):
            return meta.toNode(self.name)["name"].value() or 0

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ID or 0

        if hasattr(meta, 'uclass'):
            return

        raise YException

    @trace
    def __call__(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            meta.graph.setIdentifier(args[0])

        if hasattr(meta, "rename"):
            return meta.rename(self.item, *args, **kwargs)

        if hasattr(meta, "hda"):
            return meta.node(self.item).setName(*args, **kwargs)

        if hasattr(meta, "runtime"):
            meta.runtime.getnodebyname(self.name).name = args[0]
            return YNode(args[0])

        if hasattr(meta, "data"):
            meta.data.objects[self.item].name = "".join(args)
            return "".join(args)

        if hasattr(meta, "knob"):
            meta.toNode(self.item).setName(args[0], **kwargs)

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.item).SetAttrs({"TOOLS_Name": args[0]})

        if hasattr(meta, 'uclass'):
            if meta.assets.rename_asset(self.name, args[0]):
                return YNode(args[0])

    @trace
    def __getattr__(self, val):
        if hasattr(meta, "SDNode"):
            prop = meta.graph.getNodeFromId(self.name).getPropertyFromId(val, meta.SDPropertyCategory.Input)
            return YAttr(meta.graph.getNodeFromId(self.name).getPropertyValue(prop).get(), self.name, val)

        if hasattr(meta, "getAttr"):
            return YAttr(meta.getAttr(self.name + "." + val), self.name, val)

        if hasattr(meta, "hda"):
            parm = (meta.node(self.name).parm(val) or meta.node(self.name).parmTuple(val))
            return YAttr(parm.eval(), self.name, val)

        if hasattr(meta, "runtime"):
            if '.' in self.name:
                node, prop = self.name.split('.')
                return YAttr(getattr(meta.runtime.getnodebyname(node), prop),
                             meta.runtime.getnodebyname(node).name, val)
            else:
                return YAttr(getattr(meta.runtime.getnodebyname(self.name), val), self.name, val)

        if hasattr(meta, "data"):
            return YAttr(meta.data.objects[self.name].name, self.name, val)

        if hasattr(meta, "knob"):
            return YAttr(meta.toNode(self.name)[val], self.name, val)

        if hasattr(meta, "fusion"):
            return YAttr(getattr(meta.fusion.GetCurrentComp().FindTool(self.name), val), self.name, val)

        if hasattr(meta, 'uclass'):
            return YAttr(
                meta.editor.get_actor_reference(self.name).get_editor_property(val), self.name, val)

        raise YException

    @trace
    def attr(self, val, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            prop = meta.graph.getNodeFromId(self.name).getPropertyFromId(val, meta.SDPropertyCategory.Input)
            return YAttr(meta.graph.getNodeFromId(self.name).getPropertyValue(prop).get(), self.name, val)

        if hasattr(meta, "getAttr"):
            return YAttr(meta.getAttr(self.name + "." + val, *args, **kwargs), self.name, val)

        if hasattr(meta, "hda"):
            parm = (meta.node(self.name).parm(val) or meta.node(self.name).parmTuple(val))
            return YAttr(parm.eval(), self.name, val)

        if hasattr(meta, "runtime"):
            return YAttr(getattr(meta.runtime.getnodebyname(self.name), val), self.name, val)

        if hasattr(meta, "data"):
            return YAttr(meta.data.objects[self.name].name, self.name, val)

        if hasattr(meta, "knob"):
            return YAttr(meta.toNode(self.name)[val], self.name, val)

        if hasattr(meta, "fusion"):
            return YAttr(getattr(meta.fusion.GetCurrentComp().FindTool(self.name), val), self.name, val)

        if hasattr(meta, 'uclass'):
            return YAttr(
                meta.editor.get_actor_reference(self.name).get_editor_property(val), self.name, val)

        raise YException

    @property
    def attrs(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            return tuple([
                prop.getId() for prop in
                meta.graph.getNodeFromId(self.name).getProperties(meta.SDPropertyCategory.Input)
            ])

        if hasattr(meta, "listAttr"):
            return tuple(meta.listAttr(self.name, *args, **kwargs)) or None

        if hasattr(meta, "hda"):
            return tuple(p.name() for p in meta.node(self.name).parms() or [])

        if hasattr(meta, "runtime"):
            return inspect.getmembers(meta.runtime.getnodebyname(self.name))

        if hasattr(meta, "data"):
            return tuple(inspect.getmembers(meta.data.objects[self.name]))

        if hasattr(meta, "knob"):
            return tuple([knob.name() for knob in meta.toNode(self.name).allKnobs()])

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.name).GetAttrs()

        if hasattr(meta, 'uclass'):
            return meta.assets.find_asset_data(self.name).get_asset()

        raise YException

    @trace
    def create(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            node_id = args[0] if "::" in args[0] else "::".join(["sbs", "compositing", args[0]])
            return YNode(meta.graph.newNode(node_id).getIdentifier())

        if hasattr(meta, "createNode"):
            return YNode(meta.createNode(*args, **kwargs))

        if hasattr(meta, "hda"):
            if len(args) == 0 and len(kwargs) == 0:
                return YNode(
                    partial(
                        meta.node(self.name).createNode, self.name
                    )(*args, **kwargs).path())
            return YNode(meta.node(self.name).createNode(*args, **kwargs).path())

        if hasattr(meta, "runtime"):
            obj = getattr(meta.runtime, args[0])
            msx_class = meta.runtime.classOf(obj)
            _obj = obj(**kwargs)

            if str(msx_class) == 'modifier':
                meta.runtime.addModifier(meta.runtime.getnodebyname(self.name), _obj)
                return YNode(meta.runtime.getnodebyname(self.name).name + "." + _obj.name)

            elif str(msx_class) == 'material':
                meta.runtime.material = _obj

            return YNode(_obj.name)

        if hasattr(meta, "data"):
            try:
                getattr(meta.ops.mesh, str(self).lower() + "_add")(*args, **kwargs)
            except AttributeError:
                getattr(meta.ops.object, str(self).lower() + "_add")(*args, **kwargs)

        if hasattr(meta, "fusion"):
            return YNode(meta.fusion.GetCurrentComp().AddTool(*args, **kwargs).Name)

        if hasattr(meta, 'uclass'):
            if not 'FactoryNew' in args[0]:
                return None
            # factory = getattr(meta, args[0])()
            # tool = meta.AssetToolsHelpers.get_asset_tools()
            # Name, Path, None
            # fargs = args[1:].append(factory)
            # tool.create_asset(*fargs)

        raise YException

    @trace
    def delete(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            return meta.graph.deleteNode(meta.graph.getNodeFromId(self.name))

        if hasattr(meta, "delete"):
            node = meta.toNode(self.name) if hasattr(meta, "knob") else self.name
            return meta.delete(node, *args, **kwargs)

        if hasattr(meta, "hda"):
            return meta.node(self.name).destroy()

        if hasattr(meta, "runtime"):
            return meta.runtime.delete(meta.runtime.getnodebyname(self.name))

        if hasattr(meta, "data"):
            return meta.context.scene.objects.unlink(meta.data.objects[self.name])

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.name).Delete()

        if hasattr(meta, 'uclass'):
            # return meta.assets.delete_asset(self.name)
            return meta.editor.get_actor_reference(self.name).destroy_actor()

        raise YException

    def instance(self, *args, **kwarg):
        if hasattr(meta, "SDNode"):
            return meta.graph.newInstanceNode(self.name, *args, **kwarg)

        if hasattr(meta, "instance"):
            if len(args) > 0:
                return meta.instance(self.name, lf=1)
            else:
                return meta.listRelatives(self.name, ap=1, f=1)[1:] or None

        if hasattr(meta, "runtime"):
            return YNode(meta.runtime.instance(meta.runtime.getnodebyname(self.name)).name)

        if hasattr(meta, "hda"):
            return meta.node(self.name).copyTo(*args, **kwarg)

        if hasattr(meta, "knob"):
            if len(args) > 0:
                return meta.clone(meta.toNode(self.name), *args, **kwarg)
            else:
                return meta.toNode(self.name).clones()

        if hasattr(meta, "fusion"):
            meta.fusion.GetCurrentComp().Copy(self.name)
            return meta.fusion.GetCurrentComp().Paste(*args, **kwarg)

        if hasattr(meta, 'uclass'):
            return

        raise YException

    def select(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            context = meta.sd_app.getLocationContext()
            if context:
                return context.getSelectedNodes()
            else:
                return None

        if hasattr(meta, "select"):
            if 'shape' not in kwargs and 's' not in kwargs:
                kwargs['s'] = True

            if len(args) == 0 and len(kwargs) == 0:
                return meta.ls(sl=1)
            else:
                return meta.select(*args, **kwargs)

        if hasattr(meta, "hda"):
            return meta.node(self.name).setCurrent(*args, **kwargs)

        if hasattr(meta, "runtime"):
            if len(args) == 0 and len(kwargs) == 0:
                return meta.runtime.select(meta.runtime.getnodebyname(self.name))
            else:
                if meta.runtime.execute('$') == meta.runtime.execute('$selection'):
                    return meta.runtime.execute('$ as array')
                else:
                    return meta.runtime.execute('$')

        if hasattr(meta, "knob"):
            if len(args) == 0 and len(kwargs) == 0:
                return meta.selectedNodes()
            else:
                return meta.toNode(self.name).setSelected()

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().CurrentFrame.FlowView.Select(*args, **kwargs)

        if hasattr(meta, 'uclass'):
            # return meta.editor.get_selected_assets()
            if len(args) == 0 and len(kwargs) == 0:
                return meta.editor.get_actor_reference(self.name, True)
            else:
                return meta.editor.get_selection_set()

        raise YException

    @trace
    def hide(self, on=True):
        if hasattr(meta, "data"):
            meta.data.objects[self.name].hide = on
            return

        if hasattr(meta, "runtime"):
            return getattr(meta.runtime, "hide" if on else "unhide")(meta.runtime.getnodebyname(self.name))

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.name).SetAttrs(
                {'TOOLB_Visible': on, "TOOLB_Locked": True})

        if hasattr(meta, 'uclass'):
            # set_actor_hidden_in_game
            return meta.editor.get_actor_reference(self.name).set_editor_property('hidden', on)

        raise YException

    @trace
    def geometry(self):
        if hasattr(meta, "ls"):
            dag = OM.MGlobal.getSelectionListByName(self.name).getDagPath(0)
            return OM.MFnMesh(dag)

        if hasattr(meta, "hda"):
            return meta.node(self.name).geometry()

        if hasattr(meta, "data"):
            return meta.data.meshes[self.name]

        if hasattr(meta, "runtime"):
            return meta.runtime.getnodebyname(self.name).mesh

        if hasattr(meta, 'uclass'):
            actor = meta.editor.get_actor_reference(self.name).get_class().get_name()
            if actor == 'StaticMeshActor' or actor == 'SkeletalMeshActor':
                return meta.editor.get_actor_reference(self.name)
            return

        raise YException


class YNode(YObject):
    """relationship object"""

    def __init__(self, item=None):
        if sys.version_info < (3, 2):
            super(YNode, self).__init__(item)
        else:
            super().__init__(item)
        self.item = item

        if self.item and hasattr(meta, "SDNode"):
            self._inputs = meta.graph.getNodeFromId(self.name).getProperties(meta.SDPropertyCategory.Input)
            self._outputs = meta.graph.getNodeFromId(self.name).getProperties(meta.SDPropertyCategory.Output)

    def parent(self, *args, **kwarg):
        if hasattr(meta, "SDNode"):
            nodes = []
            for prop in self._inputs:
                for connect in meta.graph.getNodeFromId(self.name).getPropertyConnections(prop):
                    nodes.append(YNode(connect.getInputPropertyNode().getIdentifier()))
            return nodes

        if hasattr(meta, "getAttr"):
            if len(args) == 0 and len(kwarg) > 0:
                return meta.parent(self.item, *args, **kwarg)
            else:
                return YNode(
                    partial(meta.listRelatives, self.item, p=1)(*args, **kwarg))

        if hasattr(meta, "hda"):
            return YNode(meta.node(self.name).parent().path())

        if hasattr(meta, "runtime"):
            if len(args) > 0:
                meta.runtime.getnodebyname(self.item).parent = args[0]
                return YNode(args[0])
            else:
                _parent = meta.runtime.getnodebyname(self.item).parent
                return YNode(_parent.name) if _parent else None

        if hasattr(meta, "knob"):
            index = meta.toNode(self.name).inputs() - 1
            return YNode(meta.toNode(self.name).input(index).name())

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ParentTool

        if hasattr(meta, 'uclass'):
            return YNode(
                meta.editor.get_actor_reference(self.name).get_parent_actor().get_name())

        raise YException

    def children(self, *args, **kwarg):
        if hasattr(meta, "SDNode"):
            nodes = []
            for prop in self._outputs:
                for connect in meta.graph.getNodeFromId(self.name).getPropertyConnections(prop):
                    nodes.append(YNode(connect.getOutputPropertyNode().getIdentifier()))
            return nodes

        if hasattr(meta, "getAttr"):
            return partial(meta.listRelatives, self.item, c=1)(*args, **kwarg) or None

        if hasattr(meta, "hda"):
            return [YNode(node.name) for node in meta.node(self.item).children()]

        if hasattr(meta, "runtime"):
            if len(args) > 0:
                meta.runtime.execute('append $%s.children $%s' % (self.item, args[0]))
                return YNode(args[0])
            else:
                nodes = []
                children = meta.runtime.getnodebyname(self.item).children
                for i in range(children.count):
                    nodes.append(children[i].name)
                return nodes

        raise YException

    @trace
    def connect(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            args = (args[0], meta.graph.getNodeFromId(args[1].id), args[2])
            return meta.graph.getNodeFromId(self.name).newPropertyConnectionFromId(*args).getClassName()

        if hasattr(meta, "connectAttr"):
            return partial(meta.connectAttr, self.name + "." + args[0])(args[1:], **kwargs)

        if hasattr(meta, "hda"):
            return partial(meta.node(self.name).setInput, 0)(*args, **kwargs)

        if hasattr(meta, "knob"):
            return meta.toNode(self.name).setInput(*args, **kwargs)

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ConnectInput(*args, **kwargs)

        raise YException

    @trace
    def disconnect(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            for arg in args:
                for prop in self._inputs:
                    if arg == prop.getId():
                        return meta.graph.getNodeFromId(self.name).deletePropertyConnections(prop)
                for prop in self._outputs:
                    if arg == prop.getId():
                        return meta.graph.getNodeFromId(self.name).deletePropertyConnections(prop)
            return

        if hasattr(meta, "disconnectAttr"):
            return partial(meta.disconnectAttr, self.name + "." + args[0])(args[1:], **kwargs)

        if hasattr(meta, "hda"):
            return partial(meta.node(self.name).setInput, 0, None)(*args, **kwargs)

        if hasattr(meta, "knob"):
            return meta.toNode(self.name).setInput(0, None)

        if hasattr(meta, "fusion"):
            return setattr(meta.fusion.GetCurrentComp().FindTool(self.name), "Input", None)

        raise YException

    @trace
    def inputs(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            return [connect.getId() for connect in self._inputs if connect.isConnectable()]

        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, s=1)(*args, **kwargs)

        if hasattr(meta, "hda"):
            return [YNode(node.name) for node in meta.node(self.name).inputs()]

        if hasattr(meta, "knob"):
            return [YNode(meta.toNode(self.name).input(index).name()) for index in
                    range(meta.toNode(self.name).inputs())]

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.name).GetInputList().values()[0].GetAttrs()

        raise YException

    @trace
    def outputs(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            return [connect.getId() for connect in self._outputs if connect.isConnectable()]

        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, d=1)(*args, **kwargs)

        if hasattr(meta, "hda"):
            return [YNode(node.name) for node in meta.node(self.name).outputs()]

        if hasattr(meta, "knob"):
            return meta.toNode(self.name).dependencies(meta.EXPRESSIONS)

        if hasattr(meta, "fusion"):
            return meta.fusion.GetCurrentComp().FindTool(self.name).GetOutputList().values()[0].GetAttrs()

        raise YException


@total_ordering
class YAttr(_YAttr):
    """parametric object"""

    def __init__(self, *args):
        assert len(args) > 2, "parameter is invalid."
        self._values = args
        self.obj, self.val = self._values[1:]

    @property
    def value(self):
        if hasattr(meta, "SDNode"):
            return self._values[0]
        
        if ':' in str(self._values[0]):
            return getattr(self._values[0], self.val)
        else:
            return self._values[0]

    def __getitem__(self, idx):
        return self._values[idx]

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value >= other.value

    @trace
    def set(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            sd_value = meta.SDValueInt.sNew(args[0])

            if type(self.value) == bool:
                sd_value = meta.SDValueBool.sNew(args[0])
            if type(self.value) == float:
                sd_value = meta.SDValueFloat.sNew(args[0])
            if type(self.value) == str:
                sd_value = meta.SDValueString.sNew(args[0])

            prop = meta.graph.getNodeFromId(self.obj).getPropertyFromId(self.val, meta.SDPropertyCategory.Input)
            return meta.graph.getNodeFromId(self.obj).setPropertyValue(prop, sd_value)

        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, *args, **kwargs)

        if hasattr(meta, "hda"):
            parm = (meta.node(self.obj).parm(self.val) or
                    meta.node(self.obj).parmTuple(self.val))
            return parm.set(
                args[0].tolist() if hasattr(args[0], "T") else args[0], **kwargs)

        if hasattr(meta, "runtime"):
            if ':' in str(self._values[0]):
                return setattr(self._values[0], self.val, args[0])
            else:
                return setattr(meta.runtime.getnodebyname(self.obj), self.val, args[0])

        if hasattr(meta, "data"):
            return setattr(meta.data.objects[self.obj],
                           self.val, args[0].tolist() if hasattr(args[0], "T") else args[0])

        if hasattr(meta, "knob"):
            return meta.toNode(self.obj)[self.val].setValue(args[0], **kwargs)

        if hasattr(meta, "fusion"):
            return setattr(meta.fusion.GetCurrentComp().FindTool(self.obj), self.val, args[0])

        if hasattr(meta, 'uclass'):
            return meta.assets.find_asset_data(self.obj).get_asset().set_editor_property(self.obj, self.val)

        raise YException

    def create(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    @trace
    def lock(self, on):
        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, lock=on)

        if hasattr(meta, "hda"):
            return meta.node(self.obj).parm(self.val).lock(on)

        if hasattr(meta, "knob"):
            return meta.toNode(self.obj)[self.val].setEnabled(on)

        raise YException

    @trace
    def hide(self, on=True):
        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, keyable=not on, channelBox=not on)

        if hasattr(meta, "hda"):
            return meta.node(self.obj).parm(self.val).hide(on)

        if hasattr(meta, "knob"):
            return meta.toNode(self.obj)[self.val].setVisible(not on)

        raise YException

    @property
    def asVector(self):
        try:
            return YVector(self._values[0])
        except TypeError:
            return YVector(*self._values[0])

    @property
    def asColor(self):
        try:
            return YColor(self._values[0])
        except TypeError:
            return YColor(*self._values[0])

    @property
    def asMatrix(self):
        try:
            return YMatrix(self._values[0])
        except TypeError:
            return YMatrix(*self._values[0])


class YFile(_YObject):
    """save, open and export"""

    def __init__(self, path=""):
        self.file = path

    @property
    def name(self):
        return os.path.basename(self.file)

    @property
    def path(self):
        return os.path.dirname(self.file)

    @classmethod
    def open(cls, *args, **kwargs):
        from yurlungur.core.command import file

        if args[0].endswith("abc"):
            return cls(file.abcImporter(*args, **kwargs))

        if args[0].endswith("fbx"):
            return cls(file.fbxImporter(*args, **kwargs))

        if hasattr(meta, "sbs"):
            return cls(meta.manager.loadUserPackage(*args, **kwargs))

        if hasattr(meta, "file"):
            return cls(partial(meta.file, i=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.load(*args, **kwargs))

        if hasattr(meta, "runtime"):
            if meta.runtime.loadMaxFile(*args, **kwargs):
                return cls(args[0])

        if hasattr(meta, "data"):
            return cls(meta.ops.wm.open_mainfile(*args, **kwargs))

        if hasattr(meta, "knob"):
            return meta.scriptOpen(*args, **kwargs)

        if hasattr(meta, "fusion"):
            storage = meta.resolve.GetMediaStorage()
            if "." in args:
                return storage.AddItemsToMediaPool(*args)
            else:
                return meta.manager.LoadProject(*args, **kwargs)

        raise YException

    @classmethod
    def save(cls, *args, **kwargs):
        from yurlungur.core.command import file

        if args[0].endswith("abc"):
            return cls(file.abcExporter(*args, **kwargs))

        if args[0].endswith("fbx"):
            return cls(file.fbxExporter(*args, **kwargs))

        if hasattr(meta, "sbs"):
            return cls(meta.manager.savePackageAs(*args, **kwargs))

        if hasattr(meta, "file"):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.save(*args, **kwargs))

        if hasattr(meta, "runtime"):
            if meta.runtime.saveMaxFile(*args, **kwargs):
                return cls(args[0])

        if hasattr(meta, "data"):
            return meta.ops.wm.save_mainfile(*args, **kwargs)

        if hasattr(meta, "knob"):
            return meta.scriptSave(*args, **kwargs)

        if hasattr(meta, "fusion"):
            return meta.manager.SaveProject(*args, **kwargs)

        raise YException

    @property
    def current(self):
        if hasattr(meta, "sbs"):
            return meta.manager.getUserPackageFromFilePath()

        if hasattr(meta, "file"):
            return meta.file(exn=1, q=1)

        if hasattr(meta, "hipFile"):
            return meta.hipFile.path()

        if hasattr(meta, "runtime"):
            return meta.runtime.maxFilePath + meta.runtime.maxFileName

        if hasattr(meta, "data"):
            return meta.data.filepath

        if hasattr(meta, "knob"):
            return meta.scriptName()

        if hasattr(meta, "fusion"):
            return meta.manager.GetCurrentProject()

        raise YException

    def reference(self):
        raise YException
