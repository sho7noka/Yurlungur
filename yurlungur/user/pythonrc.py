
import sys

# server
HOST = 'localhost'
PORT = 1089

# user
EGG = "/Users/shosumioka/Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/181.5087.37/PyCharm.app/Contents/debug-eggs/pycharm-debug.egg"
PYD = "/Users/shosumioka/Library/Application/ Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/181.5087.37/PyCharm.app/Contents/helpers/pydev"
YUR = "/Users/shosumioka/Documents/Yurlungur"

if EGG not in sys.path:
    sys.path.append(EGG)
    sys.path.append(PYD)
    sys.path.append(YUR)

import yurlungur as yr
yr.YNode("Camera").location.set(yr.YVector(1, 1, 1).array())

import pydevd
try:
    # import hrpyc
    # hrpyc.start_server(port=PORT, use_thread=False)

    pydevd.settrace(HOST, port=PORT, stdoutToServer=True, stderrToServer=True)
    yr.log(yr.name)
except:
    pydevd.stoptrace()


# hou sever side
# import hrpyc
# connection, hou = hrpyc.import_remote_module()

# http://www.sidefx.com/docs/houdini/hom/rpc.html
# /Applications/Blender/blender.app/Contents/Resources/2.79/scripts/startup
# /Applications/Houdini/Houdini16.5.473/Frameworks/Houdini.framework/Versions/16.5.473/Resources/houdini/python2.7libs