# set all textures in the project to linear color after matching their asset name to
# containing one of the following keywords in color_patterns
import unreal

# instances of unreal classes
editor_asset_lib = unreal.EditorAssetLibrary()
string_lib = unreal.StringLibrary()

# get all assets in source dir
source_dir = "/Game/"
include_subfolders = True
set_textures = 0

assets = editor_asset_lib.list_assets(source_dir, recursive=include_subfolders)
color_patterns = ["_ORM", "_OcclusionRoughnessMetallic", "_Metallic", "Roughness", "_RGH", "_Mask", "_MSK", "Linear"]

for asset in assets:
    # for every asset, check it against all the patterns
    for pattern in color_patterns:
        if string_lib.contains(asset, pattern):
            # load the asset, turn off sRGB and set compression settings to TC_Mask
            asset_obj = editor_asset_lib.load_asset(asset)
            asset_obj.set_editor_property("sRGB", False)
            asset_obj.set_editor_property("CompressionSettings", unreal.TextureCompressionSettings.TC_MASKS)

            unreal.log("Checking {} against {}".format(asset, pattern))
