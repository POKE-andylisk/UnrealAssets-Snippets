# appends a prefix to the group of selected assets
# the prefix is retrieved from look-up dictionary in the Project_Structure_Mappings.json file
# ensure the json file is in the same directory as this script so it can be read

# automatic asset prefixes
import unreal
import json
import os

# instances of unreal classes
editor_util = unreal.EditorUtilityLibrary()
system_lib = unreal.SystemLibrary()

# read the project structure json file to retrieve folder mapping dictionary
prefix_mapping = {}
project_structure_file = os.path.join(os.path.dirname(__file__),"Project_Structure_Mappings.json")
unreal.log(project_structure_file)

with open(project_structure_file, "r") as json_file:
    prefix_mapping = json.loads(json_file.read()).get("Prefixes")

# get the selected assets
selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)
prefixed = 0

for asset in selected_assets:
    # get the class instance and the clear text name
    asset_name = asset.get_name()
    asset_class = asset.get_class()
    class_name = system_lib.get_class_display_name(asset_class)

    # get the prefix for the given class
    class_prefix = prefix_mapping.get(class_name, None)

    if class_name is None:
        unreal.log_warning("No mapping for asset {} of type {}".format(asset_name, class_name))
        continue

    if not asset_name.startswith(class_prefix):
        # renmae the asset and add prefix
        new_name = class_prefix + asset_name
        editor_util.rename_asset(asset, new_name)
        prefixed += 1
        unreal.log("Prefixed {} of type {} with {}".format(asset_name, class_name, class_prefix))

    else:
        unreal.log("Asset {} of type {} is already prefixed with {}".format(asset_name, class_name, class_prefix))

if prefixed != 0:
    unreal.log("Prefixed {} of {} assets".format(asset_name, class_name))
else:
    unreal.log("No assets were changed on this execution, either no assets were selected or prefix already exists")