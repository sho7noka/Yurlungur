# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["renderdoc"]
    import yurlungur

    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        setattr(__sys.modules[__name__], obj, getattr(yurlungur, obj))

    from yurlungur.core.env import Unity, Unreal

    # https://docs.unity3d.com/ja/2019.4/Manual/RenderDocIntegration.html
    if Unity():
        import UnityEngine
        import UnityEditor
        import UnityEditorInternal

        if (UnityEditorInternal.RenderDoc.IsInstalled() and UnityEditorInternal.RenderDoc.IsSupported()):
            UnityEditorInternal.RenderDoc.Load()

            if (UnityEngine.Experimental.Rendering.ExternalGPUProfiler.IsAttached()):
                UnityEngine.Experimental.Rendering.ExternalGPUProfiler.BeginGPUCapture()
                UnityEngine.Experimental.Rendering.ExternalGPUProfiler.EndGPUCapture()
            else:
                import clr
                assembly = clr.GetClrType(UnityEditor.EditorWindow).Assembly
                window = assembly.GetType("UnityEditor.GameView")
                UnityEditorInternal.RenderDoc.BeginCaptureRenderDoc(window)
                UnityEditorInternal.RenderDoc.EndCaptureRenderDoc(window)

        elif (UnityEngine.Apple.FrameCapture.IsDestinationSupported(
                UnityEngine.Apple.FrameCaptureDestination.GPUTraceDocument)):
            UnityEngine.Apple.FrameCapture.BeginCaptureToXcode()
            UnityEngine.Apple.FrameCapture.EndCapture()

    # https://docs.unrealengine.com/4.27/en-US/PythonAPI/class/MoviePipelineDebugSettings.html?highlight=renderdoc
    if Unreal():
        import unreal
        setings = unreal.MoviePipelineDebugSettings()
        settings.set_editor_property("capture_frame", 60)
        settings.set_editor_property("capture_frames_with_render_doc", True)

    # chrome 
    # set RENDERDOC_HOOK_EGL=0
    # --disable-gpu-sandbox --gpu-startup-dialog --disable-direct-composition


except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, quit, connect = __App("renderdoc")._actions

    __all__ = ["run", "shell", "quit", "connect"]
