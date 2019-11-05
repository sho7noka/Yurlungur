# coding: utf-8
try:
    from yurlungur.core.plugin import Plugbase
    import UnityEngine
except ImportError:
    from yurlungur.core.env import App as _

    run, shell, end = _("unity")._actions


class Unity(Plugbase):
    def proxy(self):
        pass