# coding: utf-8
try:
    import maya
except ImportError:
    from yurlungur.core.env import App as _

    run, shell, end = _("maya")._actions
