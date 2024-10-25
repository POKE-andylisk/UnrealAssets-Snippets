# duplicates the selected assets in the content browser by "num_copies" amount of times
# it is hard-coded for now, but I will using this script as the basis for having a GUI driving the value
# from user-input

import unreal
import os
import time

start_time = time.time()

# instances of unreal classes
editor_util = unreal.EditorUtilityLibrary()
editor_asset_lib = unreal.EditorAssetLibrary()

# get the selected assets
selected_assets = editor_util.get_selected_assets()
num_assets = len(selected_assets)

num_copies = 10
total_num_copies = num_assets * num_copies
text_label = "Duplicating Assets"
running = True

with unreal.ScopedSlowTask(total_num_copies, text_label) as slow_task:
    # display the dialog
    slow_task.make_dialog(True)
    for asset in selected_assets:
        # get the asset name and path to be duplicated
        asset_name = asset.get_fname()
        asset_path = editor_asset_lib.get_path_name_for_loaded_asset(asset)
        source_path = os.path.dirname(asset_path)

        for i in range(num_copies):
            # if user pressed the cancel, stop
            if slow_task.should_cancel():
                running = False
                break

            new_name = "{}_{}".format(asset_name, i)
            dest_path = os.path.join(source_path, new_name)
            duplicate = editor_asset_lib.duplicate_asset(asset_path, dest_path)
            slow_task.enter_progress_frame(1)

            if duplicate is None:
                unreal.log_warning("Duplciate from {} at {} already exits".format(source_path, dest_path))
        
        if not running:
            break

end_time = time.time()
unreal.log("{} asset/s duplicated {} times in {}".format(asset_name, num_copies, end_time - start_time))