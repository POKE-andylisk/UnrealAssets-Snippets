# deletes the selected assets by first determining whether there are references and dependences
# the instant_delete variable determines whether to delete thme right away or first moving them
# into a separate trash folder

import unreal
import os

# instances of unreal classes
editor_util = unreal.EditorUtilityLibrary()
editor_asset_lib = unreal.EditorAssetLibrary()

# get the selected assets
selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)
removed = 0

# instantly delete assets or move to trash folder
instant_delete = False
trash_folder = os.path.join(os.sep, "Game", "Trash")
to_be_deleted = []

for asset in selected_assets:
    # get the full path to the to be duplicated asset
    asset_name = asset.get_fname()
    asset_path = editor_asset_lib.get_path_name_for_loaded_asset(asset)

    # get a list of references for this asset
    asset_references = editor_asset_lib.find_package_referencers_for_asset(asset_path)

    if len(asset_references) == 0:
        to_be_deleted.append(asset)

for asset in to_be_deleted:
    asset_name = asset.get_fname()

    # instantly delete the assets
    if instant_delete:
        deleted = editor_asset_lib.delete_loaded_asset(asset)

        if not deleted:
            unreal.log_warning("Asset {} could not be deleted".format(asset_name))
            continue

        removed += 1

    # move the assets to the trash folder
    else:
        new_path = os.path.join(trash_folder, str(asset_name))
        moved = editor_asset_lib.rename_loaded_asset(asset, new_path)

        if not moved:
            unreal.log_warning("Asset {} could not be moved to trash".format(asset_name))
            continue
        removed += 1

output_test = "removed" if instant_delete else "moved to trash"
unreal.log("{} of {} to be deleted assets, of {} selected, removed".format(removed, len(to_be_deleted), num_assets))