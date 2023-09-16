# coding: utf-8
import sys, contextlib
from yurlungur.core import env as _env

# dispatch for exit
if _env.Blender() or _env.Nuke() or _env.Houdini():
    sys.exit = None

# dispatch for RPC
try:
    from yurlungur.tool import rpc
    import rpyc
    rpc.session = rpyc.classic.connect

except ImportError:
    pass

from pxr import Usd
from yurlungur.core.command import File
usd = Usd

# maya houdini blender DaVinci Renderdoc
Gl = object

# dispatch for Qt
if _env.Qt():
    from yurlungur.user import Qt
    from yurlungur.tool import window as _window

    Qt.main_window = _window.main_window
    Qt.show = _window.show

# dispatch for app
try:
    from vfxwindow import VFXWindow as _UIWindow

    Qt.UIWindow = _UIWindow
    _UIWindow.c4d = _env.C4D()
    _UIWindow.toolbag = _env.Toolbag()
    _UIWindow.substance_painter = _env.Painter()

    # https://github.com/huntfx/vfxwindow/wiki/Quick-Start#callbacks
    if _env.Max():
        _UIWindow.addCallback = None

    if _env.Substance():
        import sd as __sd

        app = __sd.getContext().getSDApplication()

        _UIWindow.addCallbackBeforeFileLoaded = app.registerBeforeFileLoadedCallback
        _UIWindow.addCallbackAfterFileLoaded = app.registerAfterFileLoadedCallback
        _UIWindow.addCallbackBeforeFileSaved = app.registerBeforeFileSavedCallback
        _UIWindow.addCallbackAfterFileSaved = app.registerAfterFileSavedCallback
        _UIWindow.removeCallbacks = (app.unregisterCallback(uuid) for uuid in [])

    if _env.Painter():
        import substance_painter.event as __e

        # Subscribe to project related events.
        connections = {
            __e.ProjectOpened: _UIWindow.addCallbackProjectOpened,
            __e.ProjectCreated: _UIWindow.addCallbackProjectCreated,
            __e.ProjectAboutToClose: _UIWindow.addCallbackProjectAboutToClose,
            __e.ProjectAboutToSave: _UIWindow.addCallbackProjectAboutToSave,
            __e.ProjectSaved: _UIWindow.addCallbackProjectSaved,
            __e.ExportTexturesAboutToStart: _UIWindow.addCallbackExportTexturesAboutToStart,
            __e.ExportTexturesEnded: _UIWindow.addCallbackExportTexturesEnded,
            __e.ShelfCrawlingStarted: _UIWindow.addCallbackShelfCrawlingStarted,
            __e.ShelfCrawlingEnded: _UIWindow.addCallbackShelfCrawlingEnded,
            __e.ProjectEditionEntered: _UIWindow.addCallbackProjectEditionEntered,
            __e.ProjectEditionLeft: _UIWindow.addCallbackProjectEditionLeft,
        }
        for event, callback in connections.items():
            __e.DISPATCHER.connect(event, callback)

except ImportError:
    pass

# dispatch application
import yurlungur
from yurlungur.core.env import v

if not v(_env._Maya):
    del yurlungur.maya
if not v(_env._Cinema4D):
    del yurlungur.c4d
if not v(_env._Max):
    del yurlungur.max
if not v(_env._Modo):
    del yurlungur.modo
if not v(_env._Substance):
    del yurlungur.substance_designer
if not v(_env._SubstancePainter):
    del yurlungur.substance_painter
if not v(_env._Toolbag):
    del yurlungur.toolbag

if not v(_env._Davinci):
    del yurlungur.davinci

if not v(_env._Blender):
    del yurlungur.blender
if not v(_env._Unreal):
    del yurlungur.unreal

if not v(_env._RenderDoc):
    del yurlungur.renderdoc
if not yurlungur.pycharm.enable:
    del yurlungur.pycharm
if not yurlungur.vscode.enable:
    del yurlungur.vscode

# TODO
if not v(_env._Nuke):
    del yurlungur.nuke
if not v(_env._Houdini):
    del yurlungur.houdini
if not v(_env._Photoshop):
    pass  # del yurlungur.photoshop

# _env.set()

del yurlungur.adapters, yurlungur.core, yurlungur.exception, yurlungur.wrapper, yurlungur.tool, v
del yurlungur, sys, contextlib

# import stubs; stubs.load()
