# coding: utf-8
import importlib
import sys
import threading
import types
import socket

if sys.version_info.major >= 3:
    import xmlrpc.server as _xmlrpc_server
    import xmlrpc.client as _xmlrpc_client
else:
    import SimpleXMLRPCServer as _xmlrpc_server
    import xmlrpclib as _xmlrpc_client

from yurlungur.core.app import application
from yurlungur.core import env
from yurlungur.core.deco import trace


@trace
def session(port=18811, server="127.0.0.1", name="hou"):
    """
    rpc session for client

    Args:
        port:
        server:
        name:

    Returns:
        proxy
    """

    """    
    if env.Houdini():
        import hrpyc
        _, hou = hrpyc.import_remote_module()

    # https://qiita.com/tm8r/items/29d598231b793be6c6ea
    if env.Unity():
        import unity_python.client.unity_client as unity_client
        unity_client
    """

    if env.Houdini() or env.Unity():
        import rpyc
        connection = rpyc.classic.connect(server, port)
        proxy = connection.modules[name]
        return proxy
    else:
        proxy = _xmlrpc_client.ServerProxy('http://%s:%d' % (server, port))
        return proxy


@trace
def listen(port=18811, server="127.0.0.1", use_thread=True, quiet=True):
    """
    rpc listen for server

    NOTE: register_function は　オブジェクトを解釈しないので全入力が必要
    Args:
        port:
        use_thread:
        quiet:

    Returns:

    """

    """
    if env.Maya():
        import maya.cmds as cmds
        import maya.app.general.CommandPort
        cmds.commandPort(n=':%d' % port , stp='python')

    if env.Houdini():
        import hou
        hou.hscript("openport -p %d" % port)
    """

    if env.Houdini() or env.Unity():

        # Note that quiet=False only applies when use_thread=False.
        if use_thread:
            thread = threading.Thread(
                target=lambda: listen(port, use_thread=False))
            thread.start()
            return thread

        args = []
        if quiet:
            args.append("-q")
        args.extend(("-p", str(port), "--dont-register"))

        import rpyc.servers.classic_server
        options, args = rpyc.servers.classic_server.parser.parse_args(args)
        options.registrar = None
        options.authenticator = None
        rpyc.servers.classic_server.serve_threaded(options)
    else:
        server = _xmlrpc_server.SimpleXMLRPCServer((server, port), allow_none=True, logRequests=False)
        print("Listening on port %s %d..." % (application.__name__, port))

        import yurlungur
        for i in dir(yurlungur):
            # Ignore internal stuff
            if i[0] == "_" or i == "Qt":
                continue

            o = getattr(yurlungur, i)
            if type(o) == types.FunctionType:
                server.register_function(o, "yurlungur.%s" % i)

            else:
                try:
                    for m in dir(o) or []:
                        if m[0] == "_":
                            continue

                        meth = getattr(o, m)
                        if (type(meth) not in (types.MethodType, types.FunctionType)):
                            continue

                        # if isinstance(meth, hou.EnumValue):
                        #     client.register_function(meth.__repr__, "hou.%s.%s.__repr__" % (i, m))
                        if (type(o) in (type, type) and type(meth) == types.MethodType):
                            server.register_function(meth, "typeMethods.yurlungur.%s.%s" % (i, m))
                        else:
                            for m in dir(o):
                                meth = getattr(o, m)
                                if (type(meth) not in (types.MethodType, types.FunctionType)) or m == "_":
                                    continue

                                # if isinstance(meth, hou.EnumValue):
                                #     client.register_function(meth.__repr__, "hou.%s.%s.__repr__" % (i, m))
                                if (type(o) in (type, type) and type(meth) == types.MethodType):
                                    server.register_function(meth, "typeMethods.yurlungur.%s.%s" % (i, m))
                                else:
                                    server.register_function(meth, "yurlungur.%s.%s" % (i, m))
                except TypeError:
                    pass

        server.register_function(server.shutdown, "close")
        server.register_introspection_functions()
        server.serve_forever()


@trace
def send_chr(msg, port=18811, server="127.0.0.1"):
    """
    send socket
    Args:
        msg:
        port:
        server:

    Returns:

    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server, port))
        s.send(msg + '\n')
        res = s.recv(1024)
        # s.close()
        return res


@trace
def remote_debug_listen(HOST='localhost', port=3000):
    """
    Args:
        HOST:
        port:

    Returns:
    """
    try:
        vscode = importlib.import_module("debugpy")
        # vscode.configure(python=designer_py_interpreter)
        vscode.listen((HOST, port))
        vscode.wait_for_client()
        return
    except ModuleNotFoundError:
        pass

    try:
        pycharm = importlib.import_module("pydevd_pycharm")
        pycharm.settrace(HOST, port=port, stdoutToServer=True, stderrToServer=True, suspend=False)
        return
    except ModuleNotFoundError:
        pass

    try:
        vim = importlib.import_module("vim")
        vim.current
        return
    except ModuleNotFoundError:
        pass


import random
import time
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer, MultiPathXMLRPCServer


class SimpleThreadedXMLRPCServer(ThreadingMixIn, MultiPathXMLRPCServer):
    pass


# sleep for random number of seconds
def sleep():
    r = random.randint(2, 10)
    print('sleeping {} seconds'.format(r))
    time.sleep(r)
    return 'slept {} seconds, exiting'.format(r)


# run server
def run_server(host="localhost", port=8000):
    server_addr = (host, port)
    server = SimpleThreadedXMLRPCServer(server_addr)
    server.allow_reuse_address = True
    server.register_function(sleep, 'sleep')
    server.register_function(server.shutdown, "close")

    print("Server thread started. Testing server ...")
    print('listening on {} port {}'.format(host, port))

    server.serve_forever()


if __name__ == '__main__':
    run_server()
