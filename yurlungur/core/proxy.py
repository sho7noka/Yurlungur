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
            id = ""
            for node in meta.graph.getNodes():
                d = node.getDefinition()
                if d.getId() == self.item or d.getLabel() == self.item or node.getIdentifier() == self.item:
                    id = node.getIdentifier()
                    break
            return id if id else meta.graph.getIdentifier()

        if hasattr(meta, "ls"):
            return meta.ls(self.name, uuid=1)[0] or 0

        if hasattr(meta, "root"):
            return meta.node(self.name).sessionId() or 0

        if hasattr(meta, "data"):
            return meta.data.objects[self.name].id_data or 0

        raise YException

    @trace
    def __call__(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            meta.graph.setIdentifier(args[0])

        if hasattr(meta, "rename"):
            return meta.rename(self.item, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.item).setName(*args, **kwargs)

        if hasattr(meta, "data"):
            meta.data.objects[self.item].name = "".join(args)

        if hasattr(meta, "script"):
            return meta.script[self.name].setName(args[0])

    @trace
    def __getattr__(self, val):
        if hasattr(meta, "SDNode"):
            prop = meta.graph.getNodeFromId(self.name).getPropertyFromId(val, meta.SDPropertyCategory.Input)
            return YAttr(meta.graph.getNodeFromId(self.name).getPropertyValue(prop).get(), self.name, val)

        if hasattr(meta, "getAttr"):
            return YAttr(meta.getAttr(self.name + "." + val), self.name, val)

        if hasattr(meta, "root"):
            parm = (meta.node(self.name).parm(val) or meta.node(self.name).parmTuple(val))
            return YAttr(parm.eval(), self.name, val)

        if hasattr(meta, "data"):
            return YAttr(meta.data.objects[self.name].name, self.name, val)

        if hasattr(meta, "script"):
            value = meta.script[self.name][val].getValue()
            return YAttr(meta.script[self.name], self.name, val)

        raise YException

    @trace
    def attr(self, val, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            prop = meta.graph.getNodeFromId(self.name).getPropertyFromId(val, meta.SDPropertyCategory.Input)
            return YAttr(meta.graph.getNodeFromId(self.name).getPropertyValue(prop).get(), self.name, val)

        if hasattr(meta, "getAttr"):
            return YAttr(meta.getAttr(self.name + "." + val, *args, **kwargs), self.name, val)

        if hasattr(meta, "root"):
            parm = (meta.node(self.name).parm(val) or meta.node(self.name).parmTuple(val))
            return YAttr(parm.eval(), self.name, val)

        if hasattr(meta, "data"):
            return YAttr(meta.data.objects[self.name].name, self.name, val)

        if hasattr(meta, "script"):
            value = meta.script[self.name][val].getValue()
            return YAttr(meta.script[self.name], self.name, val)

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

        if hasattr(meta, "root"):
            return tuple(p.name() for p in meta.node(self.name).parms() or [])

        if hasattr(meta, "data"):
            return inspect.getmembers(meta.data.objects[self.name])

        if hasattr(meta, "script"):
            return meta.script[self.name].values()

        raise YException

    @trace
    def create(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            node_id = args[0] if "::" in args[0] else "::".join(["sbs", "compositing", args[0]])
            return YNode(meta.graph.newNode(node_id).getIdentifier())

        if hasattr(meta, "createNode"):
            return YNode(meta.createNode(*args, **kwargs))

        if hasattr(meta, "root"):
            if len(args) == 0 and len(kwargs) == 0:
                return YNode(
                    partial(
                        meta.node(self.name).createNode, self.name
                    )(*args, **kwargs).path())
            return YNode(meta.node(self.name).createNode(*args, **kwargs).path())

        if hasattr(meta, "ops"):
            try:
                getattr(meta.ops.mesh, str(self).lower() + "_add")(*args, **kwargs)
            except AttributeError:
                getattr(meta.ops.object, str(self).lower() + "_add")(*args, **kwargs)

        if hasattr(meta, "script"):
            node = getattr(meta, self.name)(*args, **kwargs)
            meta.script.addChild(node)

        raise YException

    @trace
    def delete(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            return meta.graph.deleteNode(meta.graph.getNodeFromId(self.name))

        if hasattr(meta, "delete"):
            return meta.delete(self.name, *args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.name).destroy()

        if hasattr(meta, "context"):
            return meta.context.scene.objects.unlink(meta.data.objects[self.name])

        raise YException

    def instance(self, *args, **kwarg):
        if hasattr(meta, "SDNode"):
            return meta.graph.newInstanceNode(self.name, *args, **kwarg)

        if hasattr(meta, "instance"):
            if len(args) > 0:
                return meta.instance(self.name, lf=1)
            else:
                return meta.listRelatives(self.name, ap=1, f=1)[1:] or None

        raise YException

    def select(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            return

        if hasattr(meta, "select"):
            if 'shape' not in kwargs and 's' not in kwargs:
                kwargs['s'] = True

            if len(args) == 0 and len(kwargs) == 0:
                return meta.select(*args, **kwargs)
            else:
                return meta.ls(sl=1)

        if hasattr(meta, "script"):
            meta.script.selection().clear()
            for arg in args:
                meta.script.selection().add(meta.script[arg])

        raise YException

    @trace
    def hide(self, on=True):
        if hasattr(meta, "data"):
            meta.data.objects[self.name].hide = on

        raise YException

    @trace
    def geometry(self):
        if hasattr(meta, "ls"):
            dag = OM.MGlobal.getSelectionListByName(self.name).getDagPath(0)
            return OM.MFnMesh(dag)

        if hasattr(meta, "root"):
            return meta.node(self.name).geometry()

        if hasattr(meta, "data"):
            return meta.data.meshes[self.name]

        raise YException


class YNode(YObject):
    """relationship object"""

    def __init__(self, item=None):
        if sys.version_info > (3, 2):
            super().__init__(item)
        else:
            super(YNode, self).__init__(item)
        self.item = item

        if self.item and hasattr(meta, "SDNode"):
            self._inputs = meta.graph.getNodeFromId(self.name).getProperties(meta.SDPropertyCategory.Input)
            self._outputs = meta.graph.getNodeFromId(self.name).getProperties(meta.SDPropertyCategory.Output)

    def parent(self, *args, **kwarg):
        if len(args) > 0:
            return meta.parent(self.item, *args, **kwarg)

        elif len(args) == 0 and len(kwarg) > 0:
            return meta.parent(self.item, *args, **kwarg)

        else:
            if hasattr(meta, "SDNode"):
                nodes = []
                for prop in self._inputs:
                    for connect in meta.graph.getNodeFromId(self.name).getPropertyConnections(prop):
                        nodes.append(YNode(connect.getInputPropertyNode().getIdentifier()))
                return nodes

            if hasattr(meta, "getAttr"):
                return YNode(
                    partial(meta.listRelatives, self.item, p=1)(*args, **kwarg))

            if hasattr(meta, "root"):
                return YNode(meta.node(self.item).parent().name())

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

        if hasattr(meta, "root"):
            return YNode(meta.node(self.item).children())

        if hasattr(meta, ""):
            return YNode(script.children(Gaffer.Node))

        raise YException

    @trace
    def connect(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            args = (args[0], meta.graph.getNodeFromId(args[1].id), args[2])
            return meta.graph.getNodeFromId(self.name).newPropertyConnectionFromId(*args).getClassName()

        if hasattr(meta, "connectAttr"):
            return partial(meta.connectAttr, self.name + "." + args[0])(args[1:], **kwargs)

        if hasattr(meta, "root"):
            return partial(meta.node(self.name).setInput, 0)(*args, **kwargs)

        if hasattr(meta, ""):
            return destinationNode["destinationPlugName"].setInput(sourceNode["sourceNode"])

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

        if hasattr(meta, "root"):
            return partial(meta.node(self.name).setInput, 0, None)(*args, **kwargs)

        if hasattr(meta, ""):
            node["plugName"].setInput(None)

        raise YException

    @trace
    def inputs(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            return [connect.getId() for connect in self._inputs if connect.isConnectable()]

        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, s=1)(*args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.name).inputs()

        raise YException

    @trace
    def outputs(self, *args, **kwargs):
        if hasattr(meta, "SDNode"):
            return [connect.getId() for connect in self._outputs if connect.isConnectable()]

        if hasattr(meta, "listConnections"):
            return partial(meta.listConnections, d=1)(*args, **kwargs)

        if hasattr(meta, "root"):
            return meta.node(self.name).outputs()

        raise YException


@total_ordering
class YAttr(_YAttr):
    """parametric object"""

    def __init__(self, *args, **kwargs):
        assert len(args) > 2, "parameter is invalid."
        self._values = args
        self.obj, self.val = self._values[1:]

    @property
    def value(self):
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
            if type(self.value) == int:
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

        if hasattr(meta, "root"):
            parm = (meta.node(self.obj).parm(self.val) or
                    meta.node(self.obj).parmTuple(self.val))
            return parm.set(
                args[0].tolist() if hasattr(args[0], "T") else args[0], **kwargs)

        if hasattr(meta, "data"):
            return setattr(meta.data.objects[self.obj],
                           self.val, args[0].tolist() if hasattr(args[0], "T") else args[0])

        if hasattr(meta, "script"):
            return node["plugName"].setValue(*args, **kwargs)

        raise YException

    @trace
    def lock(self, on):
        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, lock=on)

        if hasattr(meta, "root"):
            return meta.node(self.obj).parm(self.val).lock(on)

        raise YException

    @trace
    def hide(self, on=True):
        if hasattr(meta, "setAttr"):
            return meta.setAttr(self.obj + "." + self.val, keyable=not on, channelBox=not on)

        if hasattr(meta, "root"):
            return meta.node(self.obj).parm(self.val).hide(on)

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

    def __init__(self, file=""):
        self.file = file

    @property
    def name(self):
        return os.path.basename(self.file)

    @property
    def path(self):
        return os.path.dirname(self.file)

    @classmethod
    def open(cls, *args, **kwargs):
        if hasattr(meta, "sbs"):
            return cls(meta.manager.loadUserPackage(*args, **kwargs))

        if hasattr(meta, "file"):
            return cls(partial(meta.file, i=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.load(*args, **kwargs))

        if hasattr(meta, "ops"):
            return cls(meta.ops.wm.open_mainfile(*args, **kwargs))

        if hasattr(meta, "script"):
            return cls(meta.script.importFile(*args, **kwargs))

        raise YException

    @classmethod
    def save(cls, *args, **kwargs):
        if hasattr(meta, "sbs"):
            return cls(meta.manager.savePackageAs(*args, **kwargs))

        if hasattr(meta, "file"):
            return cls(partial(meta.file, s=1)(*args, **kwargs))

        if hasattr(meta, "hipFile"):
            return cls(meta.hipFile.save(*args, **kwargs))

        if hasattr(meta, "ops"):
            return meta.ops.wm.save_mainfile(*args, **kwargs)

        if hasattr(meta, "script"):
            return meta.script.serialiseToFile(*args, **kwargs)

        raise YException

    @property
    def current(self):
        if hasattr(meta, "sbs"):
            return self(meta.manager.getUserPackageFromFilePath())

        if hasattr(meta, "file"):
            return self(meta.file(exn=1, q=1))

        if hasattr(meta, "hipFile"):
            return self(meta.hipFile.path())

        if hasattr(meta, "data"):
            return self(meta.data.filepath)

        if hasattr(meta, "script"):
            return self(meta.script["fileName"].getValue())

        raise YException

    def reference(cls):
        raise YException
