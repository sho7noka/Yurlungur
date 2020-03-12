# coding: utf-8

# https://docs.unity3d.com/Packages/com.unity.scripting.python@2.0/manual/index.html
try:
    import UnityEngine
    import UnityEditor

    getattr(UnityEngine, "Debug")

except (ImportError, AttributeError):
    from yurlungur.core.env import App as _

    run, shell, end = _("unity")._actions


def Console():
    typeName = "UnityEngine.MonoBehaviour"
    # print System.Reflection.Assembly.Load("UnityEngine.dll").GetType(typeName);
    for asm in System.AppDomain.CurrentDomain.GetAssemblies():
        print asm.ToString()
    import clr
    return clr.UnityEditor.Scripting.Python.PythonConsoleWindow

def EvalScript(script):
    pass


"""
using UnityEngine;
using UnityEditor;

[InitializeOnLoad]
public class Startup {
    static Startup()
    {
        UnityEditor.PackageManager.Client.Add("com.unity.scripting.python");
    }
}
using UnityEngine;
using System.IO;
using System.Reflection;
using System.Collections;
#if UNITY_EDITOR
using System;
using UnityEditor;
using UnityEditor.SceneManagement;

[UnityEditor.InitializeOnLoad]
public class ExampleClass
{
    [MenuItem("Examples/Execute menu items")]
    static void EditorPlaying()
    {
        // https://docs.unity3d.com/Packages/com.unity.package-manager-ui@2.0/manual/index.html
        UnityEditor.PackageManager.Client.Add("com.unity.scripting.python");


        var newScene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
        EditorApplication.ExecuteMenuItem("GameObject/3D Object/Cube");
        EditorSceneManager.SaveScene(newScene, "Assets/MyNewScene.unity");
        EditorApplication.Exit(0);

        PropertyInfo[] myPropertyInfo;
        myPropertyInfo = Type.GetType("System.Type").GetProperties();
        myPropertyInfo[0].ToString();
    }

    static void ResetPositionOnSelected()
    {
        Undo.SetCurrentGroupName("Zero out selected gameObjects");
        var group = Undo.GetCurrentGroup();

        Undo.RecordObjects(Selection.transforms, "transform selected objects");

        foreach (var t in Selection.transforms)
        {
            t.position = Vector3.zero;
        }

        Undo.CollapseUndoOperations(group);
    }
}
#endif
"""
