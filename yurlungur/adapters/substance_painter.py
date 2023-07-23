# coding: utf-8
u"""
https://substance3d.adobe.com/documentation/spdoc/command-lines-98959411.htm
"""

import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["substance_painter"]

    from functools import partial
    import types
    import inspect
    import json
    import yurlungur
    import substance_painter

    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        if obj == "user" or obj == "tool":
            continue
        setattr(__sys.modules[__name__], obj, getattr(yurlungur, obj))
    

    class Baking:
        @staticmethod
        def bake(textureSetName : str):
            return substance_painter.js.evaluate(f"alg.baking.{inspect.currentframe().f_code.co_name}('{textureSetName}')")
        @staticmethod
        def setCommonBakingParameters(parameters : object):
            return substance_painter.js.evaluate(f"alg.baking.{inspect.currentframe().f_code.co_name}({parameters})")
        @staticmethod
        def setCurvatureMethod(method : str = "FromMesh"):
            return substance_painter.js.evaluate(f"alg.baking.{inspect.currentframe().f_code.co_name}('{method}')")
        @staticmethod
        def setTextureSetBakingParameters(textureSetName : str, parameters : object):
            return substance_painter.js.evaluate(f"alg.baking.{inspect.currentframe().f_code.co_name}('{textureSetName}',{parameters})")
        @staticmethod
        def textureSetBakingParameters(textureSetName : str):
            return substance_painter.js.evaluate(f"alg.baking.{inspect.currentframe().f_code.co_name}('{textureSetName}')")

        def textureSet(self, name : str = ""):
            if name == "":
                return substance_painter.textureset.get_active_stack().material().name()
            return substance_painter.textureset.from_name(name).material().name()

        def meshMap(self, key):
            usages = ["AO", "BentNormals", "Curvature", "Height", "ID", "Normal", "Opacity", "Position", "Thickness", "WorldSpaceNormal"]
            # ambient_occlusion, normal_base, id, curvature, position, thickness, world_space_normals
            usage = getattr(substance_painter.textureset.MeshMapUsage, key)

            res = self.textureSet().get_mesh_map_resource(usage)
            self.textureSet().set_mesh_map_resource(usage, res or None)
            substance_painter.js.evaluate(f"alg.mapexport.meshMapIdentifiers('{self.textureSet()}')")


    class Shaders:
        @staticmethod
        def groups(shaderId : int = 0):
            return substance_painter.js.evaluate(f"alg.shaders.{inspect.currentframe().f_code.co_name}({shaderId})")
        @staticmethod
        def materials(shaderId : int = 0):
            return substance_painter.js.evaluate(f"alg.shaders.{inspect.currentframe().f_code.co_name}({shaderId})")
        @staticmethod
        def parameter(shaderId : int, identifier : str):
            return substance_painter.js.evaluate(f"alg.shaders.{inspect.currentframe().f_code.co_name}({shaderId},'{identifier}')")
        @staticmethod
        def parameters(shaderId : int = 0, group : str = ""):
            return substance_painter.js.evaluate(f"alg.shaders.{inspect.currentframe().f_code.co_name}({shaderId},'{group}')")
        @staticmethod
        def setParameters(shaderId : int, parameters : object):
            return substance_painter.js.evaluate(f"alg.shaders.{inspect.currentframe().f_code.co_name}({shaderId, parameters})")
        @staticmethod
        def shaderInstancesFromObject(jsObject : object):
            return substance_painter.js.evaluate(f"alg.shaders.{inspect.currentframe().f_code.co_name}({jsObject})")
        @staticmethod
        def updateShaderInstance(shaderId : int = 0, shaderUrl : str = ""):
            return substance_painter.js.evaluate(f"alg.shaders.{inspect.currentframe().f_code.co_name}({shaderId},'{shaderUrl}')")

    __sys.modules[__name__].baking = types.ModuleType("baking", "alg.baking\nManage baking of the opened project")
    
    for obj in "commonBakingParameters", "curvatureMethod", "selectCageMesh", "selectHighDefinitionMeshes":
        setattr(__sys.modules[__name__].baking, obj, partial(substance_painter.js.evaluate, f"alg.baking.{obj}()"))

    for obj in inspect.getmembers(Baking, inspect.isfunction):
        setattr(__sys.modules[__name__].baking, obj[0], getattr(Baking, obj[0]))

    __sys.modules[__name__].shaders = types.ModuleType("shaders", "alg.shaders\nControl shader instances of the currently opened project")
    
    for obj in "instances", "shaderInstancesToObject":
        setattr(__sys.modules[__name__].shaders, obj, partial(substance_painter.js.evaluate, f"alg.shaders.{obj}()"))

    for obj in inspect.getmembers(Shaders, inspect.isfunction):
        setattr(__sys.modules[__name__].shaders, obj[0], getattr(Shaders, obj[0]))


except (ImportError, KeyError):
    import base64
    import json

    if __sys.version_info >= (3, 0):
        import http.client as http
    else:
        import httplib as http

    class RemotePainter():
        def __init__(self, port=60041, host='localhost'):
            self._host = host
            self._port = port

            # Json server connection
            self._PAINTER_ROUTE = '/run.json'
            self._HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

        # Execute a HTTP POST request to the Substance Painter server and send/receive JSON data
        def _jsonPostRequest(self, route, body, type):
            connection = http.HTTPConnection(self._host, self._port, timeout=3600)
            connection.request('POST', route, body, self._HEADERS)
            response = connection.getresponse()

            data = response.read()
            connection.close()

            if type == "js":
                data = json.loads(data.decode('utf-8'))

                if 'error' in data:
                    OutJson = json.loads(body.decode())
                    print(base64.b64decode(OutJson["js"]))
                    raise ExecuteScriptError(data['error'])
            else:
                # Python can return nothing, so decoding can fail
                try:
                    data = data.decode('utf-8').rstrip()
                except:
                    pass

            return data

        def checkConnection(self):
            connection = http.HTTPConnection(self._host, self._port)
            connection.connect()

        def execScript(self, script, type="python"):
            Command = base64.b64encode(script.encode('utf-8'))

            if type == "js":
                Command = '{{"js":"{0}"}}'.format(Command.decode('utf-8'))
            else:
                Command = '{{"python":"{0}"}}'.format(Command.decode('utf-8'))

            Command = Command.encode("utf-8")

            return self._jsonPostRequest(self._PAINTER_ROUTE, Command, type)

        def show(self):
            self.execScript("import substance_painter;substance_painter.ui.show_main_window()", "python")


    from yurlungur.core.env import App as __App
    __Remote = RemotePainter()
    show = __Remote.show
    _, run, quit, _ = __App("substance_painter")._actions
    __all__ = ["run", "quit", "show"]