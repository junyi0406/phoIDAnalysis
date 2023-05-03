import os
import dask
import json
import uproot3 
import pandas as pd
import pickle as pk
from concurrent.futures import ThreadPoolExecutor

def save_dfs(dfs, file_name):
    with open(file_name, 'wb') as f:
        pk.dump(dfs, f)

def load_dfs(file_name):
    with open(file_name, 'rb') as f:
        dfs = pk.load(f)
    return dfs

def read_rootfile(config_path, era, Category, debug = False, useDask = False):
    # era must be UL16preVFP, UL16postVFP, UL17, UL18
    # Category can be ZGToLLG DYJets HToZG
    import dask.dataframe as dd
    from dask.diagnostics import ProgressBar
    with open(config_path, "r") as config:
        config = json.load(config)
    tree_path = config["tree_path"]
    debug     = config["debug"]
    branches  = config["branches"]["common"] + config["branches"]["UL_only"]
    flatten   = config["flatten"]
    dataset   = config["MCSample"][Category]
    eras      = dataset["era"]
    
    dfs = []
    
    path = dataset["path"][eras.index(era)]

    if useDask:
        if isinstance(path, list): # for the HZg samples
            for i, dir in enumerate(path):
                files = filter(lambda name : name[-5:] == ".root", os.listdir(dir))
                data = [dask.delayed(read_single_rootfile)(dir+file, tree_path, branches, Category+"_"+dataset["production"][i], debug, flatten) for file in files]
                df_merged = dask.delayed(pd.concat)(data)
                dfs.append(df_merged)
        elif isinstance(path, str):
            files = filter(lambda name : name[-5:] == ".root", os.listdir(path))
            data = [dask.delayed(read_single_rootfile)(path+file, tree_path, branches, Category, debug, flatten) for file in files]
            df_merged = dask.delayed(pd.concat)(data)
            dfs.append(df_merged)
        else:
            print("wtf?")
    else:
        print("This function hasn't been finished.")
        exit()
                
    if useDask: 
        print("start computing")
        dfs = dd.from_delayed(dfs)
        # dfs = dfs.compute(scheduler="processes")
        with dask.config.set(pool=ThreadPoolExecutor(6)):
            with ProgressBar():
                result = dfs.compute()
    print("dataframe are all set")
    return result
        
def read_minitree(config_path, debug = False, useDask = False):
    import dask.dataframe as dd
    from dask.diagnostics import ProgressBar
    with open(config_path, "r") as config:
        config = json.load(config)
    tree_path = config["tree_path"]
    debug     = config["debug"]
    branches  = config["branches"]["common"] + config["branches"]["UL_only"]
    flatten   = config["flatten"]

    dfs = []
    for channel in config["Classes"]:
        for sample in config["MiniTree"]:
            production = config["MiniTree"][sample]["production"]
            if channel==production:
                print("reading {}.root".format(sample))
                path = config["MiniTree"][sample]["path"]
                if useDask:
                    dfs.append(dask.delayed(read_single_rootfile)(path, tree_path, branches, sample, debug, flatten))
    if useDask:
        print("start computing")
        dfs = dd.from_delayed(dfs)
        with dask.config.set(pool=ThreadPoolExecutor(8)):
            with ProgressBar():
                result = dfs.compute()
                # result.reset_index(inplace = True, drop = True)
    print("dataframe are all set")
    return result
    
def read_single_rootfile(filename, tree_path, branches, Category, debug, flatten, stop_entry=1000, selection=False):
    tree = uproot3.open(filename)[tree_path]
    if debug:
        df = tree.pandas.df(branches=branches,flatten=flatten,entrystop=stop_entry)
    else:
        df = tree.pandas.df(branches=branches,flatten=flatten)
    if isinstance(selection, str):
        df.query(selection)
    df["Category"] = Category
    return df
    


