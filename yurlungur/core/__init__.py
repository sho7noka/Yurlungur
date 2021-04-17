from yurlungur.core.app import application, use, initialize
from yurlungur.core import env
from yurlungur.core.command import file, node, attr
from yurlungur.core.deco import UndoGroup, cache, threads, timer
from yurlungur.core.exception import except_runtime, except_key, except_os
from yurlungur.core.logger import pprint
from yurlungur.core.datatype import Vector, Matrix, Color
from yurlungur.core.proxy import File

if env.Maya() or env.Houdini() or env.Substance() or env.Nuke() or env.Davinci() or env.C4D() or env.Rumba():
    from yurlungur.core.proxy import Node
else:
    from yurlungur.core.proxy import Object as Node

del app, command, deco, logger, proxy
