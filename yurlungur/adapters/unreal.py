# coding: utf-8
import sys as __sys

try:
    import unreal

    # C:\Program Files\Epic Games\UE_4.26\Engine\Plugins\Experimental\PythonScriptPlugin\Content\Python
    import debugpy_unreal
    import remote_execution

    # command
    # https://docs.unrealengine.com/ja/ProductionPipelines/DevelopmentSetup/Tools/ConsoleManager/index.html

    @unreal.uclass()
    class EditorUtil(unreal.GlobalEditorUtilityBase):
        """"""

    @unreal.uclass()
    class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
        """"""

    @unreal.uclass()
    class GetEditorLevelLibrary(unreal.EditorLevelLibrary):
        """"""

    @unreal.uclass()
    class MaterialEditingLib(unreal.MaterialEditingLibrary):
        """"""

    @unreal.uclass()
    class GetAnimationLibrary(unreal.AnimationLibrary):
        """"""


    def execute_console_command(script):
        # UE4Editor.exe Project.uproject -ExecCmds=”Automation RunTests テスト名;Quit” -game
        # unreal.PythonScriptLibrary.execute_python_command("任意のスクリプトかパス")
        Editor = GetEditorLevelLibrary().get_editor_world()
        unreal.SystemLibrary.execute_console_command(Editor, script)

    def editor_utility(euw_path):
        """https://kinnaji.com/2021/01/08/unrealpythonsummary/#上級編　レベル【★★★★】"""
        EUS = unreal.EditorUtilitySubsystem()
        EUWBP = unreal.load_object(None, euw_path)  # euw_path = /Game/EUW_Test.EUW_Test
        EUS.spawn_and_register_tab(EUWBP)

    def uname(item):
        """compatible for asset and"""

        for asset in GetEditorAssetLibrary().list_assets("/Game/"):
            if asset.endswith(item):
                return asset

        for actor in GetEditorLevelLibrary().get_all_level_actors():
            if item in actor.get_name():
                return EditorUtil().get_actor_reference(actor.get_full_name().split(":")[1])

        raise Exception


    stubs = unreal.SystemLibrary.get_project_directory() + "/Intermediate/PythonStub/unreal.py"
    __sys.modules[__name__] = __sys.modules["unreal"]
    execute_console_command("DumpConsoleCommands")
    tools = unreal.AssetToolsHelpers.get_asset_tools()


except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, _ = __App("unreal")._actions

    
class Timeline(object):
    def __init__(self, project):
        self.project = project
        self.timeline = project.GetCurrentTimeline()
        self.media = project.GetMediaPool()
        self.clips = self.media.GetRootFolder().GetClips().values()

    def __repr__(self):
        return 

    def __getitem__(self, val):
        return

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
        assert isinstance(val, int)

        if 0 < val < self.timeline.GetTrackCount("video"):
            self.track = self.timeline.GetItemsInTrack("video", val)
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


# print(unreal.SequencerScriptingRange().get_end_frame())
# print(unreal.SequencerScriptingRangeExtensions().get_end_seconds())
# LevelSequence = unreal.find_asset('/Game/LevelSequences')
# bindings = LevelSequence.get_bindings()

# for b in bindings:
#     if b.get_display_name() == 'CubeTest':
#         
#         # bindingsの中のトラック。Transformとか
#         tracks = b.get_tracks()
#         for t in tracks:
#             # 例 : Transformの中のメンバー
#             sections = t.get_sections()
#             for s in sections:
#                 # 例 : Transformの中のチャンネル。物によって型が違う
#                 channels = s.get_channels()
#                 for c in channels:
#                     keys = c.get_keys()
#                     for k in keys:
#                         c.remove_key(k)
# 
#                 for i in range(0, 5):
#                     FNumber = unreal.FrameNumber(30 * i)
#                     Event = unreal.MovieSceneEvent()
#                     #loc x にキーを追加
#                     channels[0].add_key(FNumber, 1)
# 
# # マスタートラックを取得
# MasterTracks = LevelSequence.get_master_tracks()
# for MasterTrack in MasterTracks:
#     for Section in MasterTrack.get_sections():
#         for Channel in Section.get_channels():
#             Keys = Channel.get_keys()
#             for Key in Keys:
#                 Channel.remove_key(Key)
#             for i in range(0, 5):
#                 FNumber = unreal.FrameNumber(30 * i)
#                 Event = unreal.MovieSceneEvent()
#                 Channel.add_key(FNumber, Event)

# 4 エクスポート unreal.AnimSequenceExporterFBX()
# export_task = unreal.AssetExportTask()
# export_task.automated = True
# export_task.exporter = unreal.AnimSequenceExporterFBX[]
# export_task.filename = "MyOutputPath"
# export_task.object = sequence_to_export
# unreal.Exporter.run_asset_export_task(export_task)