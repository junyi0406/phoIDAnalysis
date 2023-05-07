import os 
import sys
import json
import seaborn as sns
import RootFileLib as rfl
import matplotlib.pyplot as plt
from DedicateTrainer.splitter import spit_promptPho
from DedicateTrainer.PtEtarwt import df_pteta_rwt, check_reweight_plot


if __name__=="__main__":
    ### prepare the sample 
    # if(len(sys.argv)) < 2:
    #     print("no args")
    #     exit()
    # else:
    #     config_path = os.getcwd()+"/"+ sys.argv[1]
    #     cates = sys.argv[2:]
    # procs = []
    # eras = ["UL16preVFP", "UL16postVFP", "UL17", "UL18"]
    # for cate in cates:
    #     for era in eras:
    #         df = rfl.read_minitree(config_path=config_path, era=era, cate=cate, useDask=True)
    #         rfl.save_dfs(df, "DataFrame/"+cate+"/"+cate+"_"+era+".pk")
    
    train_config_path = os.getcwd()+"/"+ sys.argv[1]
    
    with open(train_config_path, "r") as config:
        config = json.load(config)
    
    print("Loading dataFrame...")
    df = rfl.load_dfs("DataFrame/HZg/HZg_UL18.pk")
    print("Spliting event...")
    TestIndices, TrainIndices = spit_promptPho(df, 0.02, 5)
    
    ## Check the test-train dataset
    # fig, axes = plt.subplots(1, 1, figsize=(10, 5))
    # kplot=sns.countplot(x="_phoIsPrompt", data=df, ax=axes,hue='Dataset',palette=['#432371',"#FAAE7B","black"])
    # for p in kplot.patches:
    #     kplot.annotate(format(p.get_height(), '.2f'), (p.get_x() + p.get_width() / 2., p.get_height()), ha = 'center', va = 'center', xytext = (0, 5), textcoords = 'offset points',size=8)
    # axes.set_title("Number of samples")
    # plt.savefig("picture/rewt/TotalStat_TrainANDTest.png")
    
    
    #### Do the pT eta reweighted, The TrainConfig is needed.
    df["NewWt"] = df['xsecwt']
    ReweightClass = config["WhichClassToReweightTo"]
    print("After reweighting> In Training:")
    df.loc[TrainIndices, "NewWt"] = df_pteta_rwt(
        df.loc[TrainIndices],"_phoIsPrompt",
        ptw=config["ptbins"], etaw=config["etabins"],
        pt=config["ptwtvar"], eta=config["etawtvar"],
        SumWeightCol="xsecwt", NewWeightCol="NewWt",
    )
    print("After reweighting> In Testing:")
    df.loc[TestIndices, "NewWt"] = df_pteta_rwt(
        df.loc[TestIndices],"_phoIsPrompt",
        ptw = config["ptbins"] , etaw = config["etabins"],
        pt  = config["ptwtvar"], eta  = config["etawtvar"],
        SumWeightCol = "xsecwt", NewWeightCol = "NewWt"
    )
    check_reweight_plot(df, config, "picture/rewt/")
    