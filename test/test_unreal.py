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

        GetEditorAssetLibrary = type('GetEditorAssetLibrary', (yr.meta.EditorAssetLibrary,), dict())
        print GetEditorAssetLibrary()

        workingPath = "/Game/"
        editorAssetLib = GetEditorAssetLibrary();
        allAssets = editorAssetLib.list_assets(workingPath, True, False)
        processingAssetPath = ""
        allAssetsCount = len(allAssets)
        if ( allAssetsCount > 0):
            with unreal.ScopedSlowTask(allAssetsCount, processingAssetPath) as slowTask:
                slowTask.make_dialog(True)
                for asset in allAssets:
                    processingAssetPath = asset
                    deps = editorAssetLib.find_package_referencers_for_asset(asset, False)
                    if (len(deps) <= 0):
                        print ">>> Deleting >>> %s" % asset
                        editorAssetLib.delete_asset(asset)
                    if slowTask.should_cancel():
                        break
                    slowTask.enter_progress_frame(1, processingAssetPath)

if __name__ == '__main__':
    unittest.main()