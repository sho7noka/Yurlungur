# coding: utf-8
try:
    import clr
    import UnityEngine as UnityEngine
    import UnityEditor as UnityEditor

    Console = clr.UnityEditor.Scripting.Python.PythonConsoleWindow
    Outputs = Console.AddToOutput
    getattr(UnityEngine, "Debug")  # NOTE: DO NOT DELETE
    
    # C:\Users\shosu\MAGUchan\Library\PackageCache\com.unity.scripting.python@4.0.0-pre.1\Python~\site-packages\unity_python
    from unity_python.common import utils
    _PYTHON_INTERPRETER_PATH = unreal.get_interpreter_executable_path()
    # C:\Users\shosu\MAGUchan\ProjectSettings\PythonSettings.asset

    # TODO
    # https://docs.unity3d.com/Packages/com.unity.scripting.python@4.0/api/UnityEditor.Scripting.Python.PythonSettings.html
    # https://github.com/unity3d-jp/MeshSync/tree/dev/Editor/Scripts/DCCIntegration
    # C:\Program Files\Unity\Hub\Editor\2019.4.22f1\Editor\Data\Tools

    def EvalScript(script):
        """
        NOTE: Require Roslyn or Mono.CSharp

        Args:
            script:

        Returns:

        """
        import System.IO
        try:
            # com.unity.code-analysis
            clr.AddReference("Microsoft.CodeAnalysis.CSharp.Scripting")
            import Microsoft.CodeAnalysis.CSharp.Scripting as scripting
            scripting.CSharpScript.EvaluateAsync(script)

            clr.AddReference("Mono.CSharp")
            import Mono.Csharp
            Mono.CSharp.Evaluator.Run(script)

        except System.IO.FileNotFoundException:
            """
            https://stackoverflow.com/questions/19600315/how-to-use-a-net-method-which-modifies-in-place-in-python/19600349#19600349
            var value = 0;
            UnityEditor.ExpressionEvaluator.Evaluate(script, value: out value);    
            """
            v = 0
            _, out = UnityEditor.ExpressionEvaluator.Evaluate(script, v)
            print(out)

except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, quit, _ = __App("unity")._actions


def Projects():
    """
    Returns: RecentProjectPath list
    """
    import os
    from yurlungur.core import deco

    recent_key = 'RecentlyUsedProjectPaths-'
    projects = []

    # https://area.autodesk.jp/column/tutorial/maya_atoz/send-to-unity/
    if deco.Windows():
        import _winreg
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Unity Technologies\Unity Editor 5.x')
        info = _winreg.QueryInfoKey(key)
        for i in range(info[1]):
            v = _winreg.EnumValue(key, i)
            if recent_key in v[0]:
                projects.append(v[1])

    if deco.Mac():
        import plistlib
        plist = os.getenv("HOME") + "/Library/Preferences/com.unity3d.UnityEditor5.x.plist"

        with open(plist, "rb") as fp:
            info = plistlib.load(fp)
            for k, v in info.items():
                if recent_key in k:
                    projects.append(v)

    # TODO
    if deco.Linux():
        projects.append("")

    return projects


def initialize_package(path="", version="6.0.0"):
    """
    https://docs.unity3d.com/Packages/com.unity.scripting.python@4.0/manual/index.html
    Args:
        path:

    Returns:

    """
    import os, textwrap, json

    if path == "":
        latest = Projects()[-1]
        mn = os.path.join(latest, "Packages/manifest.json")
        cs = os.path.join(latest, "Assets/PythonEditor.cs")
        py = os.path.join(latest, "/Library/PythonInstall", "python.exe")
    else:
        mn = os.path.join(path, "Packages/manifest.json")
        cs = os.path.join(path, "Assets/PythonEditor.cs")
        py = os.path.join(path, "/Library/PythonInstall", "python.exe")

    with open(mn, "r") as f:
        df = json.load(f)  # , object_pairs_hook=collections.OrderedDict)
        df["dependencies"]["com.unity.scripting.python"] = version
        with open(mn, "w") as w:
            json.dump(df, w, indent=4)

    with open(cs, "w") as f:
        f.write(textwrap.dedent("""
        using System;
        using System.IO;
        using System.Linq;
        using System.Collections.Generic;
        using Object = UnityEngine.Object;
        #if UNITY_EDITOR
        using UnityEditor;
        using UnityEditor.Scripting.Python;

        namespace PythonExtensions
        {
            [InitializeOnLoad]
            public class Startup
            {
                public static void Exec()
                {
                    var args = Environment.GetCommandLineArgs();

                    if (args.First().EndsWith(".py"))
                    {
                        PythonRunner.RunFile(args.First());
                    }
                    else
                    {
                        PythonRunner.RunString(args.First());
                    }
                }
            }

            public class PythonExtension
            {
                [MenuItem("Assets/Create/Python/Open In ScriptEditor")]
                private static void OpenScriptEditor()
                {
                    // get text
                    var selectedAssets = Selection.GetFiltered(typeof(Object), SelectionMode.Assets);
                    var path = AssetDatabase.GetAssetPath(selectedAssets.First());
                    var m_codeContents = System.IO.File.ReadAllText(path);
        
                    // serialize field
                    EditorApplication.ExecuteMenuItem("Window/General/Python Console");
        
                    var window = EditorWindow.GetWindow<PythonConsoleWindow>();
                    var content = new SerializedObject(window);
                    content.Update();
                    var property = content.FindProperty("m_codeContents");
                    property.stringValue = m_codeContents;
                    content.ApplyModifiedProperties();
                }
        
                [MenuItem("Assets/Create/Python/Python Script")]
                private static void CreateScript()
                {
                    var path = "Assets/Python";
                    if (!AssetDatabase.IsValidFolder(path))
                    {
                        path = Path.GetDirectoryName(path);
                    }
        
                    path += Path.DirectorySeparatorChar + "new_script.py";
                    path = AssetDatabase.GenerateUniqueAssetPath(path);
                    path = Path.GetFullPath(path);
        
                    File.CreateText(path);
                    AssetDatabase.Refresh();
                }
            }
        
            public class SaveHook : UnityEditor.AssetModificationProcessor
            {
                private static bool is_python = false;
        
                private void OnWillSaveAssets(IEnumerable<string> paths)
                {
                    foreach (var path in paths)
                    {
                        if (!path.EndsWith(".py")) continue;
                        is_python = true;
                        break;
                    }
        
                    if (is_python)
                        AssetDatabase.Refresh();
                }
            }
        }
        #endif
        """))


class Timeline(object):
    def __init__(self, project):
        self.project = project
        self.timeline = project.GetCurrentTimeline()
        self.media = project.GetMediaPool()
        self.clips = self.media.GetRootFolder().GetClips().values()

    def __repr__(self):
        return self.timeline.GetName() + self.timeline.GetCurrentTimecode()

    def __getitem__(self, val):
        return self

    @property
    def current(self):
        return self.timeline

    def imports(self, *args):
        self.media.AppendToTimeline(*args)
        self.timeline = self.project.GetCurrentTimeline()
        return self

    @property
    def tracks(self):
        return Track(self.timeline)


class Track(object):
    def __init__(self, timeline):
        self.timeline = timeline
        self.track = timeline.GetCurrentVideoItem()

    def __repr__(self):
        return self.track.GetName()

    def __getitem__(self, val):
        return self

    @property
    def current(self):
        return self.timeline.GetCurrentVideoItem()

    @property
    def clips(self):
        return Item(self.track)


class Item(object):
    def __init__(self, track):
        self.track = track

    def __repr__(self):
        return self.track.GetName() + self.track.GetDuration()

    def __getitem__(self, val):
        return self

    def exports(self, path):
        return self.track.ExportFusionComp(path, 1)

    def delete(self, name):
        return self.track.DeleteFusionCompByName(name)

"""
    from UnityEngine import *
    from UnityEditor import *

    asset = Resources.FindObjectsOfTypeAll(typeof(TimelineAsset)).First()
    path = AssetDatabase.GetAssetOrScenePath(asset)
    timelineAsset = AssetDatabase.LoadAssetAtPath < TimelineAsset > (path)
    AssetDatabase.OpenAsset(timelineAsset)

    playable = GameObject.Find(timelineAsset.name).GetComponent < PlayableDirector > ()
    animationTrack = timelineAsset.CreateTrack < MorphControlTrack > (null, "MTH_DEF")
    mesh = GameObject.Find("MTH_DEF").GetComponent < SkinnedMeshRenderer > ()
    playable.SetGenericBinding(animationTrack, mesh)

    timelineAsset.editorSettings.scenePreview = true
    timelineAsset.CreateTrack < AnimationTrack > ()
    timelineAsset.DeleteTrack(timelineAsset.GetOutputTracks().First())
    track = timelineAsset.GetOutputTrack(0)
    track.CreateDefaultClip()

    
    UnityEditorでTcpListenerでソケットListenしてるとドメインリロード前にStopしてもポートが開放されずに死ぬことがたまにあってなんでや?
    TcpListenerのStart前にSocketにSetHandleInformationをP/Invokeで呼ばない限り、(継承する設定で)子プロセスが立ち上がった際にソケットが子プロセスに複製されてそっちで掴んでしまい、
    AcceptTcpClientが子プロセスが終了しない限り戻らず、Listenも終わらなくなる、という話っぽかった。Unity Editorは猛然と子プロセス気軽に立ち上げてく
    https://stackoverflow.com/questions/48858029/why-does-redirecting-the-input-stream-of-a-process-affect-the-behaviour-of-a-tcp
    
    using
    UnityEditor;
    using
    Unity.EditorCoroutines.Editor;
    using
    UnityEditor.Scripting.Python;

    // / < summary >
    // / Editor
    初期化時にTCPListener
    を初期化
    // / < / summary >
    [InitializeOnLoad]


public
static


class EditorPipeline
    {
        private
    static
    TcpListener
    server;
    private
    static
    EditorCoroutine
    _coroutine;

    // / < summary >
    // / https: // kan - kikuchi.hatenablog.com / entry / EditorCoroutineUtility
                   // / < / summary >
                            static
    EditorPipeline()
    {
        UnityEngine.Application.runInBackground = true;
    server = new
    TcpListener(IPAddress.Parse("127.0.0.1"), 8001);
    server.Start();
    _coroutine = EditorCoroutineUtility.StartCoroutineOwnerless(Start());
    EditorApplication.quitting += Quit;
    }

    private
    static
    IEnumerator
    Start()
    {
        UnityEngine.Debug.Log("TCP port is opened: 8001");
    yield
    return null; // new
    EditorWaitForSeconds(5);
    server.BeginAcceptSocket(DoAcceptTcpClientCallback, server);

}

private
static
void
Quit()
{
server.Stop();
EditorCoroutineUtility.StopCoroutine(_coroutine);
}

private
static
void
DoAcceptTcpClientCallback(IAsyncResult
ar)
{
var
listener = (TcpListener)
ar.AsyncState;
var
client = listener.EndAcceptTcpClient(ar);
var
stream = client.GetStream();
var
reader = new
StreamReader(stream, Encoding.UTF8);

while (client.Connected)
    {
while (!reader.EndOfStream)
    {
        PythonRunner.RunString(reader.ReadLine());
    // UnityEngine.Debug.Log();
    }

    if (!client.Client.Poll(1000, SelectMode.SelectRead) | | (client.Client.Available != 0)) continue;
    client.Close();
    break;
}
}
}
"""
