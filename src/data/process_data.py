import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize
import json
from os.path import exists


def get_output_filename(file_id, fn):
    out_dir = "/".join(fn.split("/")[:-1]) + "/"
    fn_root = ".".join(fn.split(".")[:-1])
    fn = fn_root + "_" + file_id + ".png"
    return fn


def process_raw_data(raw_df):
    processed_df = raw_df
    if "raw_memory" in raw_df.columns.values: # results computed with new code
        processed_df["fear_memory"] = (raw_df["raw_memory"] - 1) / 2
    else: # results computed with old version of code...
        processed_df["fear_memory"] = (raw_df["fear_memory"] - 1) / 2
    return processed_df


def complex_agg(df):
    def agg_function(x):
        aggs_dict = {"count": x["result"].count(), "solved": (x["result"] == 0).sum()}
        return pd.Series(aggs_dict, index=[key for key in aggs_dict.keys()])

    return df.groupby(["nbr_snakes", "fear_memory"]).apply(agg_function)


def r2(x, y, a, fit):
    # determine quality of the fit
    squaredDiffs = np.square(y - fit(x, a))
    squaredDiffsFromMean = np.square(y - np.mean(y))
    rSquared = 1 - np.sum(squaredDiffs) / np.sum(squaredDiffsFromMean)
    return rSquared


def draw_fm_dep(filename, norm_res, config, defaults):
    ### Produces plot that shows proportion of mazes solved as a function of
    ### the fear memory for specific snake populations.
    cax = config["process_data"]["fm_plot"]
    dax = defaults["process_data"]["fm_plot"]
    axes_translation = get_data("axes_translation", config, defaults)
    colors = get_data("colors", cax, dax)
    snake_populations = get_data("snake_populations", cax, dax)
    highlight_populations = get_data("highlight_populations", cax, dax)
    if snake_populations:
        nrt = norm_res.transpose()[snake_populations]
    else:
        nrt = norm_res.transpose()
        snake_populations = nrt.columns.values
    x = nrt.index
    print(nrt)
    fig, ax = plt.subplots()
    hpx = []
    hpy = []
    if "highlight_points" in cax.keys():
        hp = cax["highlight_points"]
        points = hp["points"]
        for p in points:
            hpx.append(p["x"])
            hpy.append(nrt[p["col"]].loc[p["x"]])
        plt.plot(
            hpx,
            hpy,
            marker=hp["marker"],
            markersize=hp["markersize"],
            linewidth=hp["linewidth"],
            color=hp["color"],
        )
    for sp_id in range(len(snake_populations)):
        sp = snake_populations[sp_id]
        if sp in highlight_populations:
            plt.plot(
                x.values,
                nrt[sp].values,
                marker=".",
                markersize=15,
                linestyle="-",
                linewidth=1.5,
                label="%s cat" % (sp) + "s" * bool(sp > 1),
            )
        else:
            plt.plot(
                x.values,
                nrt[sp].values,
                marker=".",
                linestyle=":",
                linewidth=1,
                label="%s cat" % (sp) + "s" * bool(sp > 1),
            )
    plt.xlabel(axes_translation[x.name])
    plt.ylabel("Survival rate [1]")
    xlim = get_data("xlim", cax, dax)
    ylim = get_data("ylim", cax, dax)
    xticks = get_data("xticks", cax, dax)
    yticks = get_data("yticks", cax, dax)
    if xticks == None and hpx != []:
        xticks = [np.round(x, 2) for x in hpx]
        if xlim:
            xticks += xlim
    if yticks == None and hpy != []:
        yticks = [np.round(y, 2) for y in hpy]
        if ylim:
            yticks += ylim
    if xticks:
        ax.set_xticks(xticks)
    if yticks:
        ax.set_yticks(yticks)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    ax.spines["top"].set_visible(True)
    ax.spines["right"].set_visible(True)
    # # plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    if "legend" in cax:
        lgnd = cax["legend"]
        # print(cax["legend"].get("loc", 0))
        if "bbox_to_anchor" in lgnd:
            plt.legend(loc=lgnd.get("loc", 0), bbox_to_anchor=lgnd.get("bbox_to_anchor", (1,1)))
        else:
            plt.legend(loc=lgnd.get("loc", 0))
    if "grid" in cax:
        cg = cax["grid"]
        dg = dax["grid"]
        plt.grid(
            color=get_data("color", cg, dg),
            axis=get_data("axis", cg, dg),
            linestyle=get_data("linestyle", cg, dg),
            linewidth=get_data("linewidth", cg, dg),
        )

    if "size_inches" in cax:
        # fig.set_size_inches(6, 4)
        print(get_data("size_inches", cax, dax))
        fig.set_size_inches(get_data("size_inches", cax, dax))
    plt.savefig(filename, dpi=get_data("dpi", cax, dax))


def negexp(x, a):
    return np.exp(-a * x)


def draw_ns_dep(filename, norm_res, config, defaults):
    ### Produces plot that shows proportion of mazes solved as a function of
    ### the number of snakes for specific fear memory values.
    cax = config["process_data"]["ns_plot"]
    dax = defaults["process_data"]["ns_plot"]
    axes_translation = get_data("axes_translation", config, defaults)
    colors = get_data("colors", cax, dax)
    fear_interpretation = get_data("fear_interpretation", config, defaults)
    fm_populations = get_data("fm_populations", cax, dax)
    if fm_populations:
        nr = norm_res[fm_populations]
    else:
        nr = norm_res
        fm_populations = nr.columns.values
    x = nr.index
    fig, ax = plt.subplots()
    hpx = []
    hpy = []
    if "highlight_points" in cax.keys():
        hp = cax["highlight_points"]
        points = hp["points"]
        for p in points:
            hpx.append(p["x"])
            hpy.append(nr[p["col"]].loc[p["x"]])
        plt.plot(
            hpx,
            hpy,
            marker=hp["marker"],
            markersize=hp["markersize"],
            linewidth=hp["linewidth"],
            color=hp["color"],
        )
    for fm_id in range(len(fm_populations)):
        fm = fm_populations[fm_id]
        [a], cv = scipy.optimize.curve_fit(negexp, x.values, nr[fm].values)
        plt.plot(
            x.values,
            negexp(x.values, a),
            color=colors[fm_id % len(colors)],
            linestyle="--",
        )
        plt.plot(
            x.values,
            nr[fm].values,
            color=colors[fm_id % len(colors)],
            marker=".",
            linewidth=0,
            label="%s: fear memory lasts %i step"
            % (fear_interpretation[str("%3.1f" % (fm))], int(fm))
            + "s" * (int(fm) != 1)
            + "; fit: $R^2$=%4.2f" % (r2(x.values, nr[fm].values, a, negexp)),
        )
    plt.xlabel(axes_translation[x.name])
    plt.ylabel(
        "Proportion of %ix%i mazes solved"
        % (get_data("height", config, defaults), get_data("width", config, defaults))
    )
    xlim = get_data("xlim", cax, dax)
    ylim = get_data("ylim", cax, dax)
    xticks = get_data("xticks", cax, dax)
    yticks = get_data("yticks", cax, dax)
    if xticks == None and hpx != []:
        xticks = [np.round(x, 2) for x in hpx]
        if xlim:
            xticks += xlim
    if yticks == None and hpy != []:
        yticks = [np.round(y, 2) for y in hpy]
        if ylim:
            yticks += ylim
    if xticks:
        ax.set_xticks(xticks)
    if yticks:
        ax.set_yticks(yticks)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # # plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
    if "legend" in cax:
        plt.legend(loc=cax["legend"].get("loc", 0))
    if "grid" in cax:
        cg = cax["grid"]
        dg = dax["grid"]
        plt.grid(
            color=get_data("color", cg, dg),
            axis=get_data("axis", cg, dg),
            linestyle=get_data("linestyle", cg, dg),
            linewidth=get_data("linewidth", cg, dg),
        )
    plt.savefig(filename, dpi=get_data("dpi", cax, dax))


def get_data(param, config, defaults):
    if param in config.keys():
        return config[param]
    elif param in defaults.keys():
        return defaults[param]
    else:
        print(
            "Error: parameter [%s] neither defined in config.json, nor in defaults.json"%param
        )
        exit(1)


def get_data_filename(params, config, defaults):
    ofns = []
    ddir = get_data("data_directory", config["results"], defaults["results"])
    dfn = get_data("data_filename", config["results"], defaults["results"])
    if exists(ddir + dfn):
        ofns.append(ddir + dfn)
    alt_dfn = get_data(
        "alternate_data_filename", config["process_data"], defaults["process_data"]
    )
    if exists(ddir + alt_dfn):
        ofns.append(ddir + alt_dfn)
    selected_fn = params["file"]
    fn = None
    if len(ofns) == 1:
        fn = ofns[0]
    if selected_fn in ofns:
        fn = selected_fn
    if (fn == None) and len(ofns) > 1:
        print("Warning: Multiple filename defined in config file.")
        print("         Defaulting to alternate_data_filename: %s" % (alt_dfn))
        fn = ddir + alt_dfn
    if fn == None:
        print(
            "Error, unable to determine data file to be processed. Please specify. Options found in config.json are:"
        )
        if len(ofns) > 1:
            print("Options are:")
            for i in range(len(ofns)):
                print("- %s" % (ofns[i]))
        exit(1)
    return fn


def process_data(df, config, defaults, fn, limit=None):
    if limit == None:
        dfx = df
        fm_fn = get_output_filename("fm", fn)
        ns_fn = get_output_filename("ns", fn)
    else:
        dfx = df[df["random_seed"] < limit]
        fm_fn = get_output_filename("fm_%i" % (limit), fn)
        ns_fn = get_output_filename("ns_%i" % (limit), fn)
    res = complex_agg(dfx).unstack()
    norm_res = res["solved"] / res["count"]
    if "fm_plot" in config["process_data"].keys():
        draw_fm_dep(fm_fn, norm_res, config, defaults)
    if "ns_plot" in config["process_data"].keys():
        draw_ns_dep(ns_fn, norm_res, config, defaults)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--profile", help="profile name (as defined in config.json)"
    )
    parser.add_argument("-f", "--file", help="input filename")
    params = vars(parser.parse_args())
    # print(params)

    with open("defaults.json", "r") as f:
        defaults = json.load(f)
    with open("config.json", "r") as f:
        config = json.load(f)[params["profile"]]

    if not "process_data" in config:
        print("Configuration %s does not contain data processing instructions.")
        print("Nothing to be processed.")
        exit(0)

    fn = get_data_filename(params, config, defaults)

    print("Processing file %s" % (fn))
    df = process_raw_data(pd.read_csv(fn))
    # process_data(df, config, defaults, fn, limit=None)

    res = complex_agg(df).unstack()
    minmin = res["count"].min().min()
    process_data(df, config, defaults, fn, limit=minmin)

    # limits = [50, 100, 150, 200, 250]
    # for limit in limits:
    #     process_data(df, config, defaults, fn, limit=limit)
