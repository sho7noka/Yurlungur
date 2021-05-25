"""
コード補完
https://github.com/macvim-dev/macvim/blob/6de65806e5c70db61ed9faeeda86236577dbdf84/runtime/doc/if_pyth.txt
https://speakerdeck.com/knzm/python-module-import-system
https://github.com/minoue/mayaScriptEditor.vim/blob/master/plugin/mayaScriptEditor.vim
https://gist.github.com/utatsuya/e4d60228b2372662b2fc
"""
import sys
import types
from imp import find_module, load_module

import importlib

from yurlungur.tool.rpc import remote_debug_listen


class VimModuleLoader(object):
    def __init__(self, module):
        self.module = module

    def load_module(self, fullname, path=None):
        return self.module


def _find_module(fullname, oldtail, path):
    idx = oldtail.find('.')
    if idx > 0:
        name = oldtail[:idx]
        tail = oldtail[idx + 1:]
        fmr = find_module(name, path)
        module = load_module(fullname[:-len(oldtail)] + name, *fmr)
        return _find_module(fullname, tail, module.__path__)
    else:
        fmr = find_module(fullname, path)
        return load_module(fullname, *fmr)


# It uses vim module itself in place of VimPathFinder class: it does not
# matter for python which object has find_module function attached to as
# an attribute.
class VimPathFinder(object):
    @classmethod
    def find_module(cls, fullname, path=None):
        try:
            return VimModuleLoader(_find_module(fullname, fullname, path or vim._get_paths()))
        except ImportError:
            return None

    @classmethod
    def load_module(cls, fullname, path=None):
        return _find_module(fullname, fullname, path or vim._get_paths())


def hook(path):
    if path == vim.VIM_SPECIAL_PATH:
        return VimPathFinder
    else:
        raise ImportError


# sys.path_hooks.append(hook)

try:
    sys.modules[__name__] = importlib.import_module("pynvim")
    setattr(sys.modules[__name__], "remote_debug", remote_debug_listen)
    setattr(sys.modules[__name__], "enable", True)

except:
    sys.modules[__name__] = types.ModuleType("vim")
    setattr(sys.modules[__name__], "enable", False)
