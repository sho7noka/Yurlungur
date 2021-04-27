# coding: utf-8
import sys
import contextlib
import importlib

from yurlungur.core import env as _env
from yurlungur.tool import window as _window

# dispatch for Qt
if _env.Qt():
    from yurlungur import Qt

    Qt.main_window = _window.main_window
    Qt.show = _window.show

# dispatch for app
with contextlib.suppress(ImportError):
    from vfxwindow import VFXWindow as _UIWindow

    Qt.UIWindow = _UIWindow
    _UIWindow.c4d = _env.C4D()
    _UIWindow.marmoset = _env.Marmoset()
    _UIWindow.rumba = _env.Rumba()
    _UIWindow.substance_painter = _env.SPainter()
    _UIWindow.unity = _env.Unity()

    # https://github.com/huntfx/vfxwindow/wiki/Quick-Start#callbacks
    if _env.Max():
        _UIWindow.addCallback = None

    if _env.Unity():
        _UIWindow.addCallback = None

    if _env.Substance():
        import sd as __sd

        app = __sd.getContext().getSDApplication()

        _UIWindow.addCallbackBeforeFileLoaded = app.registerBeforeFileLoadedCallback
        _UIWindow.addCallbackAfterFileLoaded = app.registerAfterFileLoadedCallback
        _UIWindow.addCallbackBeforeFileSaved = app.registerBeforeFileSavedCallback
        _UIWindow.addCallbackAfterFileSaved = app.registerAfterFileSavedCallback
        _UIWindow.removeCallbacks = (app.unregisterCallback(uuid) for uuid in [])

    if _env.SPainter():
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

# dispatch for exit
if _env.Blender() or _env.Nuke():
    sys.exit = None

try:
    import pydevd_pycharm as __pycharm

    is_evd = True
except ImportError:
    try:
        import debugpy as __dpy

        is_code = True
    except ImportError:
        try:
            import ptvsd as __ptvsd

            is_code = True
        except ImportError:
            pass
            # import traceback
            # traceback.print_exc()

# __rpc.debug_listen = remote_debug_listen

from yurlungur.tool.rpc import remote_debug_listen
ptvsd = importlib.import_module("ptvsd")
pycharm = importlib.import_module("pydevd_pycharm")
vim = importlib.import_module("vim")

ptvsd.remote_debug = remote_debug_listen
pycharm.remote_debug = remote_debug_listen
vim.remote_debug = remote_debug_listen
