

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
                
  

def MakeFeaturePlots(df_final, features, feature_range, region, sig_back_era, OutputDirName='Output'):
    import os
    import matplotlib.pyplot as plt
    from matplotlib.ticker import AutoLocator, AutoMinorLocator
    print("Making "+region+" region feature plots")

    sig, back, era = sig_back_era.split("_")[:3]
    try:
        os.mkdir(OutputDirName+sig_back_era+"/")
    except FileExistsError:
        pass
    try:
        os.mkdir(OutputDirName+sig_back_era+"/"+region+"/")
    except FileExistsError:
        pass
    colors = ["b", "darkorange"]
    for m in range(len(features)):
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        for i, cate in enumerate([sig, back]):
            df_weight = df_final.loc[(df_final["Category"]==cate)
                        & (df_final["region"] ==region)
                        & (df_final["Dataset"]=="Test"), "NewWt"]
            df_final.loc[(df_final["Category"]==cate)
                        & (df_final["region"] ==region)
                        & (df_final["Dataset"]=="Test"), features[m]].hist(histtype='step', 
                                                                    bins=40,
                                                                    range=(feature_range[region][features[m]][0], feature_range[region][features[m]][1]), 
                                                                    alpha=1,
                                                                    ax=ax, 
                                                                    density=True,
                                                                    ls='-', 
                                                                    color=colors[i],
                                                                    weights =df_weight/df_weight.sum(),
                                                                    linewidth=1,
                                                                    grid=False,
                                                                    label=cate+": test")
            df_weight = df_final.loc[(df_final["Category"]==cate)
                        & (df_final["region"] ==region)
                        & (df_final["Dataset"]=="Train"), "NewWt"]
            df_final.loc[(df_final["Category"]==cate)
                        & (df_final["region"] ==region)
                        & (df_final["Dataset"]=="Train"), features[m]].hist(histtype='bar', 
                                                                    bins=40,
                                                                    range=(feature_range[region][features[m]][0], feature_range[region][features[m]][1]),
                                                                    color=colors[i],
                                                                    alpha=0.4,
                                                                    ax=ax, 
                                                                    density=True,
                                                                    weights =df_weight/df_weight.sum(),
                                                                    grid=False,
                                                                    label=cate+": train")    
        fig.text(0.13, 0.9, "CMS", fontsize=14, fontweight="bold")
        fig.text(0.23, 0.9, "work-in-progress", fontsize=10)
        ax.tick_params(axis = "x", direction="in", top=True, right=True)
        ax.tick_params(axis = "y", direction="in", top=True, right=True) 
        plt.margins(1)                       
        ax.legend(loc='upper right', ncol=2)
        ax.set_xlabel(features[m])
        ax.set_ylabel("a.u.")
        plt.xlim(feature_range[region][features[m]][0], feature_range[region][features[m]][1])
        if feature_range[region][features[m]][2]:
            ax.set_yscale("log")
        # ax.set_title(features[m]+" ("+Set+" Dataset)")
        plt.savefig(OutputDirName+sig_back_era+"/"+region+"/"+features[m]+".png", dpi=600)
        print(OutputDirName+sig_back_era+"/"+region+"/"+features[m]+".png has been saved!")
