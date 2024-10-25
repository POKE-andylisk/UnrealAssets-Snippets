# exectue this file from the editor using Tools > Exceute python script
import unreal
import os
unreal.log("Hello World from 2024!")
unreal.log_warning("A warning to the world!")
unreal.log_error("An error to the world!")

# unreal.log(os.path.dirname(__file__))

prefix_map_file = os.path.join(os.path.dirname(__file__),"prefix_mapping.json")
unreal.log(prefix_map_file)