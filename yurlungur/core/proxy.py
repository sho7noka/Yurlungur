# -*- coding: utf-8 -*-
import os, inspect
from functools import partial

from yurlungur.core.deco import trace
from yurlungur.core.wrapper import YObject
from yurlungur.tool.meta import meta
from yurlungur.core.vars import ref


class Object(YObject):
    """document base object
    >>> cone = Object("pCone")
    >>> cone.set("my_cone")
    >>> cone.castShadows.set(True)
    >>> # or
    >>> cone.attr("castShadows").set(True)
    >>> cone.delete()
    """

    def __init__(self, item):
        self.item = item

    def __dir__(self):
        return self.attrs

    def __getattr__(self, val):
        if val in self.attrs:
            return self.attr(val)
        else:
            from yurlungur.core.command import _NodeType
            return _NodeType()

    @property
    def name(self):
        if getattr(meta, "SDNode", False):
            return self.id
        elif getattr(meta, "hda", False):
            return self.item.name
        else:
            return self.item

    @property
    def id(self):
        if getattr(meta, "SDNode", False):
            node_id = ""
            for node in meta.graph.getNodes():
                d = node.getDefinition()
                if (d.getId() == self.item or d.getLabel() == self.item or node.getIdentifier() == self.item):
                    node_id = node.getIdentifier()
                    break
            return node_id if node_id else meta.graph.getIdentifier()

        if getattr(meta, "ls", False):
            return meta.ls(self.name, uuid=1)[0] or 0

        if getattr(meta, "hda", False):
            return meta.node(self.name).sessionId() or 0

        if getattr(meta, "knob", False):
            return meta.toNode(self.name)["name"].value() or 0

        if getattr(meta, "C4DAtom", False):
            return meta.doc.SearchObject(self.item).GetGUID()

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ID or 0

        if getattr(meta, "data", False):
            return meta.data.objects[self.name].id_data or 0

        if getattr(meta, "uclass", False):
            return meta.unreal.uname(self.name).get_name() or 0

        if getattr(meta, "Debug", False):
            return meta.engine.GameObject.Find(self.name).GetInstanceID() or 0

        if getattr(meta, "doc", False):
            return meta.eval("""
            var ref = new ActionReference();
            ref.putEnumerated(charIDToTypeID('Lyr '), charIDToTypeID('Ordn'), charIDToTypeID('Trgt')); // reference is active layer
            var layerDesc = executeActionGet(ref);
            var layerID = layerDesc.getInteger(stringIDToTypeID('layerID'));layerID;""")
        
        if getattr(meta, "runtime", False):
            return meta.runtime.getnodebyname(self.name).gbufferChannel or 0

        if getattr(meta, "lx", False):
            return meta.Scene().item(self.name).id

        if getattr(meta, "SceneObject", False):
            return meta.findObject(self.name).uid
        

    def set(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            meta.graph.setIdentifier(args[0])
            return Node(args[0])

        if getattr(meta, "rename", False):
            return meta.rename(self.item, *args, **kwargs)

        if getattr(meta, "hda", False):
            return meta.node(self.item).setName(*args, **kwargs)

        if getattr(meta, "knob", False):
            return meta.toNode(self.item).setName(args[0], **kwargs)

        if getattr(meta, "C4DAtom", False):
            return meta.doc.SearchObject(self.item).SetName(args[0])

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                return (
                    meta.fusion.GetCurrentComp()
                        .FindTool(self.item)
                        .SetAttrs({"TOOLS_Name": args[0]})
                )
            else:
                return meta.davinci.Projects()[self.item]

        if getattr(meta, "data", False):
            meta.data.objects[self.item].name = "".join(args)
            return "".join(args)

        if getattr(meta, "uclass", False):
            uname = meta.unreal.uname(self.name)
            if type(uname) == str:
                meta.assets.rename_asset(
                    uname, os.path.join(os.path.dirname(uname), args[0])
                )
                return Node(args[0])
            else:
                return uname.set_actor_label(args[0])

        if getattr(meta, "doc", False):
            try:
                return setattr(meta.doc.activeLayer, "name", args[0])
            except AttributeError:
                return meta.doc.currentLayer().setValue_forKey_(args[0], "name")

        if getattr(meta, "runtime", False):
            meta.runtime.getnodebyname(self.name).name = args[0]
            return Node(args[0])

        if getattr(meta, "lx", False):
            meta.Scene().item(self.name).name = args[0]
            return Node(args[0])

        if getattr(meta, "SceneObject", False):
            meta.findObject(args[0]).name = args[1]
            return meta.findObject(args[1])

    @trace
    def attr(self, val, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            prop = meta.graph.getNodeFromId(self.name).getPropertyFromId(
                val, meta.sd.SDPropertyCategory.Input)
            return Attribute(
                meta.graph.getNodeFromId(self.name).getPropertyValue(prop).get(),
                self.name, val, )

        if getattr(meta, "ls", False):
            return Attribute(
                meta.getAttr(self.name + "." + val, *args, **kwargs), self.name, val
            )

        if getattr(meta, "hda", False):
            parm = meta.node(self.name).parm(val) or meta.node(self.name).parmTuple(val)
            return Attribute(parm.eval(), self.name, val)

        if getattr(meta, "knob", False):
            return Attribute(meta.toNode(self.name)[val], self.name, val)

        if getattr(meta, "C4DAtom", False):
            return Attribute(
                meta.doc.SearchObject(self.name)[getattr(meta, val)], self.name, val)

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                return Attribute(
                    getattr(meta.fusion.GetCurrentComp().FindTool(self.name), val), self.name, val
                )
            else:
                return Attribute

        if getattr(meta, "data", False):
            return Attribute(meta.data.objects[self.name].name, self.name, val)

        if getattr(meta, "uclass", False):
            try:
                return Attribute(
                    meta.unreal.uname(self.name).get_editor_property(val), self.name, val
                )
            except:
                return Attribute(
                    meta.unreal.uname(self.name).root_component.get_editor_property(val),
                    self.name, val
                )

        if getattr(meta, "doc", False):
            try:
                layer = meta.doc.layers[self.name]
            except TypeError:
                layer = meta.ps.Document().layers[self.name]

            return Attribute(getattr(layer, val), self.name, val)

        if getattr(meta, "runtime", False):
            return Attribute(
                getattr(meta.runtime.getnodebyname(self.name), val), self.name, val)

        if getattr(meta, "lx", False):
            return Attribute(getattr(meta.Scene().item(self.name), val), self.name, val)

        if getattr(meta, "SceneObject", False):
            return Attribute(meta.findObject(val), self.name, val)

    @property
    def attrs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return (prop.getId() for prop in
                    meta.graph.getNodeFromId(self.name).getProperties(
                        meta.sd.SDPropertyCategory.Input
                    ))

        if getattr(meta, "listAttr", False):
            return tuple(meta.listAttr(self.name, *args, **kwargs) or [])

        if getattr(meta, "hda", False):
            return (p.name() for p in meta.node(self.name).parms() or [])

        if getattr(meta, "knob", False):
            return (knob.name() for knob in meta.toNode(self.name).allKnobs())

        if getattr(meta, "C4DAtom", False):
            attrs = []
            ids = {}  # {v.lower(): v for v in dir(app.application) if v.isupper()}
            for k, v in ids.items():
                try:
                    meta.doc.SearchObject(self.name)[getattr(meta, v)]
                    attrs.append(k)
                except AttributeError:
                    pass
            return tuple(attrs)

        if getattr(meta, "fusion", False):
            return tuple(meta.fusion.GetCurrentComp().FindTool(self.name).GetAttrs())

        if getattr(meta, "data", False):
            return tuple(inspect.getmembers(meta.data.objects[self.name]))

        if getattr(meta, "uclass", False):
            return meta.unreal.uname(self.name).component_tags()

        if getattr(meta, "doc", False):
            try:
                return (p for p, _ in inspect.getmembers(meta.photoshop.Photoshop.ArtLayer) if "_" not in p)
            except AttributeError:
                return (k for k in meta.ps.Document()._doc.layers()[0].properties())

        if getattr(meta, "runtime", False):
            return tuple(inspect.getmembers(meta.runtime.getnodebyname(self.name)))

        if getattr(meta, "lx", False):
            return (attr for attr in dir(meta.Scene().item(self.name)) if not attr.startswith("__"))

        if getattr(meta, "SceneObject", False):
            return (attr for attr in dir(meta.findObject(args[0])) if not attr.startswith("__"))

    @trace
    def create(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            node_id = (
                args[0] if "::" in args[0] else "::".join(["sbs", "compositing", args[0]])
            )
            return Node(meta.graph.newNode(node_id).getIdentifier())

        # maya and nuke
        if getattr(meta, "createNode", False):
            return Node(meta.createNode(*args, **kwargs))

        if getattr(meta, "hda", False):
            if len(args) == 0 and len(kwargs) == 0:
                return Node(
                    partial(meta.node(self.name).createNode, self.name)(*args, **kwargs).path()
                )
            return Node(meta.node(self.name).createNode(*args, **kwargs).path())

        if getattr(meta, "C4DAtom", False):
            if args[0][0] == "O":  # object
                obj = meta.BaseObject(getattr(meta, args[0]))
                meta.doc.InsertObject(obj)

            if args[0][0] == "T":  # tag
                obj = meta.doc.SearchObject(self.name).MakeTag(getattr(meta, args[0]))

            if args[0][0] == "M":  # material
                obj = meta.BaseMaterial(getattr(meta, args[0]))
                meta.doc.InsertMaterial(obj)

            meta.EventAdd()
            return Node(obj.GetName())

        if getattr(meta, "fusion", False):
            return Node(meta.fusion.GetCurrentComp().AddTool(*args, **kwargs).Name)

        if getattr(meta, "data", False):
            if self.name:
                self.select(self.name)
                return meta.ops.object.modifier_add(type=str(args[0]).upper())
            else:
                try:
                    return getattr(meta.ops.mesh, args[0] + "_add")(*args[1:], **kwargs)
                except AttributeError:
                    return partial(meta.ops.object.add, type=str(args[0]).upper())(*args[1:], **kwargs)

        if getattr(meta, "uclass", False):
            factory = getattr(meta, self.name + "Factory")
            if not args:
                args = (self.name, "/Game", None)

            assert len(args) == 3 and factory

            new_asset = partial(meta.tools.create_asset, *args)(factory(), **kwargs)
            if new_asset:
                meta.assets.save_loaded_asset(new_asset)
                return Node(new_asset.get_name())
            else:
                return

        if getattr(meta, "doc", False):
            try:
                ps = getattr(meta.photoshop.Photoshop, "ps%s" % args[0], meta.doc.psNormalLayer)
                layer = meta.doc.artLayers.Add()
                layer.name = self.name
                return setattr(layer, "Kind", ps)
            except AttributeError:
                _ = kwargs.update({"name": self.name})
                layer = meta.classForScriptingClass_("art layer").alloc().initWithProperties_(kwargs)
                meta.ps.Document()._doc.artLayers().addObject_(layer)
                return Object(self.name)

        if getattr(meta, "runtime", False):
            obj = getattr(meta.runtime, args[0])
            msx_class = meta.runtime.classOf(obj)
            _obj = obj(**kwargs)

            if str(msx_class) == "modifier":
                meta.runtime.addModifier(meta.runtime.getnodebyname(self.name), _obj)
                return Node(
                    meta.runtime.getnodebyname(self.name).name + "." + _obj.name
                )

            elif str(msx_class) == "material":
                meta.runtime.material = _obj

            return Node(_obj.name)

        if getattr(meta, "lx", False):
            obj = {
                "actor": meta.current().addActor, "camera": meta.current().addCamera, "group": meta.current().addGroup,
                "item": meta.current().addItem, "joint": meta.current().addJointLocator, "material": meta.current().addMaterial,
                "mesh": meta.current().addMesh, "render": meta.current().addRenderPassGroup, "shader": meta.current().addShaderItem
            }[args[0]](*args[1:])
            return Object(obj.name)

        if getattr(meta, "SceneObject", False):
            obj = {
                "mesh": meta.MeshObject, "material": meta.Material,
                "light": meta.LightObject, "camera": meta.CameraObject, "fog": meta.FogObject,
            }[args[0]](*args[1:])
            return Object(obj.name)

    @trace
    def delete(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return meta.graph.deleteNode(meta.graph.getNodeFromId(self.name))

        # maya and nuke
        if getattr(meta, "delete", False):
            node = meta.toNode(self.name) if getattr(meta, "knob") else self.name
            return meta.delete(node, *args, **kwargs)

        if getattr(meta, "hda", False):
            return meta.node(self.name).destroy()

        if getattr(meta, "C4DAtom", False):
            return meta.doc.SearchObject(self.item).Remove()

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                return meta.fusion.GetCurrentComp().FindTool(self.name).Delete()
            else:
                return meta.davinci

        if getattr(meta, "data", False):
            return meta.context.collection.objects.unlink(meta.data.objects[self.name])

        if getattr(meta, "uclass", False):
            uname = meta.unreal.uname(self.name)
            if type(uname) == str:
                return meta.assets.delete_asset(uname)
            else:
                return uname.destroy_actor()

        if getattr(meta, "doc", False):
            try:
                return meta.doc.layers[self.name].delete()
            except TypeError:
                return meta.ps.Document().layers[self.name].delete()

        if getattr(meta, "runtime", False):
            return meta.runtime.delete(meta.runtime.getnodebyname(self.name))

        if getattr(meta, "lx", False):
            meta.Scene().select(meta.Scene().item(self.name))
            return meta.lx.eval("item.delete")

        if getattr(meta, "SceneObject", False):
            return meta.findObject(self.name).destroy()

    @trace
    def instance(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            return meta.graph.newInstanceNode(self.name, *args, **kwarg)

        if getattr(meta, "instance", False):
            if len(args) > 0:
                return meta.instance(self.name, lf=1)
            else:
                return meta.listRelatives(self.name, ap=1, f=1)[1:] or None

        if getattr(meta, "hda", False):
            return meta.node(self.name).copyTo(*args, **kwarg)

        if getattr(meta, "knob", False):
            if len(args) > 0:
                return meta.clone(meta.toNode(self.name), *args, **kwarg)
            else:
                return meta.toNode(self.name).clones()

        if getattr(meta, "C4DAtom", False):
            obj = meta.InstanceObject()
            obj.SetReferenceObject(meta.doc.SearchObject(self.name))
            meta.doc.InsertObject(obj)
            return obj.GetName()

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                meta.fusion.GetCurrentComp().Copy(self.name)
                return meta.fusion.GetCurrentComp().Paste(*args, **kwarg)
            else:
                meta.davinci

        if getattr(meta, "data", False):
            return meta.ops.object.make_local(type='SELECT_OBJECT')

        if getattr(meta, "uclass", False):
            uname = meta.unreal.uname(self.name)
            if type(uname) == str:
                return meta.assets.duplicate_asset(
                    uname, os.path.join(os.path.dirname(uname), *args)
                )
            else:
                return

        if getattr(meta, "doc", False):
            try:
                return meta.doc.layers[self.name].duplicate()
            except TypeError:
                return meta.ps.Document().layers[self.name].duplicate()

        if getattr(meta, "runtime", False):
            return Node(
                meta.runtime.instance(meta.runtime.getnodebyname(self.name)).name
            )

        if getattr(meta, "lx", False):
            return meta.Scene().duplicateItem(meta.Scene().item(self.name), instance=True)

        if getattr(meta, "SceneObject", False):
            return Object(meta.findObject(self.name).duplicate(args[0]).name)

    @trace
    def select(self, *args, **kwargs):
        from yurlungur.core.command import node

        if getattr(meta, "SDNode", False):
            return node.sel

        if getattr(meta, "select"):
            if "shape" not in kwargs and "s" not in kwargs:
                kwargs["s"] = True

            if len(args) == 0 and len(kwargs) == 0:
                return node.sel
            else:
                return meta.select(*args, **kwargs)

        if getattr(meta, "hda", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.sel
            else:
                return meta.node(self.name).setCurrent(*args, **kwargs)

        if getattr(meta, "knob", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.sel
            else:
                return meta.toNode(self.name).setSelected()

        if getattr(meta, "C4DAtom", False):
            if len(args) == 0 and len(kwargs) == 0:
                meta.doc.SetActiveObject(meta.doc.SearchObject(args[0]), meta.SELECTION_NEW)
            return meta.doc.GetActiveObject().GetName()

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                if len(args) == 0 and len(kwargs) == 0:
                    return meta.fusion.GetCurrentComp().GetToolList(True)
                else:
                    return meta.fusion.GetCurrentComp().CurrentFrame.FlowView.Select(
                        *args, **kwargs
                    )
            else:
                return meta.davinci

        if getattr(meta, "data", False):
            if len(args) == 0 and len(kwargs) == 0:
                # return meta.context.view_layer.objects.selected
                return node.sel
            else:
                return meta.ops.object.select_pattern(pattern=self.name)

        if getattr(meta, "uclass", False):
            uname = meta.unreal.uname(self.name)
            if len(args) == 0 and len(kwargs) == 0:
                if type(uname) == str:
                    return node.sel
                else:
                    return (
                        Node(asset.get_name())
                        for asset in meta.editor.get_selection_set()
                    )
            else:
                if type(uname) == str:
                    return
                else:
                    return meta.editor.set_actor_selection_state(uname, *args)

        if getattr(meta, "doc", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.sel
            else:
                try:
                    return setattr(
                        meta.doc, "ActiveLayer", meta.doc.artLayers[self.name],
                    )
                except TypeError:
                    return meta.doc.currentLayer().setTo_(meta.ps.Document().layers[self.name])

        if getattr(meta, "runtime", False):
            if len(args) == 0 and len(kwargs) == 0:
                return node.sel
            else:
                return meta.runtime.select(meta.runtime.getnodebyname(self.name))

        if getattr(meta, "lx", False):
            if len(args) == 0 and len(kwargs) == 0:
                return meta.Scene().selected
            else:
                return meta.Scene().select(meta.Scene().item(self.name))

        if getattr(meta, "SceneObject", False):
            return node.sel

    @trace
    def hide(self, on=True):
        if getattr(meta, "C4DAtom", False):
            return setattr(
                meta.doc.SearchObject(self.item)[meta.ID_BASEOBJECT_VISIBILITY_EDITOR], on)

        if getattr(meta, "fusion", False):
            return (meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .SetAttrs({"TOOLB_PassThrough": on, "TOOLB_Locked": False})
                    )

        if getattr(meta, "data", False):
            return setattr(meta.data.objects[self.name], "hide_viewport", on)

        if getattr(meta, "uclass", False):
            return meta.unreal.uname(self.name).root_component.set_editor_property(
                "visible", not on
            )

        if getattr(meta, "doc", False):
            try:
                return setattr(meta.doc.layers[self.name], "visible", not on)
            except TypeError:
                return meta.ps.Document().layers[self.name].setValue_forKey_(not on, "visible")

        if getattr(meta, "runtime", False):
            return getattr(meta.runtime, "hide" if on else "unhide")(
                meta.runtime.getnodebyname(self.name)
            )

        if getattr(meta, "lx", False):
            self.select(self.name)
            return meta.lx.eval("item.channel locator$visible %s" % "on" if on else "off")

        if getattr(meta, "SceneObject", False):
            return setattr(meta.findObject(self.name), "visible", not on)


    @trace
    def parent(self, *args, **kwarg):
        if getattr(meta, "data", False):
            if len(args) > 0:
                return setattr(meta.data.objects[self.item], "parent", meta.data.objects[args[0]])
            else:
                return Object(meta.data.objects[self.item].parent.name)

        if getattr(meta, "uclass", False):
            if len(args) > 0:
                return
            else:
                return Object(meta.unreal.uname(self.name).get_parent_actor().get_name())

        if getattr(meta, "doc", False):
            if len(args) > 0:
                return
            else:
                return Object(meta.doc.artLayers[self.name].parent.name)

        if getattr(meta, "runtime", False):
            if len(args) > 0:
                meta.runtime.getnodebyname(self.item).parent = args[0]
                return Object(args[0])
            else:
                _parent = meta.runtime.getnodebyname(self.item).parent
                return Object(_parent.name) if _parent else None

        if getattr(meta, "SceneObject", False):
            if len(args) > 0:
                meta.findObject(self.name).parent = meta.findObject(args[0])
                return Object(meta.findObject(args[0]))
            else:
                return Object(meta.findObject(self.name).parent.name)

    @trace
    def children(self):
        if getattr(meta, "data", False):
            children = []
            for obj in meta.data.objects:
                if obj.parent == meta.data.objects[self.item]:
                    children.append(obj)
            return (Object(obj.name) for obj in children)

        if getattr(meta, "uclass", False):
            return (
                Object(actor.get_name())
                for actor in meta.unreal.uname(self.item).get_all_child_actors()
            )

        if getattr(meta, "doc", False):
            return (
                Object(layer.name) for layer in meta.doc.LayerSets[self.item].layers
            )

        if getattr(meta, "runtime", False):
            nodes = []
            children = meta.runtime.getnodebyname(self.item).children
            for i in range(children.count):
                nodes.append(children[i].name)
            return (Object(node.name) for node in nodes)

        if getattr(meta, "SceneObject", False):
            return (
                Object(obj.name) for obj in meta.findObject(self.name).getChildren()
            )

    @trace
    def sequence(self):
        if getattr(meta, "fusion", False):
            return meta.davinci.Timeline

        if getattr(meta, "knob", False):
            index = meta.toNode(self.name).inputs() - 1
            return Node(meta.toNode(self.name).input(index).name())

        if getattr(meta, "data", False):
            from yurlungur.adapters import blender
            return blender.Timeline(self.name)

        if getattr(meta, "uclass", False):
            return meta.unreal.Timeline(self.name)
        
        if getattr(meta, "SceneObject", False):
            from yurlungur.adapters import toolbag
            return toolbag.Timeline()
        

class Node(Object):
    """relationship object"""

    def __init__(self, item=None):
        super(Node, self).__init__(item)
        self.item = item
        if self.item and getattr(meta, "SDNode", False):
            self._inputs = meta.graph.getNodeFromId(self.name).getProperties(meta.sd.SDPropertyCategory.Input)
            self._outputs = meta.graph.getNodeFromId(self.name).getProperties(meta.sd.SDPropertyCategory.Output)

    @trace
    def parent(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            nodes = []
            for prop in self._inputs:
                for connect in meta.graph.getNodeFromId(
                        self.name
                ).getPropertyConnections(prop):
                    nodes.append(Node(connect.getInputPropertyNode().getIdentifier()))
            return nodes

        if getattr(meta, "ls", False):
            if len(args) == 0 and len(kwarg) > 0:
                return meta.parent(self.item, *args, **kwarg)
            else:
                return Node(
                    partial(meta.listRelatives, self.item, p=1)(*args, **kwarg)
                )

        if getattr(meta, "hda", False):
            return Node(meta.node(self.item).parent().path())

        if getattr(meta, "knob", False):
            return Node(".".join(meta.toNode(self.name).fullName().split(".")[:-1]))

        if getattr(meta, "fusion", False):
            return meta.fusion.GetCurrentComp().FindTool(self.name).ParentTool

    def children(self, *args, **kwarg):
        if getattr(meta, "SDNode", False):
            nodes = []
            for prop in self._outputs:
                for connect in meta.graph.getNodeFromId(
                        self.name
                ).getPropertyConnections(prop):
                    nodes.append(Node(connect.getOutputPropertyNode().getIdentifier()))
            return nodes

        if getattr(meta, "ls", False):
            return partial(meta.listRelatives, self.item, c=1)(*args, **kwarg) or None

        if getattr(meta, "hda", False):
            return [Node(node.name) for node in meta.node(self.item).children()]

        if getattr(meta, "knob", False):
            return 

        if getattr(meta, "fusion", False):
            # group or macro
            return [Node(v) for v in meta.fusion.GetCurrentComp().ActiveTool.GetChildrenList(*args, **kwarg).values()]
        
    @trace
    def connect(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            args = (args[0], meta.graph.getNodeFromId(args[1].id), args[2])
            return (
                meta.graph.getNodeFromId(self.name)
                    .newPropertyConnectionFromId(*args)
                    .getClassName()
            )

        if getattr(meta, "ls"):
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

        if hasattr(meta, "ls"):
            return partial(
                meta.disconnectAttr, self.name + "." + args[0])(args[1:], **kwargs)

        if getattr(meta, "hda", False):
            return partial(meta.node(self.name).setInput, 0, None)(*args, **kwargs)

        if getattr(meta, "knob", False):
            return meta.toNode(self.name).setInput(0, None)

        if getattr(meta, "fusion", False):
            return setattr(
                meta.fusion.GetCurrentComp().FindTool(self.name), "Input", None)

    @trace
    def inputs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return [
                connect.getId() for connect in self._inputs if connect.isConnectable()
            ]

        if hasattr(meta, "ls"):
            return partial(meta.listConnections, s=1)(*args, **kwargs)

        if getattr(meta, "hda", False):
            return [Node(node.name) for node in meta.node(self.name).inputs()]

        if getattr(meta, "knob", False):
            return [
                Node(meta.toNode(self.name).input(index).name()) for index in range(meta.toNode(self.name).inputs())
            ]

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .GetInputList()
                    .values()[0].GetAttrs()
            )

    @trace
    def outputs(self, *args, **kwargs):
        if getattr(meta, "SDNode", False):
            return [
                connect.getId() for connect in self._outputs if connect.isConnectable()
            ]

        if hasattr(meta, "ls"):
            return partial(meta.listConnections, d=1)(*args, **kwargs)

        if getattr(meta, "hda", False):
            return [Node(node.name) for node in meta.node(self.name).outputs()]

        if getattr(meta, "knob", False):
            return meta.toNode(self.name).dependencies(meta.EXPRESSIONS)

        if getattr(meta, "fusion", False):
            return (
                meta.fusion.GetCurrentComp()
                    .FindTool(self.name)
                    .GetOutputList()
                    .values()[0].GetAttrs()
            )


# @total_ordering
class Attribute(YObject):
    """parametric object"""
    def __init__(self, *args):
        if len(args) == 0:
            self._values = [None, "none", 0]
        else:
            assert len(args) > 2, "parameter is invalid."
            self._values = args
            self.obj, self.val = self._values[1:]

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
            return meta.setAttr(
                self.obj + "." + self.val, *args, **kwargs)

        if getattr(meta, "hda", False):
            parm = meta.node(self.obj).parm(self.val) or meta.node(self.obj).parmTuple(
                self.val
            )
            return parm.set(
                args[0].tolist() if hasattr(args[0], "T") else args[0], **kwargs
            )

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setValue(args[0], **kwargs)

        if getattr(meta, "C4DAtom", False):
            meta.doc.SearchObject(self.obj)[getattr(meta, self.val)] = args[0]
            return args[0]

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                return setattr(
                    meta.fusion.GetCurrentComp().FindTool(self.obj), self.val, args[0])
            else:
                return meta.davinci

        if getattr(meta, "data", False):
            return setattr(
                meta.data.objects[self.obj], self.val,
                args[0].tolist() if hasattr(args[0], "T") else args,
            )

        if getattr(meta, "uclass", False):
            try:
                return meta.unreal.uname(self.obj).set_editor_property(self.val, args[0])
            except TypeError:
                return getattr(meta.unreal.uname(self.obj), self.val)(*args, **kwargs)
            except:
                return meta.unreal.uname(self.obj).root_component.set_editor_property(
                    self.val, args[0]
                )

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

        # http://help.autodesk.com/view/MAXDEV/2021/ENU/?guid=Max_Python_API_using_pymxs_pymxs_differences_pymxs_controllers_html
        if getattr(meta, "runtime", False):
            if ":" in str(self._values[0]):
                return setattr(self._values[0], self.val, args[0])
            else:
                return setattr(meta.runtime.getnodebyname(self.obj), self.val, args[0])

        if getattr(meta, "SceneObject", False):
            return setattr(meta.findObject(self.val), "", args[0])

        if getattr(meta, "lx", False):
            return setattr(meta.Scene().item(self.obj), self.val, args[0])

    @trace
    def create(self, *args, **kwargs):
        """
        create custom attribute
        >>> import yurlungur
        >>> Attribute(meta.data.objects[self.name].name, self.name, val)
        >>> attr = yurlungur.attr.create(yurlungur.node.ls()[0], "mName", "test")
        >>> yurlungur.attr.mName.delete() or attr.delete()
        """
        if getattr(meta, "ls", False):
            setattr(self, "ID", "ID")
            return meta.addAttr(self.obj, ln='ID', k=True)

        if getattr(meta, "hda", False):
            map_value = "%s -> %s" % ("ID", "ID".upper())
            if geo.findGlobalAttrib("ID") is None:
                geo.addAttrib(meta.attribType.Global, "ID", "")
            return geo.setGlobalAttribValue("ID", map_value)

        if getattr(meta, "knob", False):
            if type(self.val) == list:
                knob = "Array_Knob"
            if type(self.val) == int:
                knob = "WH_Knob"
            if type(self.val) == bool:
                knob = "Boolean_Knob"
            k = partial(meta, knob)("ID".lower(), "ID")
            return self.obj.addKnob(k)

        if getattr(meta, "data", False):
            self.obj["ID"] = str(self.val)
            return

        if getattr(meta, "runtime", False):
            attributes = '''attributes "ID"
            (
                parameters main rollout:params
                (
                    param1 type:#float ui:spinParam1 default:10 animateable:True
                )

                rollout params "Test Parameters"
                (
                    spinner spinParam1 "Param1" type:#float
                )
            )'''
            attr = meta.eval(attributes)
            t = meta.runtime.getnodebyname(self.obj)
            meta.runtime.custAttributes.add(t.baseObject, attr)
            partial(t, "ID").param1 = self.val
            return Attribute()

    @trace
    def delete(self, attr):
        """delete attribute"""
        assert type(attr) != Attribute, "arg is not Attribute Object"
        delattr(self, attr)

    @trace
    def lock(self, on=True):
        if getattr(meta, "ls", False):
            return meta.setAttr(self.obj + "." + self.val, lock=on)

        if getattr(meta, "hda", False):
            return meta.node(self.obj).parm(self.val).lock(on)

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setEnabled(not on)

    @trace
    def hide(self, on=True):
        if getattr(meta, "ls", False):
            return meta.setAttr(self.obj + "." + self.val, keyable=not on, channelBox=not on)

        if getattr(meta, "hda", False):
            return meta.node(self.obj).parm(self.val).hide(on)

        if getattr(meta, "knob", False):
            return meta.toNode(self.obj)[self.val].setVisible(not on)

    @property
    def vector(self):
        from yurlungur.core.datatype import Vector
        try:
            return Vector(self._values[0])
        except TypeError:
            return Vector(*self._values[0])

    @property
    def color(self):
        from yurlungur.core.datatype import Color
        try:
            return Color(self._values[0])
        except TypeError:
            return Color(*self._values[0])

    @property
    def matrix(self):
        from yurlungur.core.datatype import Matrix
        try:
            return Matrix(self._values[0])
        except TypeError:
            return Matrix(*self._values[0])


class File(YObject):
    """
    save, open and export
    """
    def __init__(self, path=""):
        self.file = path if path else self.current

    @property
    def name(self):
        if getattr(meta, "data", False):
            return meta.path.basename(self.file)
        else:
            return os.path.basename(self.file)

    @property
    def path(self):
        return os.path.dirname(self.file)

    @classmethod
    def open(cls, *args, **kwargs):
        if args[0].endswith("fbx") or args[0].endswith("usd"):
            from yurlungur.core.command import file
            im = getattr(file, os.path.splitext(args[0]), False)
            if im:
                return cls(im.Import(*args, **kwargs))

        if getattr(meta, "SDNode", False):
            return cls(meta.manager.loadUserPackage(*args, **kwargs))

        if getattr(meta, "ls", False):
            return cls(partial(meta.file, i=1)(*args, **kwargs))

        if getattr(meta, "hda", False):
            return cls(meta.hipFile.load(*args, **kwargs))

        if getattr(meta, "knob", False):
            return meta.scriptOpen(*args, **kwargs)

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                return meta.fusion
            else:
                storage = meta.resolve.GetMediaStorage()
                if "." in args:
                    return storage.AddItemsToMediaPool(*args)
                else:
                    return meta.manager.LoadProject(*args, **kwargs)

        if getattr(meta, "C4DAtom", False):
            meta.documents.LoadFile(*args)
            return cls(args[0])

        if getattr(meta, "data", False):
            return partial(meta.ops.wm.open_mainfile, filepath=args[0])(**kwargs)

        if getattr(meta, "doc", False):
            return meta.Open(*args, **kwargs)

        if getattr(meta, "runtime", False):
            if meta.runtime.loadMaxFile(*args, **kwargs):
                return cls(args[0])
            
        if getattr(meta, "lx", False):
            return meta.lx.eval('scene.open "%s" import' % args[0])

        if getattr(meta, "SceneObject", False):
            return meta.loadScene(*args)

        if getattr(meta, "textureset", False):
            return getattr(meta.project, "open" if args[0].endswith(".spp") else "create")(*args, **kwargs)

    @classmethod
    def save(cls, *args, **kwargs):
        if args[0].endswith("fbx") or args[0].endswith("usd"):
            from yurlungur.core.command import file
            ex = getattr(file, os.path.splitext(args[0]), False)
            if ex:
                return cls(ex.Export(*args, **kwargs))

        if getattr(meta, "SDNode", False):
            return cls(meta.manager.savePackageAs(*args, **kwargs))

        if getattr(meta, "ls", False):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if getattr(meta, "hda", False):
            return cls(meta.hipFile.save(*args, **kwargs))

        if getattr(meta, "knob", False):
            return meta.scriptSave(*args, **kwargs)

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                return meta.fusion
            else:
                return meta.manager.SaveProject(*args, **kwargs)

        if getattr(meta, "C4DAtom", False):
            meta.documents.SaveDocument(
                meta.doc, args[0], meta.SAVEDOCUMENTFLAGS_NONE, meta.FORMAT_C4DEXPORT
            )
            return cls(args[0])

        if getattr(meta, "data", False):
            return partial(meta.ops.wm.save_mainfile, filepath=args[0])(**kwargs)

        if getattr(meta, "runtime", False):
            if meta.runtime.saveMaxFile(*args, **kwargs):
                return cls(args[0])

        if getattr(meta, "doc", False):
            return meta.doc.Save() if args[0].endswith(".psd") else meta.doc.SaveAs(*args, **kwargs)
    
        if getattr(meta, "lx", False):
            return meta.lx.eval('scene.saveAs "%s" %s true' % args)

        if getattr(meta, "SceneObject", False):
            return meta.saveScene(*args)

        if getattr(meta, "textureset", False):
            if args[0].endswith(".spp"):
                return meta.project.save_as(*args, **kwargs)
            else:
                return meta.export.export_project_textures(**kwargs)

    @property
    def current(self):
        if getattr(meta, "SDNode", False):
            return meta.graph.getPackage().getFilePath()

        if getattr(meta, "ls", False):
            return meta.file(exn=1, q=1)

        if getattr(meta, "hda", False):
            return meta.hipFile.path()

        if getattr(meta, "knob", False):
            return meta.scriptName()

        if getattr(meta, "fusion", False):
            if meta.is_fusion:
                return meta.fusion
            else:
                return meta.davinci.Projects()

        if getattr(meta, "C4DAtom", False):
            return meta.doc.GetDocumentPath() + meta.doc.GetDocumentName()

        if getattr(meta, "data", False):
            return meta.data.filepath

        if getattr(meta, "uclass", False):
            if self.path:
                return meta.assets.find_asset_data(self.path).package_path
            else:
                return meta.assets.list_assets("/Game", recursive=True, include_folder=True)

        if getattr(meta, "runtime", False):
            return meta.runtime.maxFilePath + meta.runtime.maxFileName

        if getattr(meta, "doc", False):
            try:
                return os.path.join(meta.doc.path, meta.doc.name)
            except AttributeError:
                path = meta.doc.filePath()
                return path.absoluteString() if path else ""

        if getattr(meta, "lx", False):
            return meta.current().filename
            
        if getattr(meta, "SceneObject", False):
            return meta.getScenePath()

        if getattr(meta, "textureset", False):
            if meta.project.is_open():
                return meta.project.file_path()
            else:
                return None
