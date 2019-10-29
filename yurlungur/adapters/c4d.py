# coding: utf-8
try:
    import c4d
except ImportError:
    from yurlungur.core.env import App as _

    run, shell, end = _("c4d")._actions
