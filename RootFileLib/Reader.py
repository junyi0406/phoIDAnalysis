import os
import dask
import json
import uproot3 
import pandas as pd


def read_rootfile(config_path, debug = False):
    with open(config_path, "r") as config:
        config = json.load(config)
    tree_path = config["tree_path"]
    debug     = config["debug"]
    tree_path = config["tree_path"]
    branches  = config["branches"]["common"] + config["branches"]["UL_only"]
    flatten   = config["flatten"]
    
    dfs = []
    for channel in config["Classes"]:
        # process would be a name of sample, i.e. ZGToLLG.
        for era_mode in config["MCSample"]:
            # mode would be a list of production mode for single cate in MCSample 
            # i.e. "HToZG_ggF" or "HToZG_VBF"
            modes = config["MCSample"][era_mode]["production"]
            for idx, mode in enumerate(modes):
                if channel==mode:
                    print("combing {}.root".format(era_mode))
                    path = config["MCSample"][era_mode]["path"][idx]
                    files = filter(lambda name : name[-5:] == ".root", os.listdir(path))
                    # print(files)
                    df_merged = pd.concat([read_single_rootfile(path+file, tree_path, branches, debug, flatten) for file in files])
                    dfs.append( (channel, era_mode, df_merged) )
    print("dataframe are all set")
    return dfs
        


    
def read_single_rootfile(filename, tree_path, branches, debug, flatten, stop_entry=1000, selection=False):
    tree = uproot3.open(filename)[tree_path]
    if debug:
        df = tree.pandas.df(branches=branches,flatten=flatten,entrystop=stop_entry)
    else:
        df = tree.pandas.df(branches=branches,flatten=flatten)
    if isinstance(selection, str):
        df.query(selection)
    return df
    
