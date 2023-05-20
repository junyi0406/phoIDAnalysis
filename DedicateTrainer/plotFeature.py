

def plot_corre(df, sig_back_era, Classes=[''],MVA={}, OutDir=""):
    import os 
    import seaborn as sns
    import matplotlib.pyplot as plt
    sig, back, era = sig_back_era.split("_")
    try:
        os.makedirs(OutDir)
    except FileExistsError:
        pass
    try:
        os.makedirs(OutDir + sig_back_era + "/")
    except FileExistsError:
        pass
    for cat in Classes:
        try:
            os.makedirs(OutDir + sig_back_era + "/" + cat +"/")
        except FileExistsError:
            pass

    for C in Classes:
        for k in ["Train","Test"]:
            for region in ["barrel", "endcap"]:
                fig, axes = plt.subplots(1, 1, figsize=(len(MVA["features"][region])/2, len(MVA["features"][region])/2))
                cor = df.loc[(df['region'] == region) & (df['Dataset'] == k) & (df['Category'] == C)][MVA["features"][region]].corr()
                sns.heatmap(cor, annot=True, cmap=plt.cm.Reds,ax=axes,annot_kws={"size":len(MVA["features"][region])/2.5})
                axes.collections[0].set_clim(-0.5, 1) 
                axes.tick_params(axis='x', labelsize=len(MVA["features"][region])/2)
                axes.tick_params(axis='y', labelsize=len(MVA["features"][region])/2)
                axes.tick_params(axis = "x", bottom=False, left=False, labelrotation = 85)
                axes.tick_params(axis = "y", bottom=False, left=False, labelrotation = 10)
                plt.margins(2.)
                plt.subplots_adjust(bottom=0.22, left=0.22)
                fig.text(0.21, 0.9, "CMS", fontsize=14, fontweight="bold")
                fig.text(0.3, 0.9, "work-in-progress", fontsize=10)
                fig.savefig(OutDir+"/"+ sig_back_era + "/" + C +"/"+region+"_"+k+".png", dpi=900)
                
                
def plot_importance(cv, features, region="", OutDir=""):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 1, figsize=(12/1.3, 12/2))
    plt.subplots_adjust(left=0.2)
    fig.text(0.2, 0.9, "CMS", fontsize=18, fontweight="bold")
    fig.text(0.27, 0.9, "work-in-progress", fontsize=14)
    ax.tick_params(axis = "x", direction="in", left=False)
    ax.tick_params(axis = "y", direction="in", left=False)
    bars = ax.barh(features[region], cv.best_estimator_.feature_importances_, color=[(0.9, 0.4, 0.1)])
    for bars in ax.containers:
        ax.bar_label(bars, label_type="edge", fmt='%.2f', color="k")
    ax.set_xlabel("Xgboost Feature Importance")
    plt.xlim(0, 0.5)
    fig.savefig(OutDir+region+"_Importance_.png")

                

def MakeFeaturePlots(df_final,features,feature_bins,Set="Train",MVA="XGB_1",OutputDirName='Output',cat='Category',label=[""],weight="NewWt",log=False):
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, len(features), figsize=(len(features)*5, 5))
    print("Making "+Set+" dataset feature plots")
    for m in range(len(features)):
        #print(f'Feature {m} is {features[m]}')
        for i,group_df in df_final[df_final['Dataset'] == Set].groupby(cat):
            group_df[features[m]].hist(histtype='step', bins=feature_bins[m], alpha=1,label=label[i], ax=axes[m], density=False, ls='-', weights =group_df[weight]/group_df[weight].sum(),linewidth=1)
            #df_new = pd.concat([group_df, df_new],ignore_index=True, sort=False)                                                                                            
        axes[m].legend(loc='upper right')
        axes[m].set_xlabel(features[m])
        if log:
            axes[m].set_yscale("log")
        axes[m].set_title(features[m]+" ("+Set+" Dataset)")
    plt.savefig(OutputDirName+"/"+MVA+"/"+MVA+"_"+"featureplots_"+Set+".pdf")