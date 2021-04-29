# coding: utf-8
import inspect
import os
import platform
import sys
import contextlib
import importlib

from yurlungur.core import env as _env
from yurlungur.tool import window as _window
from yurlungur.tool.rpc import remote_debug_listen as _listen

# dispatch for exit
if _env.Blender() or _env.Nuke():
    sys.exit = None

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

# pycharm > vim > vscode
if list(filter(lambda x: x.startswith("pydev"), sys.modules)):
    pycharm = importlib.import_module("pydevd_pycharm")
    pycharm.remote_debug = _listen
    print(pycharm.__file__)

else:
    try:
        vim = importlib.import_module("vim")
        vim.remote_debug = _listen

    except ModuleNotFoundError:
        try:
            if platform.system() == "Windows":
                path = os.getenv("USERPROFILE")
            if platform.system() == "Darwin":
                path = os.getenv("HOME")

            ext = os.path.join(path, ".vscode/extensions")
            pyext = list(filter(lambda x: x.startswith("ms-python.python"), os.listdir(ext)))
            mspy = os.path.join(ext, pyext[0], "pythonFiles/lib/python")
            sys.path.append(mspy)

            vscode = importlib.import_module("debugpy")
            vscode.remote_debug = _listen
        except (ModuleNotFoundError, IndexError):
            pass

# import stubs; stubs.load()
