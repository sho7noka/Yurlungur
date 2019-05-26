from yurlungur.core.app import application
from yurlungur.core.command import cmd, file
from yurlungur.core.deco import UndoGroup, cache, threads
from yurlungur.core.logger import pprint
from yurlungur.core import env

if env.Maya() or env.Houdini() or env.Substance() or env.Nuke() or env.Davinci():
    from yurlungur.core.proxy import YNode
else:
    from yurlungur.core.proxy import YObject
from yurlungur.core.proxy import YFile, YColor, YVector, YMatrix

del app, command, deco, logger, proxy
