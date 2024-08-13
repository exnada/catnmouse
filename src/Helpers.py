from datetime import datetime
import time
from os.path import exists
import copy
import json
import numpy as np
import pandas as pd


def get_active_configs(config):
    return [
        config_name
        for config_name in config
        if config[config_name]["status"] == "active"
    ]


def _get_simple_param(param, config, defaults):
    if param in config.keys():
        return config[param]
    else:
        return defaults[param]


def _get_list_param(param, config, defaults):
    if param in config.keys():
        pconf = config[param]
        if pconf["type"] == "single":
            return [pconf["value"]]
        elif pconf["type"] == "list":
            return pconf["value"]
        elif pconf["type"] == "scan":
            min_val = pconf.get("min", 0)
            max_val = pconf.get("max", 0)
            step_val = pconf.get("step", 1)
            return list(range(min_val, max_val + 1, step_val))
        elif pconf["type"] == "custom":
            return [len(pconf["value"])]
    else:
        return [defaults[param]]


def _get_custom_snakes(config, defaults):
    param = "nbr_snakes"
    if param in config.keys():
        pconf = config[param]
        if pconf["type"] == "custom":
            custom_snakes = []
            for s in pconf["value"]:
                custom_snakes.append((s[0], s[1]))
            return custom_snakes
        else:
            return None
    else:
        return None


def _check_bool(param, datablock):
    if not isinstance(datablock[param], bool):
        print("ERROR: value of %s is not bool: %s" % (param, datablock[param]))
        exit(1)


def _get_results_block(active_config, cfg, dflt):
    res = {}
    simple_params = [
        "process",
        "logs_filename",
        "data_directory",
        "mpeg_directory",
        "pics_directory",
    ]
    for param in simple_params:
        res[param] = _get_simple_param(param, cfg, dflt)
    now = datetime.now()
    date_time = now.strftime("%Y%m%d-%H%M%S")
    fn = "%s-%s.csv" % (active_config, date_time)
    res["data_filename"] = cfg.get("data_filename", fn)
    return res


def get_framework_params(active_config, config, defaults):
    framework_params = {}
    simple_params = ["height", "width", "debug_level"]
    for param in simple_params:
        framework_params[param] = _get_simple_param(
            param, config[active_config], defaults
        )
    list_params = ["raw_memory", "nbr_snakes", "random_seed"]
    for param in list_params:
        framework_params[param] = _get_simple_param(
            param, config[active_config], defaults
        )
        framework_params[param + "_list"] = _get_list_param(
            param, config[active_config], defaults
        )
    framework_params["custom_snakes"] = _get_custom_snakes(
        config[active_config], defaults
    )
    bool_params = [
        "compute_failed",
        "post_sim_image_processing",
        "post_sim_movie_processing",
    ]
    for param in bool_params:
        framework_params[param] = _get_simple_param(
            param, config[active_config], defaults
        )
        _check_bool(param, framework_params)
    framework_params["results"] = _get_results_block(
        active_config, config[active_config]["results"], defaults["results"]
    )
    return framework_params


def remove_list_entries(complex_dict):
    clean_dict = copy.copy(complex_dict)
    for key in complex_dict.keys():
        if key.endswith("_list"):
            clean_dict.pop(key)
    return clean_dict


def compile_todo_list(ofn, framework_params):
    if not exists(ofn):
        print("ERROR: output file does not exist, %s" % (ofn))
        exit(1)
    df = pd.read_csv(ofn)
    h = framework_params["height"]
    w = framework_params["width"]
    fml = framework_params["raw_memory_list"]
    nsl = framework_params["nbr_snakes_list"]
    rsl = framework_params["random_seed_list"]

    start_time = time.time()
    mask = (
        (df["height"] == framework_params["height"])
        & (df["width"] == framework_params["width"])
        & (df["raw_memory"].isin(fml))
        & (df["nbr_snakes"].isin(nsl))
        & (df["random_seed"].isin(rsl))
    )

    print(
        "entries found: ",
        df[mask].shape[0],
        "; entries expected: ",
        len(fml) * len(nsl) * len(rsl),
        "; missing: ",
        len(fml) * len(nsl) * len(rsl) - df[mask].shape[0],
    )

    previous_sim = df[mask].values[:, :5].tolist()
    todo_list = {}
    for rs_id in range(len(rsl)):
        check_list = np.zeros((len(nsl), len(fml)), dtype=int)
        rs = rsl[rs_id]
        for ns_id in range(len(nsl)):
            ns = nsl[ns_id]
            for fm_id in range(len(fml)):
                fm = fml[fm_id]
                c = [h, w, fm, ns, rs]
                if [h, w, fm, ns, rs] in previous_sim:
                    check_list[ns_id][fm_id] += 1

        missing = np.where(check_list == 0)
        if np.shape(missing)[1] > 0:
            todo_list[rs] = {}
            m_ns = missing[0]
            m_fm = missing[1]
            for i in range(np.shape(missing)[1]):
                ns = nsl[m_ns[i]]
                if ns in todo_list[rs].keys():
                    todo_list[rs][ns].append(fml[m_fm[i]])
                else:
                    todo_list[rs][ns] = [fml[m_fm[i]]]

    end_time = time.time()
    print("time delta %5.3f seconds" % (end_time - start_time))
    return todo_list
