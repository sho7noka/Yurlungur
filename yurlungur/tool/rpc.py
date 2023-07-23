# coding: utf-8
import sys
import types
import importlib
import threading
import socket

if sys.version_info.major >= 3:
    import xmlrpc.server as _xmlrpc_server
    import xmlrpc.client as _xmlrpc_client
else:
    import SimpleXMLRPCServer as _xmlrpc_server
    import xmlrpclib as _xmlrpc_client

import yurlungur
from yurlungur.core.app import application
from yurlungur.core import env


def send_chr(msg, host="localhost", port=18811):
    """
    send msg to socket

    Args:
        msg:
        port:
        host:
    Returns:

    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(msg + '\n')
        res = s.recv(1024)
        # s.close()
        return res


def session(module="hou", host="localhost", port=18811):
    """
    rpc session for client
    >>> print(session().system.listMethods())

    # https://www.sidefx.com/ja/docs/houdini/hom/rpc.html
    >>> import hrpyc
    >>> _, hou = hrpyc.import_remote_module()
    Args:
        port:
        host:
        name:

    Returns:
        proxy
    """
    if env.Houdini():
        connection = importlib.import_module("rpyc").classic.connect(host, port)
        proxy = connection.modules[module]
        return proxy
    else:
        with _xmlrpc_client.ServerProxy('http://%s:%d' % (host, port)) as proxy:
            return proxy


def listen(host="localhost", port=18811, use_thread=True, quiet=True):
    """
    rpc listen for server

    >>> if env.Maya():
    >>>     import maya.cmds as cmds
    >>>     # import maya.app.general.CommandPort
    >>>     cmds.commandPort(n=':%d' % port , stp='python')

    >>> if env.Houdini():
    >>>    import hou
    >>>    hou.hscript("openport -p %d" % port)

    NOTE: register_function は　オブジェクトを解釈しないので全入力が必要

    Args:
        host:
        port:
        use_thread:
        quiet:

    Returns:

    """
    # Note that quiet=False only applies when use_thread=False.
    if env.Houdini():
        if use_thread:
            thread = threading.Thread(
                target=lambda: listen(port, use_thread=False))
            thread.start()
            return thread

        args = []
        if quiet:
            args.append("-q")
        args.extend(("-p", str(port), "--dont-register"))

        import rpyc.servers.classic_server as server
        options, args = server.parser.parse_args(args)
        options.registrar = None
        options.authenticator = None
        server.serve_threaded(options)

    else:
        with _xmlrpc_server.SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False) as server:
            print("Listening on port %s %d..." % (application.__name__, port))

            for i in [i for i in dir(yurlungur) if i[0] != "_" and i != "Qt"]:
                obj = getattr(yurlungur, i)

                if type(obj) == types.FunctionType:
                    server.register_function(obj, "yurlungur.%s" % i)
                else:
                    try:
                        for m in [m for m in dir(obj) if m[0] != "_"]:
                            meth = getattr(obj, m)
                            if (type(meth) not in (types.MethodType, types.FunctionType)):
                                continue

                            # if isinstance(meth, hou.EnumValue):
                            #     client.register_function(meth.__repr__, "hou.%s.%s.__repr__" % (i, m))
                            if (type(obj) in (type, type) and type(meth) == types.MethodType):
                                server.register_function(meth, "typeMethods.yurlungur.%s.%s" % (i, m))
                            else:
                                for m in dir(obj):
                                    meth = getattr(obj, m)
                                    if (type(meth) not in (types.MethodType, types.FunctionType)) or m == "_":
                                        continue

                                    # if isinstance(meth, hou.EnumValue):
                                    #     client.register_function(meth.__repr__, "hou.%s.%s.__repr__" % (i, m))
                                    if (type(obj) in (type, type) and type(meth) == types.MethodType):
                                        server.register_function(meth, "typeMethods.yurlungur.%s.%s" % (i, m))
                                    else:
                                        server.register_function(meth, "yurlungur.%s.%s" % (i, m))
                    except TypeError:
                        pass

            server.register_function(server.shutdown, "quit")
            server.register_introspection_functions()
            # server.register_multicall_functions()
            # server.serve_forever()
            server_thread = threading.Thread(target=server.serve_forever, use_thread=False)
            server_thread.start()
            return server_thread


def remote_debug_listen(host='localhost', port=18811):
    """
    Args:
        host:
        port:

    Returns:
    """
    try:
        vscode = importlib.import_module("debugpy")
        vscode.listen((host, port))
        vscode.wait_for_client()
        return
    except ModuleNotFoundError:
        pass

    try:
        pycharm = importlib.import_module("pydevd_pycharm")
        pycharm.settrace(host, port=port, stdoutToServer=True, stderrToServer=True, suspend=False)
        return
    except ModuleNotFoundError:
        pass
