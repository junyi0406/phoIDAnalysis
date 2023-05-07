

def df_pteta_rwt(Mdf,
                 label,
                 returnOnlyPosWeights=0, 
                 ptw = [10,30,40,50,200,10000], 
                 etaw = [-1.5,-1.0,1.0,1.5], 
                 eta='', 
                 pt='',
                 SumWeightCol="wt",
                 NewWeightCol="NewWt",target=1,cand=0):
    #Mdf=Ndf.copy()
    ptwt = [1.0]*len(ptw)
    etawt = [1.0]*len(etaw)
    
    for k in range(len(etaw)):
        if k == len(etaw)-1:
            continue
        for i in range(len(ptw)):
            if i == len(ptw)-1:
                continue

            targetSum = Mdf.loc[(Mdf[pt] <ptw[i+1]) & (Mdf[pt] >ptw[i]) & (Mdf[eta] <etaw[k+1]) & (Mdf[eta] >etaw[k]) &(Mdf[label]==target),SumWeightCol].sum()
            candSum = Mdf.loc[(Mdf[pt] <ptw[i+1]) & (Mdf[pt] >ptw[i]) & (Mdf[eta] <etaw[k+1]) & (Mdf[eta] >etaw[k]) &(Mdf[label]==cand),SumWeightCol].sum()

            #print('Number of xsec events in signal for pt '+str(ptw[i])+' to '+str(ptw[i+1])+ 'before  weighing = '+str(targetSum))
            #print('Number of xsec events in background for pt '+str(ptw[i])+' to '+str(ptw[i+1])+ 'before  weighing = '+str(candSum))

            if candSum>0 and targetSum>0:
                ptwt[i]=candSum/(targetSum)
            else:
                ptwt[i]=0
            Mdf.loc[(Mdf[pt] <ptw[i+1]) & (Mdf[pt] >ptw[i]) 
                    & (Mdf[eta] <etaw[k+1]) & (Mdf[eta] >etaw[k]) 
                    &(Mdf[label]==cand),"rwt"] = 1.0
            Mdf.loc[(Mdf[pt] <ptw[i+1]) & (Mdf[pt] >ptw[i]) 
                    & (Mdf[eta] <etaw[k+1]) & (Mdf[eta] >etaw[k]) 
                    &(Mdf[label]==target),"rwt"] = ptwt[i]

            Mdf.loc[:,NewWeightCol] = Mdf.loc[:,"rwt"]*Mdf.loc[:,SumWeightCol]

    MtargetSum = Mdf.loc[Mdf[label]==target,NewWeightCol].sum()
    McandSum = Mdf.loc[Mdf[label]==cand,NewWeightCol].sum()
    print('Number of events in signal after  weighing = '+str(MtargetSum))
    print('Number of events in background after  weighing = '+str(McandSum))

    if returnOnlyPosWeights==0: return 0
    else:
        return ptwt
    

def check_reweight_plot(df, conf, rewt_plot_dir):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    
    for i,group_df in df[df['Dataset'] == "Train"].groupby("_phoIsPrompt"):
        group_df[conf["ptwtvar"]].hist(histtype='step', bins=conf["ptbins"], alpha=0.7,label=i, ax=ax[0], density=False, ls='-', weights =group_df["xsecwt"],linewidth=2)
        ax[0].set_title("$p_T$ before reweighting")
        ax[0].legend()
        ax[0].set_xscale('log')
        group_df[conf["ptwtvar"]].hist(histtype='step', bins=conf["ptbins"], alpha=0.7,label=i, ax=ax[1], density=False, ls='-', weights =group_df["NewWt"],linewidth=2)
        ax[1].set_title("$p_T$ after reweighting")
        ax[1].legend()
        ax[1].set_xscale('log')
    fig.savefig(rewt_plot_dir+"/pT_rwt.png")

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    for i,group_df in df[df['Dataset'] == "Train"].groupby("_phoIsPrompt"):
        group_df[conf["etawtvar"]].hist(histtype='step',
                                     bins=conf["etabins"],
                                     #[i for i in range(len(conf[""].etabins)-1)],
                                     alpha=0.7,label=i, ax=ax[0], density=False, ls='-', weights =group_df["xsecwt"],linewidth=2)
        ax[0].set_title("$\eta$ before reweighting")
        ax[0].legend()
        group_df[conf["etawtvar"]].hist(histtype='step',
                                     bins=conf["etabins"],
                                     alpha=0.7,label=i, ax=ax[1], density=False, ls='-', weights =group_df["NewWt"],linewidth=2)
        ax[1].set_title("$\eta$ after reweighting")
        ax[1].legend()
    fig.savefig(rewt_plot_dir+"/eta_rwt.png")