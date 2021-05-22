from yurlungur.core.app import application, initialize
from yurlungur.core import env
from yurlungur.core.command import file, node, attr
from yurlungur.core.deco import UndoGroup, cache, threads, timer
from yurlungur.core.exception import except_runtime
from yurlungur.core import vars
# from yurlungur.core.datatype import Vector, Matrix, Color

if env.Maya() or env.Houdini() or env.Substance() or env.Nuke() or env.Davinci() or env.C4D() or env.Rumba():
    from yurlungur.core.proxy import Node
else:
    from yurlungur.core.proxy import Object as Node
from yurlungur.core.proxy import File

del app, command, deco, proxy
