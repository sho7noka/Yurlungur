# coding: utf-8
import unreal

editor = EditorUtil()
assets = GetEditorAssetLibrary()
materials = MaterialEditingLib()
anims = GetAnimationLibrary()


def apply_lods(static_mesh):
    number_of_vertices = unreal.EditorStaticMeshLibrary.get_number_verts(static_mesh, 0)
    if number_of_vertices < 10:
        return

    print("treating asset: " + static_mesh.get_name())
    print("existing LOD count: " + str(unreal.EditorStaticMeshLibrary.get_lod_count(static_mesh)))

    options = unreal.EditorScriptingMeshReductionOptions()
    options.reduction_settings = [unreal.EditorScriptingMeshReductionSettings(1.0, 1.0),
                                  unreal.EditorScriptingMeshReductionSettings(0.8, 0.75),
                                  unreal.EditorScriptingMeshReductionSettings(0.6, 0.5),
                                  unreal.EditorScriptingMeshReductionSettings(0.4, 0.25)
                                  ]
    options.auto_compute_lod_screen_size = False
    unreal.EditorStaticMeshLibrary.set_lods(static_mesh, options)
    unreal.EditorAssetLibrary.save_loaded_asset(static_mesh)
    print("new LOD count: " + str(unreal.EditorStaticMeshLibrary.get_lod_count(static_mesh)))


all_assets = unreal.EditorAssetLibrary.list_assets(asset_path)
all_assets_loaded = [unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]
static_mesh_assets = unreal.EditorFilterLibrary.by_class(all_assets_loaded, unreal.StaticMesh)
map(apply_lods, static_mesh_assets)

allAssets = assets.list_assets("/Game/", True, False)
for asset in allAssets or []:
    deps = assets.find_package_referencers_for_asset(asset, False)
    if (len(deps) <= 0):
        assets.delete_asset(asset)

selectedAssets = editor.get_selected_assets()

selectedAssetName = selectedAssets.get_name()
selectedAssetPath = selectedAssets.get_path_name()
selectedAssetClass = selectedAssets.get_class()
allAssets = editor.list_assets(workingPath, True, False)

for selectedAsset in selectedAssets:
    selectedAsset.modify(True)
    anims.remove_all_animation_notify_tracks(selectedAsset)

editor.load_asset()

import sys

sys.path.append("C:/Users/sho/Downloads/Yurlungur")
import yurlungur as yr

reload(yr)
print yr.YNode('/Game/aaaa').name

if hasattr(meta, 'uclass'):
    meta.editor.get_actor_reference(self.name)


@unreal.uclass()
class EditorUtil(unreal.GlobalEditorUtilityBase):
    pass


@unreal.uclass()
class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
    pass


@unreal.uclass()
class MaterialEditingLib(unreal.MaterialEditingLibrary):
    pass


@unreal.uclass()
class GetAnimationLibrary(unreal.AnimationLibrary):
    pass


class Project(object):
    def __init__(self, project):
        self.project = project

    @property
    def sequences(self):
        return Timeline(self.project)


class Timeline(object):
    def __init__(self, timeline):
        self.timeline = timeline

    @property
    def tracks(self):
        return Track(self.timeline)


class Track(object):
    def __init__(self, track):
        self.track = track

    @property
    def clips(self):
        return Item(self.track)


class Item(object):
    pass
