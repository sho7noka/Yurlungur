import unreal


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
