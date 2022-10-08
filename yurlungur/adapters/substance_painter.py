# coding: utf-8
u"""
https://substance3d.adobe.com/documentation/spdoc/command-lines-98959411.html

--mesh <meshPath>	
Mesh to load in a project.

Example:
// Create a new project with a specific mesh
"Adobe Substance 3D Painter.exe" --mesh "E:/MymeshFolder/MyMesh.obj" 

// Update a mesh inside an existing project
"Adobe Substance 3D Painter.exe" --mesh "E:/MymeshFolder/MyMesh.obj" "E:/MyMeshFolder/Project.spp" 
--mesh-map	
Baked maps associated with the mesh (AO, Normal, Curvature). Can be specified multiple times. Nomenclature : TextureSetName_AdditionalMapSlot

Ambient occlusion = ambient_occlusion
Curvature = curvature
Normal = normal_base
World Space Normal = world_space_normals
Position = position
Thickness = thickness
ID = id
Example:

"Adobe Substance 3D Painter.exe" --mesh "E:/MyMeshFolder/MyMesh.obj" --mesh-map " E:/MyMeshFolder/DefaultMaterial_ambient_occlusion.png" 
--split-by-udim	Create a texture set per UDIM tile.
--export-path	Default export path where the outputs of the project will be exported.
--vram-budget <amount>	
Override the video memory (VRAM) budget defined by Substance 3D Painter engine. "Amount" is in megabytes.

Example:

// Set the VRam budget to 2GB
"Adobe Substance 3D Painter.exe" --vram-budget 2048 
--disable-version-checking	Don't check if a new version of the application is available when starting up
--enable-remote-scripting	Allow to run scripting commands from outside the application. See Remote control with scripting for more information.
"""

import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["substance_painter"]
    from yurlungur.tool.meta import meta
    setattr(__sys.modules[__name__], "eval", getattr(meta, "eval"))
    del meta

    import yurlungur

    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        if obj == "user" or obj == "tool":
            continue
        setattr(__sys.modules[__name__], obj, getattr(yurlungur, obj))


    """
    # Bake & Shader
    setattr(__sys.modules[__name__], "enable", substance_painter.js.evaluate)
    substance_painter.js.evaluate()
    substance_painter.baking.bake()

    alg.baking
    bake(textureSetName)
    commonBakingParameters()
    curvatureMethod()
    selectCageMesh()
    selectHighDefinitionMeshes()
    setCommonBakingParameters(parameters)
    setCurvatureMethod(method)
    setTextureSetBakingParameters(textureSetName, parameters)
    textureSetBakingParameters(textureSetName)

    alg.shaders
    groups(shaderId)
    instances()
    materials(shaderId)
    parameter(shaderId, identifier)
    parameters(shaderId[, group])
    setParameters(shaderId, parameters[, transactionOptions])
    shaderInstancesFromObject(jsObject)
    shaderInstancesToObject()
    updateShaderInstance(shaderId, shaderUrl)
    """

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


    class PainterError(Exception):
        def __init__(self, message):
            super(PainterError, self).__init__(message)


    class ExecuteScriptError(PainterError):
        def __init__(self, data):
            super(PainterError, self).__init__('An error occured when executing script: {0}'.format(data))


    from yurlungur.core.env import App as __App

    __Remote = RemotePainter()
    # __Remote.checkConnection()
    show = __Remote.show

    _, run, quit, _ = __App("substance_painter")._actions

    __all__ = ["run", "quit", "show"]