# stores the selected assets into a proper folder determined by the asset type
# the folder name is retrieved from look-up dictionary in the Project_Structure_Mappings.json file
# ensure the json file is in the same directory as this script so it can be read

import unreal
import os
import json

# instances of unreal classes
editor_util = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()
editor_asset_lib = unreal.EditorAssetLibrary()

# get the selected assets
selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)
cleaned = 0

# read the project structure json file to retrieve folder mapping dictionary
folder_mapping = {}
project_structure_file = os.path.join(os.path.dirname(__file__),"Project_Structure_Mappings.json")
unreal.log(project_structure_file)

with open(project_structure_file, "r") as json_file:
    folder_mapping = json.loads(json_file.read()).get("Folders")
    # unreal.log_warning(folder_mapping)

#hard coded parent path
parent_dir = "\\Game"

if num_assets > 0:
    asset_path = editor_asset_lib.get_path_name_for_loaded_asset(selected_assets[0])
    parent_dir = os.path.dirname(asset_path)


for asset in selected_assets:
    # get the class instance and the clear text name
    asset_name = system_lib.get_object_name(asset)
    asset_class = asset.get_class()
    class_name = system_lib.get_class_display_name(asset_class)
    folder_key = folder_mapping.get(class_name)

    current_folder_name = os.path.basename(parent_dir)
    unreal.log("current folder name: {}".format(current_folder_name))

    if current_folder_name in folder_key or class_name in current_folder_name:
        unreal.log_warning("Asset {} is already in correct folder {}".format(asset_name, current_folder_name))
        continue

    # assemble new path and relocate assets
    try:
        new_path = os.path.join(parent_dir, folder_key, asset_name)
        editor_asset_lib.rename_loaded_asset(asset, new_path)
        cleaned += 1
        unreal.log("Cleaned up {} to {}".format(asset_name, new_path))
    except Exception as err:
        unreal.log("Could not move {} to new location {}".format(asset_name, new_path))

    unreal.log("Asset {} with class {}".format(asset_name, class_name))