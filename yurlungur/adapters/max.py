# coding: utf-8
try:
    import pymxs
except ImportError:
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("3dsmax")._actions
