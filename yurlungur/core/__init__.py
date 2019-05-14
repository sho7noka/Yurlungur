from yurlungur.core.app import application, exApplication
from yurlungur.core.command import cmd, file
from yurlungur.core.deco import UndoGroup
from yurlungur.core import env
from yurlungur.core.logger import pprint
from yurlungur.core.proxy import YFile

if env.Maya() or env.Houdini() or env.Substance() or env.Nuke() or env.Davinci():
    from yurlungur.core.proxy import YNode
else:
    from yurlungur.core.proxy import YObject

del app, command, deco, logger, nodetype, proxy
