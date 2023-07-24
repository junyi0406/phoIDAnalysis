

def df_pteta_rwt(df, sigvar, backvar,
                ptbins, etabins_barrel, etabins_endcap,
                ptvar = "_phoCalibEt", etavar = "_phoSCEta",
                SumWeightCol = "xsecwt", NewWeightCol="NewWt",
                ):
    import numpy as np    
    # barrel 
    sig_XSwet = df.loc[(df["region"] == "barrel") & (df["Category"] == sigvar), SumWeightCol].to_numpy() 
    sig_pt  = df.loc[(df["region"] == "barrel") & (df["Category"] == sigvar), ptvar].to_numpy() 
    sigl_eta = df.loc[(df["region"] == "barrel") & (df["Category"] == sigvar), etavar].to_numpy()
    back_XSwet = df.loc[(df["region"] == "barrel") & (df["Category"] == backvar), SumWeightCol].to_numpy() 
    back_pt  = df.loc[(df["region"] == "barrel") & (df["Category"] == backvar), ptvar].to_numpy()
    back_eta = df.loc[(df["region"] == "barrel") & (df["Category"] == backvar), etavar].to_numpy()
    sig_wei, xedge, yedge = np.histogram2d(sig_pt, sigl_eta, bins=[ptbins,etabins_barrel], density=False, weights=sig_XSwet)
    back_wei, xedge, yedge = np.histogram2d(back_pt, back_eta, bins=[ptbins,etabins_barrel], density=False, weights=back_XSwet)
    # do normalization
    # sig_wei  =  sig_wei / len(sig_pt)
    # back_wei = back_wei / len(back_pt)
    weight   = back_wei / sig_wei
    # print(weight)
    for i in range(len(ptbins)-1):
        for j in range(len(etabins_barrel)-1):
            df.loc[ (df["Category"] == sigvar)
                    & (df["region"]=="barrel") 
                    & (df[ptvar]<ptbins[i+1]) 
                    & (df[ptvar]>ptbins[i])
                    & (df[etavar]<etabins_barrel[j+1])
                    & (df[etavar]>etabins_barrel[j]), NewWeightCol] = weight[i, j] * df.loc[ (df["Category"] == sigvar)
                                                                                            & (df["region"]=="barrel") 
                                                                                            & (df[ptvar]<ptbins[i+1]) 
                                                                                            & (df[ptvar]>ptbins[i])
                                                                                            & (df[etavar]<etabins_barrel[j+1])
                                                                                            & (df[etavar]>etabins_barrel[j]), SumWeightCol]
            df.loc[ (df["Category"] == backvar)
                    & (df["region"]=="barrel") 
                    & (df[ptvar]<ptbins[i+1]) 
                    & (df[ptvar]>ptbins[i])
                    & (df[etavar]<etabins_barrel[j+1])
                    & (df[etavar]>etabins_barrel[j]), NewWeightCol] = df.loc[ (df["Category"] == backvar)
                                                                            & (df["region"]=="barrel") 
                                                                            & (df[ptvar]<ptbins[i+1]) 
                                                                            & (df[ptvar]>ptbins[i])
                                                                            & (df[etavar]<etabins_barrel[j+1])
                                                                            & (df[etavar]>etabins_barrel[j]), SumWeightCol]
    for justclass in [sigvar, backvar]:
        Sum = df.loc[(df["Category"]==justclass) & (df["region"] == "barrel"), NewWeightCol].sum()
        print(f'Number of events in {justclass} and barrel after  weighing = '+str(Sum))
    
    # endcap
    sig_XSwet = df.loc[(df["region"] == "endcap") & (df["Category"] == sigvar), SumWeightCol].to_numpy()
    back_XSwet  = df.loc[(df["region"] == "endcap") & (df["Category"] == backvar), SumWeightCol].to_numpy()
    sig_pt  = df.loc[(df["region"] == "endcap") & (df["Category"] == sigvar), ptvar].to_numpy()
    sigl_eta = df.loc[(df["region"] == "endcap") & (df["Category"] == sigvar), etavar].to_numpy()
    back_pt  = df.loc[(df["region"] == "endcap") & (df["Category"] == backvar), ptvar].to_numpy()
    back_eta = df.loc[(df["region"] == "endcap") & (df["Category"] == backvar), etavar].to_numpy()
    sig_wei, xedge, yedge = np.histogram2d(sig_pt, sigl_eta, bins=[ptbins,etabins_endcap], density=False, weights=sig_XSwet)
    back_wei, xedge, yedge = np.histogram2d(back_pt, back_eta, bins=[ptbins,etabins_endcap], density=False, weights=back_XSwet)
    # remove barrel val
    sig_wei = np.delete(sig_wei, int((len(yedge)-1)/2), axis=1)
    back_wei = np.delete(back_wei, int((len(yedge)-1)/2), axis=1)
    # sig_wei  =  sig_wei / len(sig_pt)
    # back_wei = back_wei / len(back_pt)
    weight = back_wei / sig_wei
    weight = np.insert(weight, int((len(yedge)-1)/2), 0, axis=1)
    # print(weight)
    # weight[np.isnan(weight)] = 0
    for i in range(len(ptbins)-1):
        for j in range(len(etabins_endcap)-1):
            df.loc[ (df["Category"] == sigvar)
                        & (df["region"]=="endcap") 
                        & (df[ptvar]<ptbins[i+1]) 
                        & (df[ptvar]>ptbins[i])
                        & (df[etavar]<etabins_endcap[j+1])
                        & (df[etavar]>etabins_endcap[j]), NewWeightCol] = weight[i, j] * df.loc[ (df["Category"] == sigvar)
                                                                                                & (df["region"]=="endcap") 
                                                                                                & (df[ptvar]<ptbins[i+1]) 
                                                                                                & (df[ptvar]>ptbins[i])
                                                                                                & (df[etavar]<etabins_endcap[j+1])
                                                                                                & (df[etavar]>etabins_endcap[j]), SumWeightCol]
            df.loc[( df["Category"] == backvar)
                        & (df["region"]=="endcap") 
                        & (df[ptvar]<ptbins[i+1]) 
                        & (df[ptvar]>ptbins[i])
                        & (df[etavar]<etabins_endcap[j+1])
                        & (df[etavar]>etabins_endcap[j]), NewWeightCol] = df.loc[( df["Category"] == backvar)
                                                                                & (df["region"]=="endcap") 
                                                                                & (df[ptvar]<ptbins[i+1]) 
                                                                                & (df[ptvar]>ptbins[i])
                                                                                & (df[etavar]<etabins_endcap[j+1])
                                                                                & (df[etavar]>etabins_endcap[j]), SumWeightCol]
 
    for justclass in [sigvar, backvar]:
        Sum = df.loc[(df["Category"]==justclass) & (df["region"] == "endcap"), NewWeightCol].sum()
        print(f'Number of events in {justclass} and endcap after  weighing = '+str(Sum))
    return df[NewWeightCol]






def check_reweight_plot(df, conf, rewt_plot_dir, region="barrel"):
    
    df = df[df["region"]==region]
    import matplotlib.pyplot as plt 
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    for i,group_df in df.groupby("Category"):
      
        group_df[conf["ptwtvar"]].hist(histtype='step',
                                       bins=conf["ptbins"], alpha=0.7,
                                       label=i, ax=ax[0], density=True,
                                       ls='-', weights =group_df["xsecwt"],linewidth=2)
        ax[0].set_title("$p_T$ before reweighting")
        ax[0].legend()

        group_df[conf["ptwtvar"]].hist(histtype='step',
                                       bins=conf["ptbins"], alpha=0.7,
                                       label=i, ax=ax[1], density=True, 
                                       ls='-', weights =group_df["NewWt"],linewidth=2)
        ax[1].set_title("$p_T$ after reweighting")
        ax[1].legend()

    fig.savefig(rewt_plot_dir+"pT_rwt_"+region+".png")
    plt.clf()
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    for i,group_df in df.groupby("Category"):
        group_df[conf["etawtvar"]].hist(histtype='step',
                                        bins=conf["etabins_"+region],
                                        alpha=0.7,label=i, ax=ax[0], density=True,
                                        ls='-', weights =group_df["xsecwt"],linewidth=2)
    
        ax[0].set_title("$\eta$ before reweighting")
        ax[0].legend()
        group_df[conf["etawtvar"]].hist(histtype='step',
                                        bins=conf["etabins_"+region],
                                        alpha=0.7,label=i, ax=ax[1], density=True, 
                                        ls='-', weights =group_df["NewWt"],linewidth=2)
       
        ax[1].set_title("$\eta$ after reweighting")
        ax[1].legend()
    fig.savefig(rewt_plot_dir+"eta_rwt_"+region+".png")
    plt.clf()