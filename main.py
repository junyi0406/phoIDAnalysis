# %%
import os 
import sys
import json
import pickle as pk
import pandas as pd
import seaborn as sns
import RootFileLib as rfl
import matplotlib.pyplot as plt
import DedicateTrainer as dt

# %%
if __name__=="__main__":
    
   # if(len(sys.argv)) < 2:
   #    print("no args")
   #    exit()
   # else:
   #    config_path = os.getcwd()+"/"+ sys.argv[1]
      
      

   ### prepare the sample 
   # eras = ["UL18"]
   # eras = ["UL16preVFP", "UL16postVFP", "UL17", "UL18"]
   # for cate in ["HZg", "SMZg", "DYJets"]:
   #    for era in eras:
   #       df = rfl.read_minitree(config_path=config_path, era=era, cate=cate, useDask=True)
   #       rfl.save_dfs(df, "DataFrame/"+cate+"/"+cate+"_"+era+"_noPtMat.pk")
   
   # ### prepare dataset
   config_path = os.getcwd()+"/"+ sys.argv[1]
   with open(config_path, "r") as config:
      config = json.load(config)

   for files in config["sig_back"][-2:]:
      print(files)
      print("Loading dataFrame...")
      df = pd.concat([rfl.load_dfs(file) for file in files])
      df = df.reset_index()
      del df["entry"]
      del df["subentry"]
      for substr in files:
         era = rfl.find_era(substr)
         if substr.find("HZg") != -1:
            cates = ["HZg", "DYJets"]
            break
         else:     
            cates = ["SMZg", "DYJets"]  
      print("Spliting event...")

      df = dt.split_test_train_validate(df, region="barrel", cates=cates, train_ratio=0.35, test_ratio=0.5, validation_ratio=0.15)
      df = dt.split_test_train_validate(df, region="endcap", cates=cates, train_ratio=0.35, test_ratio=0.5, validation_ratio=0.15)
   
      # Check the test-train dataset
      # dt.check_test_train_dataset(df.loc[df["region"] == "barrel", :], filename="picture/split/train_test_split_barrel_"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu.png")
      # dt.check_test_train_dataset(df.loc[df["region"] == "endcap", :], filename="picture/split/train_test_split_endcap_"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu.png")

      ### Do the pT eta reweighted, The TrainConfig is needed.
      df["NewWt"] = df['xsecwt']
      print("reweighting...")
      df["NewWt"] = dt.df_pteta_rwt(
         df, cates[0], cates[1],
         ptbins=config["ptbins"], etabins_barrel=config["etabins_barrel"],etabins_endcap=config["etabins_endcap"],
         ptvar=config["ptwtvar"], etavar=config["etawtvar"],
         SumWeightCol="xsecwt", NewWeightCol="NewWt"
      )
      print("After reweighting> In Testing:")
      dt.check_reweight_plot(df[df["region"] == "barrel"], config, "picture/rewt/"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu/"+cates[0]+"_"+cates[1]+"_"+era+"_", "barrel")
      dt.check_reweight_plot(df[df["region"] == "endcap"], config, "picture/rewt/"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu/"+cates[0]+"_"+cates[1]+"_"+era+"_", "endcap")
      rfl.save_dfs(df, "DataFrame/phoDataSet/"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu.pk")
      print("DataFrame/phoDataSet/"+cates[0]+"_"+cates[1]+"_"+era+"_noPtMat_onlyZtoeeuu.pk has been saved!")


   ###### plot the correlation plots
   
   # for filename in os.listdir("DataFrame/phoDataSet/"):
   #     sig_back_era = filename[:-3]
   #     df = rfl.load_dfs("DataFrame/phoDataSet/"+sig_back_era+".pk")
   #     sig, back, era = sig_back_era.split("_")
   #     plot_corre(df, sig_back_era, Classes=[sig, back], MVA=config["MVAs"]["XGBoost"], OutDir="picture/VarCorrel/")

   ##### plot the features
   # filename = "HZg_DYJets_UL18_noPtMat_onlyZtoeeuu.pk"
   # sig_back_era = filename[:-3]
   # df = rfl.load_dfs("DataFrame/Results/"+filename)
   # MVA_config = config["MVAs"]["XGBoost"]
   # dt.MakeFeaturePlots(df, MVA_config["features"]["barrel"], MVA_config["features_range"], "barrel", sig_back_era, OutputDirName="picture/Features/")
   # dt.MakeFeaturePlots(df, MVA_config["features"]["endcap"], MVA_config["features_range"], "endcap", sig_back_era, OutputDirName="picture/Features/")
   # del df

   ###### train with XGBoost
   # df = rfl.load_dfs("DataFrame/phoDataSet/HZg_DYJets_UL18_noPtMat_onlyZtoeeuu.pk")
   # MVA_config = config["MVAs"]["XGBoost"]
   # outstr = "HZg_DYJets_UL18_noPtMat_onlyZtoeeuu_opt_params"
   # try:
   #    os.mkdir("Train_result/"+outstr+"/")
   # except FileExistsError:
   #    pass
   # dt.train_xgb(df, "barrel", MVA_config, OutDir="Train_result/"+outstr+"/")
   # dt.train_xgb(df, "endcap", MVA_config, OutDir="Train_result/"+outstr+"/")
   
   ###### do the predict
   # predicted at first
   # df = rfl.load_dfs("DataFrame/phoDataSet/"+outstr+".pk")
   # df = dt.predict(df=df, region="barrel", path_to_result = "Train_result/"+outstr+"/", XGBConf=MVA_config)
   # df = dt.predict(df=df, region="endcap", path_to_result = "Train_result/"+outstr+"/", XGBConf=MVA_config)
   # rfl.save_dfs(df, file_name="DataFrame/Results/"+outstr+".pk")
   
   ###### plot score
   # df = rfl.load_dfs("DataFrame/Results/"+outstr+".pk")
   # df["_phoTMVA"] = df["_phoTMVA"]/2 + 0.5
   # dt.plot_predicted_score(df, "barrel", "XGB_pred", "picture/TrainResult/"+outstr+"/")
   # dt.plot_predicted_score(df, "endcap", "XGB_pred", "picture/TrainResult/"+outstr+"/")

   ###### check the importance
   # with open("Train_result/"+outstr+"/barrel_modelXGB.pk", "rb") as f:
   #    cv_barrel = pk.load(f)
   # with open("Train_result/"+outstr+"/endcap_modelXGB.pk", "rb") as f:
   #    cv_endcap = pk.load(f)
   # dt.plot_error(cv_barrel, "barrel", OutDir="picture/TrainResult/"+outstr+"/")
   # dt.plot_error(cv_endcap, "endcap", OutDir="picture/TrainResult/"+outstr+"/")
   # dt.plot_importance(cv_barrel, MVA_config["features"], region="barrel", OutDir="picture/Importance/"+outstr+"/")
   # dt.plot_importance(cv_endcap, MVA_config["features"], region="endcap", OutDir="picture/Importance/"+outstr+"/")
   # dt.plot_final_ROC_curve(df, "barrel", MVA_config, OutDir="picture/TrainResult/"+outstr+"/")
   # dt.plot_final_ROC_curve(df, "endcap", MVA_config, OutDir="picture/TrainResult/"+outstr+"/")
   # dt.plot_best_params(pk.load(open("Train_result/"+outstr+"/barrel_best_params.pk", "rb")), "picture/TrainResult/"+outstr+"/barrel_")
   # dt.plot_best_params(pk.load(open("Train_result/"+outstr+"/endcap_best_params.pk", "rb")), "picture/TrainResult/"+outstr+"/endcap_")