# coding: utf-8
try:
    import pymxs
except ImportError:
    from yurlungur.core.env import App as _

    run, shell, end = _("3dsmax")._actions
