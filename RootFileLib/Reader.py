import os
import sys
sys.path.append("..")
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

def find_era(string):
    if string.find("UL16") != -1:
        if string.find("preVFP") != -1:
            era = "UL16preVFP"
        else:
            era = "UL16postVFP"
    else:
        if string.find("UL17") != -1:
            era = "UL17"
        else:
            era = "UL18"
    return era
        

def read_minitree(config_path, era, cate, debug = False, useDask = False):
    import dask.dataframe as dd
    from dask.diagnostics import ProgressBar
    
    with open(config_path, "r") as config:
        config = json.load(config)
    tree_path = config["tree_path"]
    debug     = config["debug"]
    branches  = config["branches"]["reco_pho"] + config["branches"]["UL_only"]
    dataset   = config["MCSample"][cate]
    selections   = config["MCSample"][cate]["pre-selection"]
    eras      = dataset["era"]
    path      = dataset["path"][eras.index(era)]

    
    if useDask:
        if isinstance(path, list):
            df_merged = []
            for i, filename in enumerate(path):
                filename = filename[:-5]+"_noPtMat"+filename[-5:]
                print("loading: ", filename)
                df_merged.append(dask.delayed(read_single_rootfile)(filename, tree_path, branches, selections, cate, debug))
            df_merged = dask.delayed(pd.concat)(df_merged)
        elif isinstance(path, str):
            path = path[:-5]+"_noPtMat"+path[-5:]
            print("loading: ", path)
            df_merged = dask.delayed(read_single_rootfile)(path, tree_path, branches, selections, cate, debug)
        else:
            print("unsupport data path type")
            exit()

        print("start computing")
        df_merged = dd.from_delayed(df_merged)
        
        with dask.config.set(pool=ThreadPoolExecutor(3)):
            with ProgressBar():
                result = df_merged.compute()
                # result.reset_index(inplace = True, drop = True)
    else:
        print("This function hasn't been finished.")
        exit()
    print("dataframe are all set")
    return result
    
def read_single_rootfile(filename, tree_path, branches, selections, Category, debug, stop_entry=1000):
    tree = uproot3.open(filename)[tree_path]
    
    if debug:
        for selection in selections:
            df = tree.pandas.df(branches=branches,entrystop=stop_entry).query(selection)
    else:
        for selection in selections:
            df = tree.pandas.df(branches=branches).query(selection)

    df["Category"] = Category
    df["xsecwt"] = df["_phoXSWt"]
    df.loc[((df["_phoSCEta"]<2.5) & (df["_phoSCEta"] > 1.556)) | ((df["_phoSCEta"]>-2.5) & (df["_phoSCEta"] < -1.556)), "region"] = "endcap"
    df.loc[((df["_phoSCEta"]<1.4442) & (df["_phoSCEta"] > -1.4442)), "region"] = "barrel"
    return df
    


