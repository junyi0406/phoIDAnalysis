


              
def plot_importance(cv, features, region="", OutDir=""):
    import pandas as pd
    import matplotlib.pyplot as plt
    df = pd.DataFrame(zip(features[region], cv.feature_importances_), columns=["features", "importance"])
    df = df.sort_values(by="importance", ascending=True)
    ax = df.plot.barh(x="features", y="importance", figsize=(12/1.3, 12/2), color=[(0.9, 0.4, 0.1)], legend=False)
    fig = plt.gcf()
    plt.subplots_adjust(left=0.2)
    fig.text(0.2, 0.9, "CMS", fontsize=18, fontweight="bold")
    fig.text(0.27, 0.9, "work-in-progress", fontsize=14)
    ax.tick_params(axis = "x", direction="in", left=False)
    ax.tick_params(axis = "y", direction="in", left=False)
    
    for bars in ax.containers:
        ax.bar_label(bars, label_type="edge", fmt='%.2f', color="k")
    ax.set_xlabel("Xgboost Feature Importance")
    plt.xlim(0, 0.7)
    fig.savefig(OutDir+region+"_Importance_.png")
    plt.clf()
    
def plot_error(cv, region, OutDir):
    import matplotlib.pyplot as plt
    colors = ["b", "darkorange"]
    results = cv.evals_result()
    # results = cv.best_estimator_.evals_result()
    epochs = len(results["validation_0"]["logloss"])
    x_axis = range(0, epochs)
    fig, ax = plt.subplots(figsize=(5,5))
    ax.plot(x_axis, results['validation_0']['logloss'], label='Train', color=colors[0], alpha=0.7)
    ax.plot(x_axis, results['validation_1']['logloss'], label='Validation', color=colors[1], alpha=0.7)
    ax.legend()
    fig.subplots_adjust(left=0.2)
    ax.set_ylabel('logloss')
    ax.set_xlabel('epochs')
    ax.set_yscale('log')
    ax.tick_params(axis = "x", direction="in", top=True, bottom = True)
    ax.tick_params(axis = "y", direction="in", left=True, right=True)
    fig.savefig(OutDir+region+"_logloss.png")

def plot_predicted_score(df, region, pred_var, OutDir):
    import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split
    colors = ["b", "darkorange"]
    colors_TMVA = ["k", "r"]
    fig, ax = plt.subplots(1, 1, figsize=(5, 4))
    
    for j, cate in enumerate(["Background", "Signal"]):
        # print(f"In {region}:")
        # print(f"{j} is {cate}")
        df_weight = df.loc[(df["isSignal"]==j)
            & (df["region"] == region)
            & (df["Dataset"]== "Validate"), "NewWt"]
        df.loc[(df["isSignal"]==j)
            & (df["region"] ==region)
            & (df["Dataset"]=="Validate"), pred_var].hist(histtype='step', 
                bins = 40,
                range=(-0.1, 1.2), 
                alpha=1,
                ax=ax, 
                density=True,
                ls='-', 
                color=colors[j],
                weights =df_weight/df_weight.sum(),
                linewidth=1,
                grid=False,
                label=cate+": validation")
        df_weight = df.loc[(df["isSignal"]==j)
            & (df["region"] == region)
            & (df["Dataset"]== "Train"), "NewWt"]
        df.loc[(df["isSignal"]==j)
            & (df["region"] ==region)
            & (df["Dataset"]=="Train"), pred_var].hist(histtype='bar', 
                bins = 40,
                range=(-0.1, 1.2), 
                alpha=0.4,
                ax=ax, 
                density=True,
                color=colors[j],
                weights =df_weight/df_weight.sum(),
                grid=False,
                label=cate+": train")
    
    # split TMVA into train/2 and test/2
    # index = df.index
    # test_indices  = index[(df["isSignal"]==0) & (df["region"] ==region) & (df["Dataset"]== "Test")].values.tolist()
    # train_indices = index[(df["isSignal"]==0) & (df["region"] ==region) & (df["Dataset"]== "Train")].values.tolist()
    # sub_test  = train_test_split(test_indices, test_size=0.5, shuffle=True)
    # sub_train = train_test_split(train_indices, test_size=0.5, shuffle=True)
    # df_weight = df.loc[sub_test[0]+sub_train[0], "NewWt"]
    # df.loc[sub_test[0]+sub_train[0], "_phoTMVA"].hist(histtype='step', 
    #         bins = 40,
    #         range=(-0.1, 1.2), 
    #         alpha= 0.9,
    #         ax=ax, 
    #         density=True,
    #         linewidth=1.3,
    #         color=colors_TMVA[0],
    #         weights =df_weight/df_weight.sum(),
    #         grid=False,
    #         label="Background: EGM UL ID")
    
    # test_indices  = index[(df["isSignal"]==1) & (df["region"] ==region) & (df["Dataset"]== "Test")].values.tolist()
    # train_indices = index[(df["isSignal"]==1) & (df["region"] ==region) & (df["Dataset"]== "Train")].values.tolist()
    # sub_test  = train_test_split(test_indices, test_size=0.5, shuffle=True)
    # sub_train = train_test_split(train_indices, test_size=0.5, shuffle=True)
    # df_weight = df.loc[sub_test[0]+sub_train[0], "xsecwt"]
    # df.loc[sub_test[0]+sub_train[0], "_phoTMVA"].hist(histtype='step', 
    #         bins = 40,
    #         range=(-0.1, 1.2), 
    #         alpha= 0.7,
    #         ax=ax, 
    #         density=True,
    #         linewidth=1.3,
    #         color=colors_TMVA[1],
    #         weights =df_weight/df_weight.sum(),
    #         grid=False,
    #         label="Signal: EGM UL ID")
            
    ax.legend(fontsize=6, ncol=2)
    ax.tick_params(axis = "x", direction="in", top=True, bottom = True)
    ax.tick_params(axis = "y", direction="in", left=True, right=True)
    ax.set_xlabel("XGB_pred")
    ax.set_ylabel("a.u.")
    ax.set_ylim(0.001, 1000)
    ax.set_yscale("log")
    fig.text(0.12, 0.9, "CMS", fontsize=14, fontweight="bold")
    fig.text(0.23, 0.9, "work-in-progress", fontsize=10)    
    if region == "barrel":
        fig.text(0.84, 0.9, "EB", fontsize=14)
    else:
        fig.text(0.84, 0.9, "EE", fontsize=14)    

    fig.savefig(OutDir+region+"_BDTval.png", dpi=800)
    plt.clf()
    
def plot_single_roc_point(df, region, XGBconf, var_score,
                          ax=None , marker='o', 
                          markersize=6, label=""):
    colors = XGBconf["OverlayWPColors"]
    df = df.copy()
    df["WP80"] = 0
    df["WP90"] = 0
    WP80Indices = df[var_score]>XGBconf["OverlayWP"][region][1]
    WP90Indices = df[var_score]>XGBconf["OverlayWP"][region][0]
    df.loc[WP80Indices, "WP80"] = 1
    df.loc[WP90Indices, "WP90"] = 1
    backgroundpass80 = df.loc[(df["WP80"] == 1) & (df["isSignal"] != 1), "NewWt"].sum()
    backgroundpass90 = df.loc[(df["WP90"] == 1) & (df["isSignal"] != 1), "NewWt"].sum()
    signalpass80     = df.loc[(df["WP80"] == 1) & (df["isSignal"] == 1), "NewWt"].sum()
    signalpass90     = df.loc[(df["WP90"] == 1) & (df["isSignal"] == 1), "NewWt"].sum()
    backgroundrej80 = df.loc[(df["WP80"] == 0) & (df["isSignal"] != 1), "NewWt"].sum()
    backgroundrej90 = df.loc[(df["WP90"] == 0) & (df["isSignal"] != 1), "NewWt"].sum()
    signalrej80     = df.loc[(df["WP80"] == 0) & (df["isSignal"] == 1), "NewWt"].sum()
    signalrej90     = df.loc[(df["WP90"] == 0) & (df["isSignal"] == 1), "NewWt"].sum()

    signaleff80     = (signalpass80*100)/(signalpass80+signalrej80)
    backgroundeff80 = (backgroundpass80*100)/(backgroundpass80+backgroundrej80)
    signaleff90     = (signalpass90*100)/(signalpass90+signalrej90)
    backgroundeff90 = (backgroundpass90*100)/(backgroundpass90+backgroundrej90)
    ax.plot([signaleff80], [backgroundeff80], marker=marker, color=colors[0], markersize=markersize, label=label+"WP80")
    ax.plot([signaleff90], [backgroundeff90], marker=marker, color=colors[1], markersize=markersize, label=label+"WP90")
    ax.legend(loc='best')
    
def plot_roc_curve(df, score_column, tpr_threshold=0, ax=None, color=None, linestyle='-', label=None,cat="Matchlabel",Wt="Wt",LeftLabel="CMS Preliminary"):
    import matplotlib.pyplot as plt
    from sklearn import metrics
    if ax is None: ax = plt.gca()
    if label is None: label = score_column
    fpr, tpr, thresholds = metrics.roc_curve(df[cat], df[score_column],sample_weight=df[Wt])
    mask = tpr > tpr_threshold
    fpr, tpr = fpr[mask], tpr[mask]
    auc=metrics.auc(fpr, tpr)
    label=label+' auc='+str(round(auc*100,1))+'%'
    ax.plot(tpr*100, (fpr)*100, label=label, color=color, linestyle=linestyle,linewidth=1.3,alpha=0.7)
    ax.legend(loc='best')
    return auc
    
def plot_final_ROC_curve(df, region, XGBconf, OutDir):
    import matplotlib.pyplot as plt
    df = df.loc[df["region"]==region,:]
    fig, axes = plt.subplots(1, 1, figsize=(6, 6))

    # for color,OverlayWpi in zip(XGBconf["OverlayWPColors"],XGBconf["OverlayWP"]):
    #     plot_single_roc_point(df.query('TrainDataset==0'), var=OverlayWpi, ax=axes, color=color, marker='o', markersize=8, label=OverlayWpi+" Test dataset", cat="isSignal",Wt="xsecwt")
    # if len(XGBconf.MVAs)>0:
        # for MVAi in XGBconf.MVAs:
    # plot_single_roc_point(df, region, XGBconf, "_phoTMVA", axes, label="TMVA: ")
    
    # plot_roc_curve(df.query('TrainDataset==2'),"_phoTMVA", tpr_threshold=0.0, ax=axes, color="p", linestyle='--', label='EGM UL: Validate', cat="isSignal", Wt='NewWt')
    plot_roc_curve(df.query('TrainDataset==2'),"XGB_pred", tpr_threshold=0.0, ax=axes, color="b", linestyle='--', label='XGBoost: Validate',cat="isSignal",Wt='NewWt')
    plot_roc_curve(df.query('TrainDataset==1'),"XGB_pred", tpr_threshold=0.0, ax=axes, color="b", linestyle='-', label='XGBoost: Train',cat="isSignal",Wt='NewWt')
    axes.set_xlabel("Signal efficiency  (%)")
    axes.set_ylabel("Background efficiency (%)")

    axes.set_yscale("log")
    axes.legend(loc='best',ncol=1,fontsize=10)
    axes.tick_params(axis = "x", direction="in", top=True, bottom = True)
    axes.tick_params(axis = "y", direction="in", left=True, right=True)
    fig.text(0.12, 0.9, "CMS", fontsize=16, fontweight="bold")
    fig.text(0.22, 0.9, "work-in-progress", fontsize=12)    

    fig.savefig(OutDir+region+"_ROCFinal.png")
    plt.clf()
    
def plot_best_params(best_params, OutDir):
    
    import matplotlib.pyplot as plt

    # plt.rcParams["font.family"]=["Time New Roman"] 
    columns=["parameters", "value"]
    rows = range(len(best_params.keys()))
    data = []
    for key in best_params.keys():
        if type(best_params[key][0]) is str:
            data.append( [key, best_params[key][0]])
        elif type(best_params[key][0]) is  int:
            data.append( [key, best_params[key][0]])
        elif type(best_params[key][0]) is  float:
            data.append( [key, "{:.3f}".format(best_params[key][0])]  )
        else:
            continue
         
    plt.axis('off')   
    plt.table(cellText=data, colLabels=columns, loc="center",
            rowLabels=rows, edges='vertical')
    plt.savefig(OutDir+"best_params.png")
    plt.clf()