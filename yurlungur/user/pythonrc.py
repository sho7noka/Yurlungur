import sys

# server
HOST = 'localhost'
PORT = 1089

if EGG not in sys.path:
    sys.path.append(EGG)
    sys.path.append(PYD)
    sys.path.append(YUR)

import pydevd

try:
    import hrpyc
    hrpyc.start_server()
    # import hrpyc
    # hrpyc.start_server(port=PORT, use_thread=False)

    pydevd.settrace(HOST, port=PORT, stdoutToServer=True, stderrToServer=True)
    yr.pprint(yr.name)
except:
    pydevd.stoptrace()

import ptvsd

# allow other computers to attach to ptvsd at this IP address and port, using the password
try:
    ptvsd.enable_attach("SFds_KjLDFJ:LK", address=('localhost', 3000))
    print("Not attached already, attaching...")
except ptvsd.AttachAlreadyEnabledError:
    print("Attached already, continuing...")


def test():
    # pause the program until a remote debugger is attached
    ptvsd.wait_for_attach()
    # break at this line
    ptvsd.break_into_debugger()
    before = "before"
    after = "after"

# hou sever side
sys.path += [
    "C:/Program Files/Side Effects Software/Houdini 17.5.293/houdini/python2.7libs",
    "C:/Program Files/Side Effects Software/Houdini 17.5.293/python27/lib/site-packages",
]
import hrpyc
connection, hou = hrpyc.import_remote_module()