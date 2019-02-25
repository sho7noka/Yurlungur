import doctest
import unittest
import sys

sys.path.append('../yurlungur')

from yurlungur.core.env import installed, Unreal

@unittest.skipUnless(installed("unreal"), "Unreal is not found")
class TestUnreal(unittest.TestCase):
    def test_app(self):

import sys
sys.path.append("C:/Users/sho/Downloads/Yurlungur")

import yurlungur as yr
reload(yr)

print yr.YNode('/Game/aaaa').name

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
    
editor = EditorUtil()
assets = GetEditorAssetLibrary()
materials = MaterialEditingLib()
anims = GetAnimationLibrary()


allAssets = assets.list_assets("/Game/", True, False)
for asset in allAssets or []:
    deps = assets.find_package_referencers_for_asset(asset, False)
    if (len(deps) <= 0):
        assets.delete_asset(asset)


selectedAssets = editor.get_selected_assets()
selectedAssetName = .get_name()
selectedAssetPath = .get_path_name()
selectedAssetClass = .get_class()
allAssets = editor.list_assets(workingPath, True, False)

for selectedAsset in selectedAssets:
    selectedAsset.modify(True)
    anims.remove_all_animation_notify_tracks(selectedAsset)

editor.load_asset()


if __name__ == '__main__':
    unittest.main()