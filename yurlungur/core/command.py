from proxy import YNode
from application import application

__doc__ = """Monkey Patch commands"""

def _ls(self):
    print "_ls"
    return


def _glob(self):
    return


def _cd(self):
    return


def _root(self):
    return


def _pwd(self):
    return


def _parent(self):
    return


def _children(self):
    return


def _select(self, *args):
    return


# patch

ls = YNode()
ls.ls = _ls
