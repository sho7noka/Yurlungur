# -*- coding: utf-8 -*-
import contextlib
import functools

from yurlungur.tool.meta import meta
from yurlungur.core import env


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
        elif env.Davinci():
            meta.fusion.StartUndo()

    def __exit__(self, exc_type, exc_value, traceback):
        if env.Maya():
            meta.undoInfo(cck=1)
        elif env.Blender():
            meta.context.user_preferences.edit.use_global_undo = self.undo
        elif env.Davinci():
            meta.fusion.EndUndo()


if env.Houdini():
    UndoGroup = meta.undos.group

if env.Unreal():
    UndoGroup = meta.ScopedEditorTransaction

if env.Max():
    UndoGroup = functools.partial(meta.undo, True)

if env.Nuke():
    UndoGroup = meta.Undo
