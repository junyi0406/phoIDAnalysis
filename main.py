# %%
import os 
import sys
import json
import dask
import pickle
import pandas as pd
import seaborn as sns
import RootFileLib as rfl
import matplotlib.pyplot as plt
import DedicateTrainer as dt
from DedicateTrainer import train_xgb, save_scalar
from DedicateTrainer import df_pteta_rwt, split_category, save_scalar
from DedicateTrainer import plot_corre, check_reweight_plot, check_test_train_dataset
# %%
if __name__=="__main__":
    # if(len(sys.argv)) < 2:
    #     print("no args")
    #     exit()
    # else:
    #     config_path = os.getcwd()+"/"+ sys.argv[1]
        
        

    ### prepare the sample 
    # eras = [ "UL17", "UL18"]
    # eras = ["UL16preVFP", "UL16postVFP", "UL17", "UL18"]
    # for cate in sys.argv[2:]:
    #     for era in eras:
    #         df = rfl.read_minitree(config_path=config_path, era=era, cate=cate, useDask=True)
    #         rfl.save_dfs(df, "DataFrame/"+cate+"/"+cate+"_"+era+".pk")
     
    # ### prepare dataset
    config_path = os.getcwd()+"/"+ sys.argv[1]
    with open(config_path, "r") as config:
        config = json.load(config)

    # for files in config["sig_back"]:
    #     print(files)
    #     print("Loading dataFrame...")
    #     df = pd.concat([rfl.load_dfs(file) for file in files])
    #     df = df.reset_index()
    #     del df["entry"]
    #     del df["subentry"]
    #     for substr in files:
    #         era = rfl.find_era(substr)
    #         if substr.find("HZg") != -1:
    #             cates = ["HZg", "DYJets"]
    #             break
    #         else:     
    #             cates = ["SMZg", "DYJets"]  
    #     print("Spliting event...")
    #     df = split_category(df, 0.45, cates)
        
    #     # Check the test-train dataset
    #     check_test_train_dataset(df.loc[df["region"] == "barrel", :], filename="picture/split/train_test_split_barrel_"+cates[0]+"_"+cates[1]+"_"+era+".png")
    #     check_test_train_dataset(df.loc[df["region"] == "endcap", :], filename="picture/split/train_test_split_endcap_"+cates[0]+"_"+cates[1]+"_"+era+".png")

    #     #### Do the pT eta reweighted, The TrainConfig is needed.
    #     df["NewWt"] = df['xsecwt']
    #     print("reweighting...")
    #     df["NewWt"] = df_pteta_rwt(
    #         df, cates[0], cates[1],
    #         ptbins=config["ptbins"], etabins_barrel=config["etabins_barrel"],etabins_endcap=config["etabins_endcap"],
    #         ptvar=config["ptwtvar"], etavar=config["etawtvar"],
    #         SumWeightCol="xsecwt", NewWeightCol="NewWt"
    #     )
    #     # print("After reweighting> In Testing:")
    #     check_reweight_plot(df[df["region"] == "barrel"], config, "picture/rewt/"+cates[0]+"_"+cates[1]+"_"+era+"/"+cates[0]+"_"+cates[1]+"_"+era+"_", "barrel")
    #     check_reweight_plot(df[df["region"] == "endcap"], config, "picture/rewt/"+cates[0]+"_"+cates[1]+"_"+era+"/"+cates[0]+"_"+cates[1]+"_"+era+"_", "endcap")
    #     rfl.save_dfs(df, "DataFrame/phoDataSet/"+cates[0]+"_"+cates[1]+"_"+era+".pk")
    #     print("DataFrame/phoDataSet/"+cates[0]+"_"+cates[1]+"_"+era+".pk has been saved!")


    #### append column of ESoverE
    # for filename in os.listdir("DataFrame/phoDataSet/"):
    #     sig_back_era = filename[:-3]
    #     df = rfl.load_dfs("DataFrame/phoDataSet/"+sig_back_era+".pk")
    #     df["_phoESoverE"] = (df.loc[df["region"]=="endcap", "_phoESEnP1"] + df.loc[df["region"]=="endcap", "_phoESEnP2"]) / df.loc[df["region"]=="endcap", "_phoSCRawE"]
    #     rfl.save_dfs(df, file_name="DataFrame/phoDataSet/"+filename) 
    
    ###### plot the correlation plots
    # sig_back_era = sys.argv[2]
    # df = rfl.load_dfs("DataFrame/phoDataSet/"+sig_back_era+".pk")
    # df["_phoESoverE"] = (df.loc[df["region"]=="endcap", "_phoESEnP1"] + df.loc[df["region"]=="endcap", "_phoESEnP2"]) / df.loc[df["region"]=="endcap", "_phoSCRawE"]
    # sig, back, era = sig_back_era.split("_")
    
    # plot_corre(df, sig_back_era, Classes=[sig, back], MVA=config["MVAs"]["XGBoost"], OutDir="picture/VarCorrel/")

    ###### train with XGBoost

    # df = rfl.load_dfs("DataFrame/phoDataSet/HZg_DYJets_UL17.pk")
    MVA_config = config["MVAs"]["XGBoost"]
    # do scalar at first
    # try:
    #     os.mkdir("Train_result/HZg_DYJets_UL17/")
    # except FileExistsError:
    #     pass
    # sc_barrel, sc_endcap = save_scalar(df, MVA_config["features"], MVA_config["Scalar"], OutDir="Train_result/HZg_DYJets_UL17/")
    # search_barrel, search_endcap = train_xgb(df, MVA_config, "Train_result/HZg_DYJets_UL17/")

    ###### check the importance
    with open("Train_result/HZg_DYJets_UL17/barrel_modelXGB.pk", "rb") as f:
        cv_barrel = pickle.load(f)
    with open("Train_result/HZg_DYJets_UL17/endcap_modelXGB.pk", "rb") as f:
        cv_endcap = pickle.load(f)

    dt.plot_importance(cv_barrel, MVA_config["features"], region="barrel", OutDir="picture/Importance/HZg_DYJets_UL17/")
    dt.plot_importance(cv_endcap, MVA_config["features"], region="endcap", OutDir="picture/Importance/HZg_DYJets_UL17/")
