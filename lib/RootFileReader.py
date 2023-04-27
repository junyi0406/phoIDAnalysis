import os
import dask
import json
import uproot3 
import pandas as pd


def read_rootfile(config_path):
    with open(config_path, "r") as config:
        config = json.load(config)
    tree_path = "ggNtuplizer/EventTree"

    tree = uproot3.open()[tree_path]
    
    df = tree.pandas.df(branches=branches,flatten=True,entrystop=10).query("nPho >= 1")