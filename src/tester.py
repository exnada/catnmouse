import argparse
from datetime import datetime
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json
from os.path import exists
from Game import *
from Helpers import *
from Maze import *
from Players import *


if __name__ == "__main__":
#     with open("defaults.json", "r") as f:
#         defaults = json.load(f)
#     with open("config.json", "r") as f:
#         config_ref = json.load(f)

#     active_configs = get_active_configs(config_ref)
#     if len(active_configs) == 1:
#         print("Found %i active configuration:" % (len(active_configs)))
#     else:
#         print("Found %i active configurations:" % (len(active_configs)))
#     for active_config in active_configs:
#         print("- %s" % (active_config))

#     for active_config in active_configs:
#         with open("config.json", "r") as f:
#             config = json.load(f)
#         active_configs_check = get_active_configs(config)
#         if active_configs_check != active_configs:
#             print(
#                 "ERROR: configuration file shows different active configurations. Aborting."
#             )
#             exit(1)

#         framework_params = get_framework_params(active_config, config, defaults)

#         rx = framework_params["results"]
#         lfn = rx["data_directory"] + rx["logs_filename"]  ### TO BE DONE: write logs (?)
#         ofn = rx["data_directory"] + rx["data_filename"]

#         cols = [
#             "height",
#             "width",
#             "raw_memory",
#             "nbr_snakes",
#             "random_seed",
#             "t_max",
#             "result",
#         ]

#         if not exists(ofn):
#             with open(ofn, "w") as f:
#                 f.write(",".join(str(c) for c in cols) + "\n")
#             print("creating output file %s" % (ofn))
#             print(cols)
#         else:
#             print("appending to output file %s" % (ofn))

#         params = {
#             "height": framework_params["height"],
#             "width": framework_params["width"],
#             "debug_level": framework_params["debug_level"],
#             "custom_snakes": framework_params["custom_snakes"],
#         }
#         rsl = framework_params["random_seed_list"]
#         nsl = framework_params["nbr_snakes_list"]
#         fml = framework_params["raw_memory_list"]

#         compute_failed = framework_params["compute_failed"]

#         for random_seed_id in range(len(rsl)):
#             params["random_seed"] = rsl[random_seed_id]
#             previous_results = np.zeros(len(fml), dtype=int)
#             for nbr_snakes_id in range(len(nsl)):
#                 params["nbr_snakes"] = nsl[nbr_snakes_id]
#                 for fid in range(len(fml)):
#                     params["raw_memory"] = fml[fid]
#                     if previous_results[fid] == 0 or compute_failed:
#                         game = Game(**params)
#                         result = game.simulate()
#                         row = [
#                             game.height,
#                             game.width,
#                             game.raw_memory,
#                             game.nbr_snakes,
#                             game.random_seed,
#                             game.time,
#                             result,
#                         ]
#                         print(row)
#                     else:
#                         result = previous_results[fid]
#                         row = [
#                             params["height"],
#                             params["width"],
#                             params["raw_memory"],
#                             params["nbr_snakes"],
#                             params["random_seed"],
#                             0,
#                             result,
#                         ]
#                         print(row, " skipped")

#                     previous_results[fid] = result
#                     with open(ofn, "a") as f:
#                         f.write(",".join(str(r) for r in row) + "\n")
