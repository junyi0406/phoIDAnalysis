import os 
import sys
import dask
import numpy as np
import pickle as pk
import RootFileLib as rfl
from dask.diagnostics import ProgressBar
from concurrent.futures import ThreadPoolExecutor
from SelectionTools import select_PromtPho_Signal, select_PromtPho_Back

if __name__=="__main__":
    ### prepare the sample 
    if(len(sys.argv)) < 2:
        print("no args")
        exit()
    else:
        config_path = os.getcwd()+"/"+ sys.argv[1]
        cates = sys.argv[2:]
    procs = []
    eras = ["UL16preVFP", "UL16postVFP", "UL17", "UL18"]
    for cate in cates:
        for era in eras:
            df = rfl.read_minitree(config_path=config_path, era=era, cate=cate, useDask=True)
            rfl.save_dfs(df, "DataFrame/"+cate+"/"+cate+"_"+era+".pk")
    
            
 

