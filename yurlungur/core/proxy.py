# -*- coding: utf-8 -*-

try:
    import os
    import inspect
    from functools import partial, total_ordering
except ImportError:
    total_ordering = dir

from yurlungur.core.wrapper import YException, _YObject, _YAttr
from yurlungur.core.deco import trace
from yurlungur.core.math import YVector, YColor, YMatrix
from yurlungur.tool.meta import meta


class YObject(_YObject):
    """base class
    >>> obj = YObject("pCone")
    >>> obj("cone")
    """

    def __init__(self, item):
        self.item = item

    @property
    def name(self):
        if getattr(meta, "SDNode", False):
            return self.id
        else:
            return self.item

    def __repr__(self):
        if getattr(meta, "SDNode", False):
            return "id:" + self.name
        else:
            return self.name

    @property
    def id(self):
        if getattr(meta, "SDNode", False):
            node_id = ""
            for node in meta.graph.getNodes():
                d = node.getDefinition()
                if (
                        d.getId() == self.item
                        or d.getLabel() == self.item
                        or node.getIdentifier() == self.item
                ):
                    node_id = node.getIdentifier()
                    break
            return node_id if node_id else meta.graph.getIdentifier()

        if getattr(meta, "ls", False):
            return meta.ls(self.name, uuid=1)[0] or 0

        if getattr(meta, "hda", False):
            return meta.node(self.name).sessionId() or 0

        if getattr(meta, "runtime", False):
            return meta.runtime.getnodebyname(self.name).gbufferChannel or 0

        if getattr(meta, "data", False):
            return meta.data.objects[self.name].id_data or 0

        if getattr(meta, "knob", False):
            return meta.toNode(self.name)["name"].value() or 0

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ID or 0

        if getattr(meta, "uclass", False):
            return meta.ue4.uname(self.name).get_name() or 0

        raise YException

    @trace
    def __call__(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            meta.graph.setIdentifier(args[0])

        if getattr(meta, "rename", False):
            return meta.rename(self.item, *args, **kwargs)

        if getattr(meta, "hda", False):
            return meta.node(self.item).setName(*args, **kwargs)

        if getattr(meta, "runtime", False):
            meta.runtime.getnodebyname(self.name).name = args[0]
            return YNode(args[0])

        if getattr(meta, "data", False):
            meta.data.objects[self.item].name = "".join(args)
            return "".join(args)

        if getattr(meta, "knob", False):
            meta.toNode(self.item).setName(args[0], **kwargs)

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.item)
                    .SetAttrs({"TOOLS_Name": args[0]})
            )

        if getattr(meta, "doc", False):
            try:
                return setattr(meta.doc.activeLayer, "name", args[0])
            except AttributeError:
                return meta.doc.currentLayer().setValue_forKey_(args[0], "name")

        if getattr(meta, "wind_type", False):
            return meta.module

        if getattr(meta, "uclass", False):
            uname = meta.ue4.uname(self.name)
            if type(uname) == str:
                meta.assets.rename_asset(
                    uname, os.path.join(os.path.dirname(uname), args[0])
                )
                return YNode(args[0])
            else:
                return uname.set_actor_label(args[0])

    @trace
    def __getattr__(self, val):
        if getattr(meta, "SDNode", False):
            prop = meta.graph.getNodeFromId(self.name).getPropertyFromId(
                val, meta.sd.SDPropertyCategory.Input
            )
            return YAttr(
                meta.graph.getNodeFromId(self.name).getPropertyValue(prop).get(),
                self.name,
                val,
            )

        if getattr(meta, "getAttr", False):
            return YAttr(meta.getAttr(self.name + "." + val), self.name, val)

        if getattr(meta, "hda", False):
            parm = meta.node(self.name).parm(val) or meta.node(self.name).parmTuple(val)
            return YAttr(parm.eval(), self.name, val)

        if getattr(meta, "runtime", False):
            if "." in self.name:
                node, prop = self.name.split(".")
                return YAttr(
                    getattr(meta.runtime.getnodebyname(node), prop),
                    meta.runtime.getnodebyname(node).name,
                    val,
                )
            else:
                return YAttr(
                    getattr(meta.runtime.getnodebyname(self.name), val), self.name, val
                )

        if getattr(meta, "data", False):
            return YAttr(meta.data.objects[self.name].name, self.name, val)

        if getattr(meta, "knob", False):
            return YAttr(meta.toNode(self.name)[val], self.name, val)

        if getattr(meta, "fusion", False):
            return YAttr(
                getattr(meta.fusion.GetCurrentComp().FindTool(self.name), val),
                self.name,
                val,
            )

        if getattr(meta, "doc", False):
            try:
                layer = meta.doc.layers[self.name]
            except TypeError:
                layer = meta.ps.Document().layers[self.name]

            return YAttr(getattr(layer, val), self.name, val)

        if getattr(meta, "wind_type", False):
            return YAttr(meta.module, self.name, val)

        if getattr(meta, "uclass", False):
            try:
                return YAttr(
                    meta.ue4.uname(self.name).get_editor_property(val), self.name, val
                )
            except:
                return YAttr(
                    meta.ue4.uname(self.name).root_component.get_editor_property(val),
                    self.name, val,
                )

        raise YException

    @trace
    def attr(self, val, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            prop = meta.graph.getNodeFromId(self.name).getPropertyFromId(
                val, meta.sd.SDPropertyCategory.Input
            )
            return YAttr(
                meta.graph.getNodeFromId(self.name).getPropertyValue(prop).get(),
                self.name,
                val,
            )

        if getattr(meta, "getAttr", False):
            return YAttr(
                meta.getAttr(self.name + "." + val, *args, **kwargs), self.name, val
            )

        if getattr(meta, "hda", False):
            parm = meta.node(self.name).parm(val) or meta.node(self.name).parmTuple(val)
            return YAttr(parm.eval(), self.name, val)

        if getattr(meta, "runtime", False):
            return YAttr(
                getattr(meta.runtime.getnodebyname(self.name), val), self.name, val
            )

        if getattr(meta, "data", False):
            return YAttr(meta.data.objects[self.name].name, self.name, val)

        if getattr(meta, "knob", False):
            return YAttr(meta.toNode(self.name)[val], self.name, val)

        if getattr(meta, "fusion", False):
            return YAttr(
                getattr(meta.fusion.GetCurrentComp().FindTool(self.name), val),
                self.name,
                val,
            )

        if getattr(meta, "doc", False):
            try:
                layer = meta.doc.layers[self.name]
            except TypeError:
                layer = meta.ps.Document().layers[self.name]

            return YAttr(getattr(layer, val), self.name, val)

        if getattr(meta, "wind_type", False):
            return YAttr(meta.module, self.name, val)

        if getattr(meta, "uclass", False):
            try:
                return YAttr(
                    meta.ue4.uname(self.name).get_editor_property(val), self.name, val
                )
            except:
                return YAttr(
                    meta.ue4.uname(self.name).root_component.get_editor_property(val),
                    self.name,
                    val,
                )

        raise YException

    @property
    def attrs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return tuple([
                prop.getId() for prop in
                meta.graph.getNodeFromId(self.name).getProperties(
                    meta.sd.SDPropertyCategory.Input
                )
            ])

        if getattr(meta, "listAttr", False):
            return tuple(meta.listAttr(self.name, *args, **kwargs)) or None

        if getattr(meta, "hda", False):
            return tuple(p.name() for p in meta.node(self.name).parms() or [])

        if getattr(meta, "runtime", False):
            return inspect.getmembers(meta.runtime.getnodebyname(self.name))

        if getattr(meta, "data", False):
            return tuple(inspect.getmembers(meta.data.objects[self.name]))

        if getattr(meta, "knob", False):
            return tuple([knob.name() for knob in meta.toNode(self.name).allKnobs()])

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).GetAttrs()

        if getattr(meta, "doc", False):
            return tuple(
                [p for p, _ in inspect.getmembers(meta.photoshop.Photoshop.ArtLayer) if "_" not in p])

        if getattr(meta, "uclass", False):
            return meta.ue4.uname(self.name).component_tags()

        raise YException

    @trace
    def create(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            node_id = (
                args[0] if "::" in args[0] else "::".join(["sbs", "compositing", args[0]])
            )
            return YNode(meta.graph.newNode(node_id).getIdentifier())

        if getattr(meta, "createNode", False):
            return YNode(meta.createNode(*args, **kwargs))

        if getattr(meta, "hda", False):
            if len(args) == 0 and len(kwargs) == 0:
                return YNode(
                    partial(meta.node(self.name).createNode, self.name)(
                        *args, **kwargs
                    ).path()
                )
            return YNode(meta.node(self.name).createNode(*args, **kwargs).path())

        if getattr(meta, "runtime", False):
            obj = getattr(meta.runtime, args[0])
            msx_class = meta.runtime.classOf(obj)
            _obj = obj(**kwargs)

            if str(msx_class) == "modifier":
                meta.runtime.addModifier(meta.runtime.getnodebyname(self.name), _obj)
                return YNode(
                    meta.runtime.getnodebyname(self.name).name + "." + _obj.name
                )

            elif str(msx_class) == "material":
                meta.runtime.material = _obj

            return YNode(_obj.name)

        if getattr(meta, "data", False):
            try:
                getattr(meta.ops.mesh, str(self).lower() + "_add")(*args, **kwargs)
            except AttributeError:
                getattr(meta.ops.object, str(self).lower() + "_add")(*args, **kwargs)

        if getattr(meta, "fusion", False):
            return YNode(meta.fusion.GetCurrentComp().AddTool(*args, **kwargs).Name)

        if getattr(meta, "doc", False):
            ps = getattr(meta.photoshop.Photoshop, "ps%s" % args[0], meta.doc.psNormalLayer)
            if ps:
                layer = meta.doc.artLayers.Add()
                layer.name = self.name
                return setattr(layer, "Kind", ps)
            else:
                raise YException

        if getattr(meta, "uclass", False):
            factory = getattr(meta, self.name + "Factory")
            if not args:
                args = (self.name, "/Game", None)

            assert len(args) == 3 and factory

            new_asset = partial(meta.tools.create_asset, *args)(factory(), **kwargs)
            if new_asset:
                meta.assets.save_loaded_asset(new_asset)
                return YNode(new_asset.get_name())
            else:
                return

        raise YException

    @trace
    def delete(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return meta.graph.deleteNode(meta.graph.getNodeFromId(self.name))

        if getattr(meta, "delete", False):
            node = meta.toNode(self.name) if getattr(meta, "knob") else self.name
            return meta.delete(node, *args, **kwargs)

        if getattr(meta, "hda", False):
            return meta.node(self.name).destroy()

        if getattr(meta, "runtime", False):
            return meta.runtime.delete(meta.runtime.getnodebyname(self.name))

        if getattr(meta, "data", False):
            return meta.context.scene.objects.unlink(meta.data.objects[self.name])

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).Delete()

        if getattr(meta, "doc", False):
            try:
                return meta.doc.layers[self.name].delete()
            except TypeError:
                return meta.ps.Document().layers[self.name].delete()

        if getattr(meta, "uclass", False):
            uname = meta.ue4.uname(self.name)
            if type(uname) == str:
                return meta.assets.delete_asset(uname)
            else:
                return uname.destroy_actor()

        raise YException

    def instance(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            return meta.graph.newInstanceNode(self.name, *args, **kwarg)

        if getattr(meta, "instance", False):
            if len(args) > 0:
                return meta.instance(self.name, lf=1)
            else:
                return meta.listRelatives(self.name, ap=1, f=1)[1:] or None

        if getattr(meta, "runtime", False):
            return YNode(
                meta.runtime.instance(meta.runtime.getnodebyname(self.name)).name
            )

        if getattr(meta, "hda", False):
            return meta.node(self.name).copyTo(*args, **kwarg)

        if getattr(meta, "knob", False):
            if len(args) > 0:
                return meta.clone(meta.toNode(self.name), *args, **kwarg)
            else:
                return meta.toNode(self.name).clones()

        if getattr(meta, "fusion", False):
            meta.fusion.GetCurrentComp().Copy(self.name)
            return meta.fusion.GetCurrentComp().Paste(*args, **kwarg)

        if getattr(meta, "doc", False):
            try:
                return meta.doc.layers[self.name].duplicate()
            except TypeError:
                return meta.ps.Document().layers[self.name].duplicate()

        if getattr(meta, "uclass", False):
            uname = meta.ue4.uname(self.name)
            if type(uname) == str:
                return meta.assets.duplicate_asset(
                    uname, os.path.join(os.path.dirname(uname), *args)
                )
            else:
                return

        raise YException

    def select(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            context = meta.sd_app.getUIMgr()
            return [
                YNode(node.getDefinition().getLabel())
                for node in context.getCurrentGraphSelection()
            ]

        if getattr(meta, "select"):
            if "shape" not in kwargs and "s" not in kwargs:
                kwargs["s"] = True

            if len(args) == 0 and len(kwargs) == 0:
                return meta.ls(sl=1)
            else:
                return meta.select(*args, **kwargs)

        if getattr(meta, "hda", False):
            return meta.node(self.name).setCurrent(*args, **kwargs)

        if getattr(meta, "runtime", False):
            if len(args) == 0 and len(kwargs) == 0:
                return meta.runtime.select(meta.runtime.getnodebyname(self.name))
            else:
                if meta.runtime.execute("$") == meta.runtime.execute("$selection"):
                    return meta.runtime.execute("$ as array")
                else:
                    return meta.runtime.execute("$")

        if getattr(meta, "knob", False):
            if len(args) == 0 and len(kwargs) == 0:
                return meta.selectedNodes()
            else:
                return meta.toNode(self.name).setSelected()

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().CurrentFrame.FlowView.Select(
                *args, **kwargs
            )

        if getattr(meta, "doc", False):
            if len(args) == 0 and len(kwargs) == 0:
                try:
                    return YNode(meta.doc.ActiveLayer.name)
                except AttributeError:
                    return YNode(meta.doc.currentLayer().name())
            else:
                try:
                    return setattr(
                        meta.doc,
                        "ActiveLayer",
                        meta.doc.artLayers[self.name],
                    )
                except TypeError:
                    return meta.doc.currentLayer().setTo_(meta.ps.Document().layers[self.name])

        if getattr(meta, "uclass", False):
            uname = meta.ue4.uname(self.name)
            if len(args) == 0 and len(kwargs) == 0:
                if type(uname) == str:
                    return [
                        YNode(asset.get_name())
                        for asset in meta.editor.get_selected_assets()
                    ]
                else:
                    return [
                        YNode(asset.get_name())
                        for asset in meta.editor.get_selection_set()
                    ]
            else:
                if type(uname) == str:
                    return
                else:
                    return meta.editor.set_actor_selection_state(uname, *args)

        raise YException

    @trace
    def hide(self, on=True):
        if getattr(meta, "data", False):
            return setattr(meta.data.objects[self.name], "hide", on)

        if getattr(meta, "runtime", False):
            return getattr(meta.runtime, "hide" if on else "unhide")(
                meta.runtime.getnodebyname(self.name)
            )

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .SetAttrs({"TOOLB_Visible": on, "TOOLB_Locked": True})
            )

        if getattr(meta, "doc", False):
            try:
                return setattr(meta.doc.layers[self.name], "visible", not on)
            except TypeError:
                return meta.ps.Document().layers[self.name].setValue_forKey_(not on, "visible")

        if getattr(meta, "uclass", False):
            return meta.ue4.uname(self.name).root_component.set_editor_property(
                "visible", not on
            )

        raise YException

    @trace
    def geometry(self):
        if getattr(meta, "ls", False):
            from yurlungur.core.wrapper import OM
            dag = OM.MGlobal.getSelectionListByName(self.name).getDagPath(0)
            return OM.MFnMesh(dag)

        if getattr(meta, "hda", False):
            return meta.node(self.name).geometry()

        if getattr(meta, "uclass", False):
            c_actor = meta.ue4.uname(self.name).get_class()
            if c_actor == meta.StaticMeshActor or c_actor == meta.SkeletalMeshActor:
                return meta.ue4.uname(self.name)

            return None

        raise YException


class YNode(YObject):
    """relationship object"""

    def __init__(self, item=None):
        super(YNode, self).__init__(item)
        self.item = item

        if self.item and getattr(meta, "SDNode", False):
            self._inputs = meta.graph.getNodeFromId(self.name).getProperties(meta.sd.SDPropertyCategory.Input)
            self._outputs = meta.graph.getNodeFromId(self.name).getProperties(meta.sd.SDPropertyCategory.Output)

    def parent(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            nodes = []
            for prop in self._inputs:
                for connect in meta.graph.getNodeFromId(
                        self.name
                ).getPropertyConnections(prop):
                    nodes.append(YNode(connect.getInputPropertyNode().getIdentifier()))
            return nodes

        if getattr(meta, "getAttr", False):
            if len(args) == 0 and len(kwarg) > 0:
                return meta.parent(self.item, *args, **kwarg)
            else:
                return YNode(
                    partial(meta.listRelatives, self.item, p=1)(*args, **kwarg)
                )

        if getattr(meta, "hda", False):
            return YNode(meta.node(self.name).parent().path())

        if getattr(meta, "runtime", False):
            if len(args) > 0:
                meta.runtime.getnodebyname(self.item).parent = args[0]
                return YNode(args[0])
            else:
                _parent = meta.runtime.getnodebyname(self.item).parent
                return YNode(_parent.name) if _parent else None

        if getattr(meta, "knob", False):
            index = meta.toNode(self.name).inputs() - 1
            return YNode(meta.toNode(self.name).input(index).name())

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ParentTool

        if getattr(meta, "doc", False):
            return YNode(meta.doc.artLayers[self.name].parent.name)

        if getattr(meta, "uclass", False):
            return YNode(meta.ue4.uname(self.name).get_parent_actor().get_name())

        raise YException

    def children(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            nodes = []
            for prop in self._outputs:
                for connect in meta.graph.getNodeFromId(
                        self.name
                ).getPropertyConnections(prop):
                    nodes.append(YNode(connect.getOutputPropertyNode().getIdentifier()))
            return nodes

        if getattr(meta, "getAttr", False):
            return partial(meta.listRelatives, self.item, c=1)(*args, **kwarg) or None

        if getattr(meta, "hda", False):
            return [YNode(node.name) for node in meta.node(self.item).children()]

        if getattr(meta, "runtime", False):
            if len(args) > 0:
                meta.runtime.execute("append $%s.children $%s" % (self.item, args[0]))
                return YNode(args[0])
            else:
                nodes = []
                children = meta.runtime.getnodebyname(self.item).children
                for i in range(children.count):
                    nodes.append(children[i].name)
                return nodes

        if getattr(meta, "doc", False):
            return [
                YNode(layer.name)
                for layer in meta.doc.LayerSets[self.name].layers
            ]

        if getattr(meta, "uclass", False):
            return [
                YNode(actor.get_name())
                for actor in meta.ue4.uname(self.name).get_all_child_actors()
            ]

        raise YException

    @trace
    def connect(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            args = (args[0], meta.graph.getNodeFromId(args[1].id), args[2])
            return (
                meta.graph.getNodeFromId(self.name)
                    .newPropertyConnectionFromId(*args)
                    .getClassName()
            )

        if getattr(meta, "connectAttr"):
            return partial(meta.connectAttr, self.name + "." + args[0])(
                args[1:], **kwargs
            )

        if getattr(meta, "hda", False):
            return partial(meta.node(self.name).setInput, 0)(*args, **kwargs)

        if getattr(meta, "knob", False):
            return meta.toNode(self.name).setInput(*args, **kwargs)

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .ConnectInput(*args, **kwargs)
            )

        raise YException

    @trace
    def disconnect(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            for arg in args:
                for prop in self._inputs:
                    if arg == prop.getId():
                        return meta.graph.getNodeFromId(
                            self.name
                        ).deletePropertyConnections(prop)
                for prop in self._outputs:
                    if arg == prop.getId():
                        return meta.graph.getNodeFromId(
                            self.name
                        ).deletePropertyConnections(prop)
            return

        if hasattr(meta, "disconnectAttr"):
            return partial(meta.disconnectAttr, self.name + "." + args[0])(
                args[1:], **kwargs
            )

        if getattr(meta, "hda", False):
            return partial(meta.node(self.name).setInput, 0, None)(*args, **kwargs)

        if getattr(meta, "knob", False):
            return meta.toNode(self.name).setInput(0, None)

        if getattr(meta, "fusion", False):
            return setattr(
                meta.fusion.GetCurrentComp().FindTool(self.name), "Input", None
            )

        raise YException

    @trace
    def inputs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return [
                connect.getId() for connect in self._inputs if connect.isConnectable()
            ]

        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, s=1)(*args, **kwargs)

        if getattr(meta, "hda", False):
            return [YNode(node.name) for node in meta.node(self.name).inputs()]

        if getattr(meta, "knob", False):
            return [
                YNode(meta.toNode(self.name).input(index).name())
                for index in range(meta.toNode(self.name).inputs())
            ]

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .GetInputList()
                    .values()[0]
                    .GetAttrs()
            )

        raise YException

    @trace
    def outputs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return [
                connect.getId() for connect in self._outputs if connect.isConnectable()
            ]

        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, d=1)(*args, **kwargs)

        if getattr(meta, "hda", False):
            return [YNode(node.name) for node in meta.node(self.name).outputs()]

        if getattr(meta, "knob", False):
            return meta.toNode(self.name).dependencies(meta.EXPRESSIONS)

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .GetOutputList()
                    .values()[0]
                    .GetAttrs()
            )

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
        if getattr(meta, "SDNode", False):
            return self._values[0]

        if ":" in str(self._values[0]):
            try:
                return getattr(self._values[0], self.val)
            except AttributeError:
                return self._values[0]()
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
    def __call__(self, *args, **kwargs):
        self.set(*args, **kwargs)

    @trace
    def set(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            sd_value = meta.SDValueInt.sNew(args[0])

            if type(self.value) == bool:
                sd_value = meta.SDValueBool.sNew(args[0])
            if type(self.value) == float:
                sd_value = meta.SDValueFloat.sNew(args[0])
            if type(self.value) == str:
                sd_value = meta.SDValueString.sNew(args[0])

            prop = meta.graph.getNodeFromId(self.obj).getPropertyFromId(
                self.val, meta.sd.SDPropertyCategory.Input
            )
            return meta.graph.getNodeFromId(self.obj).setPropertyValue(prop, sd_value)

        if getattr(meta, "setAttr", False):
            return meta.setAttr(self.obj + "." + self.val, *args, **kwargs)

        if getattr(meta, "hda", False):
            parm = meta.node(self.obj).parm(self.val) or meta.node(self.obj).parmTuple(
                self.val
            )
            return parm.set(
                args[0].tolist() if hasattr(args[0], "T") else args[0], **kwargs
            )

        if getattr(meta, "runtime", False):
            if ":" in str(self._values[0]):
                return setattr(self._values[0], self.val, args[0])
            else:
                return setattr(meta.runtime.getnodebyname(self.obj), self.val, args[0])

        if getattr(meta, "data", False):
            return setattr(
                meta.data.objects[self.obj],
                self.val,
                args[0].tolist() if hasattr(args[0], "T") else args[0],
            )

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setValue(args[0], **kwargs)

        if getattr(meta, "fusion", False):
            return setattr(
                meta.fusion.GetCurrentComp().FindTool(self.obj), self.val, args[0])

        if getattr(meta, "doc", False):
            try:
                return getattr(meta.doc.layers[self.obj], self.val)(*args, **kwargs)
            except TypeError:
                try:
                    return setattr(
                        meta.doc.layers[self.obj], self.val, args[0]
                    )
                except TypeError:
                    return meta.ps.Document().layers[self.obj].setValue_forKey_(args[0], self.val)

        if getattr(meta, "wind_type", False):
            return meta.module._MarvelousDesigner__module_obj.SaveFile(*args, **kwargs)

        if getattr(meta, "uclass", False):
            try:
                return meta.ue4.uname(self.obj).set_editor_property(self.val, args[0])
            except TypeError:
                return getattr(meta.ue4.uname(self.obj), self.val)(*args, **kwargs)
            except:
                return meta.ue4.uname(self.obj).root_component.set_editor_property(
                    self.val, args[0]
                )

        raise YException

    @staticmethod
    def add(self):
        pass

    @staticmethod
    def des(self):
        pass

    @trace
    def lock(self, on):
        if getattr(meta, "setAttr", False):
            return meta.setAttr(self.obj + "." + self.val, lock=on)

        if getattr(meta, "hda", False):
            return meta.node(self.obj).parm(self.val).lock(on)

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setEnabled(on)

        raise YException

    @trace
    def hide(self, on=True):
        if getattr(meta, "setAttr", False):
            return meta.setAttr(
                self.obj + "." + self.val, keyable=not on, channelBox=not on
            )

        if getattr(meta, "hda", False):
            return meta.node(self.obj).parm(self.val).hide(on)

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setVisible(not on)

        raise YException

    @property
    def vector(self):
        try:
            return YVector(self._values[0])
        except TypeError:
            return YVector(*self._values[0])

    @property
    def color(self):
        try:
            return YColor(self._values[0])
        except TypeError:
            return YColor(*self._values[0])

    @property
    def matrix(self):
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

        if getattr(meta, "sbs", False):
            return cls(meta.manager.loadUserPackage(*args, **kwargs))

        if getattr(meta, "doc", False):
            return meta.Open(*args, **kwargs)

        if getattr(meta, "wind_type", False):
            return meta.module._MarvelousDesigner__module_obj.OpenFile(*args, **kwargs)

        if getattr(meta, "file", False):
            return cls(partial(meta.file, i=1)(*args, **kwargs))

        if getattr(meta, "hipFile", False):
            return cls(meta.hipFile.load(*args, **kwargs))

        if getattr(meta, "runtime", False):
            if meta.runtime.loadMaxFile(*args, **kwargs):
                return cls(args[0])

        if getattr(meta, "data", False):
            return cls(meta.ops.wm.open_mainfile(*args, **kwargs))

        if getattr(meta, "knob", False):
            return meta.scriptOpen(*args, **kwargs)

        if getattr(meta, "fusion", False):
            storage = meta.resolve.GetMediaStorage()
            if "." in args:
                return storage.AddItemsToMediaPool(*args)
            else:
                return meta.manager.LoadProject(*args, **kwargs)

        if getattr(meta, "uclass", False):
            return cls(file.abcImporter(*args, **kwargs))

        raise YException

    @classmethod
    def save(cls, *args, **kwargs):
        from yurlungur.core.command import file

        if args[0].endswith("abc"):
            return cls(file.abcExporter(*args, **kwargs))

        if args[0].endswith("fbx"):
            return cls(file.fbxExporter(*args, **kwargs))

        if getattr(meta, "sbs", False):
            return cls(meta.manager.savePackageAs(*args, **kwargs))

        if getattr(meta, "doc", False):
            if args[0].endswith(".psd"):
                return meta.doc.Save()
            else:
                return meta.doc.SaveAs(*args, **kwargs)

        if getattr(meta, "wind_type", False):
            return meta.module._MarvelousDesigner__module_obj.SaveFile(*args, **kwargs)

        if getattr(meta, "file", False):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if getattr(meta, "hipFile", False):
            return cls(meta.hipFile.save(*args, **kwargs))

        if getattr(meta, "runtime", False):
            if meta.runtime.saveMaxFile(*args, **kwargs):
                return cls(args[0])

        if getattr(meta, "data", False):
            return meta.ops.wm.save_mainfile(*args, **kwargs)

        if getattr(meta, "knob", False):
            return meta.scriptSave(*args, **kwargs)

        if getattr(meta, "fusion", False):
            return meta.manager.SaveProject(*args, **kwargs)

        if getattr(meta, "uclass", False):
            return meta.tools.export_assets(*args, **kwargs)

        raise YException

    @property
    def current(self):
        if getattr(meta, "sbs", False):
            return meta.manager.getUserPackageFromFilePath()

        if getattr(meta, "doc", False):
            try:
                return os.path.join(meta.doc.path, meta.doc.name)
            except AttributeError:
                return meta.doc.filePath().absoluteString()

        if getattr(meta, "wind_type", False):
            return meta.module._MarvelousDesigner__module_obj.GetSaveFilePath()

        if getattr(meta, "file", False):
            return meta.file(exn=1, q=1)

        if getattr(meta, "hipFile", False):
            return meta.hipFile.path()

        if getattr(meta, "runtime", False):
            return meta.runtime.maxFilePath + meta.runtime.maxFileName

        if getattr(meta, "data", False):
            return meta.data.filepath

        if getattr(meta, "knob", False):
            return meta.scriptName()

        if getattr(meta, "fusion", False):
            return meta.manager.GetCurrentProject()

        if getattr(meta, "uclass", False):
            if self.path:
                return meta.assets.find_asset_data(self.path).package_path
            else:
                return meta.assets.list_assets(
                    "/Game", recursive=True, include_folder=True)

        raise YException

    def reference(self):
        raise YException
