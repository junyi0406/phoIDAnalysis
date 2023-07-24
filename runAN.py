

import json
import pandas as pd
import RootFileLib as rfl
import DedicateTrainer as dt


if __name__=="__main__":
    
    cates = ["HZg", "DYJets"]
    config_path = "Configs/TrainConfig.json"
    signal_df = "DataFrame/HZg/HZg_UL18_noPtMat.pk"
    background_df = "DataFrame/DYJets/DYJets_UL18_noPtMat.pk"
    era = rfl.find_era(signal_df)
  
    
    with open(config_path, "r") as config:
        config = json.load(config)
    
    # query same number of event in signal and background
    files = [signal_df, background_df]
    dfs   = [rfl.load_dfs(file) for file in files]
    num_event = [len(df.index) for df in dfs]
    df = pd.concat([df.sample(n=min(num_event)) for df in dfs])
    df = df.reset_index()
    del df["entry"]
    del df["subentry"]
    
    # train-test-validation split
    df = dt.split_test_train_validate(df, region="barrel", cates=cates, train_ratio=0.35, test_ratio=0.5, validation_ratio=0.15)
    df = dt.split_test_train_validate(df, region="endcap", cates=cates, train_ratio=0.35, test_ratio=0.5, validation_ratio=0.15)
    
    # pt-eta reweighting
    df["xsecwt"] = 1
    df["NewWt"] = dt.df_pteta_rwt(
        df, cates[0], cates[1],
        ptbins=config["ptbins"], 
        etabins_barrel=config["etabins_barrel"],etabins_endcap=config["etabins_endcap"],
        ptvar="_phoCalibEt", etavar="_phoSCEta",
        SumWeightCol="xsecwt", NewWeightCol="NewWt"
    )
   
    dt.check_reweight_plot(df, config, "picture/rewt/"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu_eqevn/", "barrel")
    dt.check_reweight_plot(df, config, "picture/rewt/"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu_eqevn/", "endcap")
    rfl.save_dfs(df, "DataFrame/phoDataSet/"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu_eqevn.pk")
    print("DataFrame/phoDataSet/"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu_eqevn.pk has been saved!")
    
    # train with XGBoost
    