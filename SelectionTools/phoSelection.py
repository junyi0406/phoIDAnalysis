'''
This module is for the photon ID trainning, which prepares the matching function and preselction for any reco photon.
The function include:
    select_PromtPho_Signal:
        - for the HToZG samples
        - pick up the ISR photon
    select_PromtPho_Signal_Back:
        - for the ZToLLG, DYJets samples
        - pick up the ISR photon
    photon_Matching (private):
        - for the HToZG, ZToLLG, DYJets samples
        - do the reco-pho matching to generator level
    preselection_HZg:
    preselection_Hgg:
    
'''
import dask

@dask.delayed
def deltaR(eta1, eta2, phi1, phi2):
    import numpy as np
    deta = eta2-eta1
    dphi = phi2-phi1
    return np.sqrt( deta*deta+dphi*dphi)

@dask.delayed
def select_PromtPho_Signal(row):
    nPho         = row["nPho"]
    mcPID        = row["mcPID"]
    mcMomPID     = row["mcMomPID"]
    mcStatusFlag = row["mcStatusFlag"]
    idx_par = photon_Matching(row) # i_th particle match to photon
    if idx_par != -999:
        isPho    = mcPID[idx_par]    == 22
        isMHiggs = mcMomPID[idx_par] == 25
        isPromptFinalState = mcStatusFlag[idx_par] >> 0 & 1 == 1
        fromHardProcessFinalState = mcStatusFlag[idx_par] >> 1 & 1 == 1
        if isPho and isMHiggs and isPromptFinalState and fromHardProcessFinalState:
            retval = 1
        else:
            retval = 0
    return retval

@dask.delayed
def select_PromtPho_Back(row):
    mcPID        = row["mcPID"]
    mcStatusFlag = row["mcStatusFlag"]
    idx_par = photon_Matching(row)
    if idx_par != -999:
        isPho    = mcPID[idx_par]    == 22
        isPromptFinalState = mcStatusFlag[idx_par] >> 0 & 1 == 1
        fromHardProcessFinalState = mcStatusFlag[idx_par] >> 1 & 1 == 1
        if isPho and isPromptFinalState and fromHardProcessFinalState:
            retval = 1
        else:
            retval = 0
    else:
        retval = 0
    return retval



@dask.delayed
def photon_Matching(row):
    # return the index of matched gen particle
    nMC    = row["nMC"]
    mcPt   = row["mcPt"]
    mcEta  = row["mcEta"]
    mcPhi  = row["mcPhi"]
    phoEt  = row["phoCalibEt"]
    phoEta = row["phoEta"]
    phoPhi = row["phoPhi"]
    for j in range(nMC):
        dr = deltaR(phoEta, mcEta[j], phoPhi, mcPhi[j])
        pt_ratio = (phoEt - mcPt[j])/mcPt[j]
        if dr < 0.1 and pt_ratio < 0.2:
            retval = j
            break
        else:
            retval = -999
    return retval        
    