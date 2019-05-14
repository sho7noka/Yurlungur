# -*- coding: utf-8 -*-
import sys
try:
    import time
    import traceback
    import functools
    import threading
    import contextlib
except ImportError:
    pass

from yurlungur.tool.meta import meta
from yurlungur.core import env, logger


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


def cache(func, *args, **kwargs):
    saved = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in saved:
            return saved[args]
        result = func(*args)
        saved[args] = result
        return result

    return wrapper if sys.version_info < (3, 2) else functools.lcu_cache(*args, **kwargs)


def trace(func):
    try:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                if hasattr(logger.logger, "warning"):
                    logger.logger.warning(traceback.format_exc())
                else:
                    logger.logger.log(traceback.format_exc(), logger.Warning)
    except (NameError, ImportError):
        wrapper = func

    return wrapper


def timer(func):
    import yurlungur

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        yurlungur.logger.pprint(
            '{0} start'.format(func.__name__)
        )
        start_time = time.clock()
        ret = func(*args, **kwargs)
        end_time = time.clock()
        yurlungur.logger.pprint(
            '\n{0}: {1:,f}s'.format("total: ", (end_time - start_time))
        )
        return ret

    return wrapper


@contextlib.contextmanager
def threads(func):
    """
    Maya, Houdini, 3dsMax, Substance and Nuke
    >>>
    :param func:
    :return:
    """
    t = threading.Thread(target=func)
    t.start()
    t.join()


def __runner(locker):
    """
    thread runner
    :param locker:
    :return:
    """
    if env.Maya():
        import maya.utils as utils
        utils.executeDeferred(locker)

    elif env.Houdini():
        meta

    elif env.Nuke():
        meta.executeInMainThreadWithResult(locker)

    elif env.Max():
        try:
            locker.acquire()
            with meta.mxstoken():
                locker
        except:
            raise
        finally:
            if locker.locked():
                locker.release()

    return locker


if env.Houdini():
    UndoGroup = meta.undos.group

if env.Unreal():
    UndoGroup = meta.ScopedEditorTransaction

if env.Max():
    UndoGroup = functools.partial(meta.undo, True)

if env.Nuke():
    UndoGroup = meta.Undo

if env.Substance():
    UndoGroup = meta.sd.UndoGroup
