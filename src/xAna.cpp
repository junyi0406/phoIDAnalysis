#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#include <TError.h>
#include <TFile.h>
#include <TString.h>
#include <TSystem.h>

#include <iostream>
#include <string>
#include <TTree.h>
#include <TLorentzVector.h>
#include <vector>

#include "../include/xAna.hpp"



phoID::dataReader::dataReader(std::string dir_path){
    std::vector<std::string> fileList = find_files(dir_path.c_str());
    data = new TreeReader(fileList);
}

void phoID::dataReader::LoopTree(bool isSignal){
    
    std::cout<<"start to build the tree!"<<std::endl;
    long int tev = data->GetEntriesFast();

    std::cout<<"There is "<< tev << " entries."<<std::endl;
    for(long int ev=0; ev<tev; ev++){
        if (ev % (tev/1000) == 0) 
            print_progress(ev, tev);
        if (!data->HasMC()){
            FATAL("error");
        }
        // std::cout<<"ok!"<<std::endl;
        exchange(ev, data);
        // std::cout<<"ok!"<<std::endl;
        _phoIsPromt.clear();
        if (isSignal)
            _phoIsPromt = select_PromtPho_Signal();
        else 
            _phoIsPromt = select_PromtPho_Back();
        // std::cout<<"ok!"<<std::endl;
        if( _phoIsPromt.size() != (unsigned int) 0)
            out_tree->Fill();
    }
    std::cout<<std::endl;
}
void phoID::dataReader::exchange(long int ev, TreeReader* reader){
    reader->GetEntry(ev);
    int run                     = data->GetInt("run");
    int nVtx                    = data->GetInt("nVtx");
    // float* puTrue               = data->GetPtrFloat("puTrue");
    int rho                     = data->GetFloat("rho");
    long long int event         = (long long int) data->GetLong64("event");
    _run   = run;
    _nVtx  = nVtx;
    _rho   = rho;
    _event = event;
    int nLHE                    = data->GetInt("nLHE");
    float* lhePx                   = data->GetPtrFloat("lhePx");
    float* lhePy                   = data->GetPtrFloat("lhePy");
    float* lhePz                   = data->GetPtrFloat("lhePz");
    float* lheE                    = data->GetPtrFloat("lheE");
    int* lhePID                    = data->GetPtrInt("lhePID");
    _nLHE = nLHE;
    convertFlt(nLHE, lhePx, _lhePx);
    convertFlt(nLHE, lhePy, _lhePy);
    convertFlt(nLHE, lhePz, _lhePz);
    convertFlt(nLHE,  lheE, _lheE);
    convertInt(nLHE,  lhePID, _lhePID);
    int nMC                     = data->GetInt("nMC");
    float* mcPt                    = data->GetPtrFloat("mcPt");
    float* mcE                     = data->GetPtrFloat("mcE");
    float* mcEta                   = data->GetPtrFloat("mcEta");
    float* mcPhi                   = data->GetPtrFloat("mcPhi");
    int* mcPID                     = data->GetPtrInt("mcPID");
    int* mcMomPID                  = data->GetPtrInt("mcMomPID");
    int* mcGMomPID                 = data->GetPtrInt("mcGMomPID");
    short int* mcStatusFlag        = (short int*) data->GetPtrShort("mcStatusFlag");
    _nMC = nMC;
    convertFlt(nMC, mcPt, _mcPt);
    convertFlt(nMC, mcE, _mcE);
    convertFlt(nMC, mcEta, _mcEta);
    convertFlt(nMC,  mcPhi, _mcPhi);
    convertInt(nMC,  mcPID, _mcPID);
    convertInt(nMC,  mcMomPID, _mcMomPID);
    convertInt(nMC,  mcGMomPID, _mcGMomPID);
    convertSInt(nMC, mcStatusFlag, _mcStatusFlag);
    int nPho                    = data->GetInt("nPho");
    float* phoEta                  = data->GetPtrFloat("phoEta");
    float* phoPhi                  = data->GetPtrFloat("phoPhi");
    float* phoEt                   = data->GetPtrFloat("phoCalibEt");
    float* phoSCRawE               = data->GetPtrFloat("phoSCRawE");
    float* phoESEnP1               = data->GetPtrFloat("phoESEnP1");
    float* phoESEnP2               = data->GetPtrFloat("phoESEnP2");
    float* phoSCEta                = data->GetPtrFloat("phoSCEta");
    float* phoSCEtaWidth           = data->GetPtrFloat("phoSCEtaWidth");
    float* phoSCPhiWidth           = data->GetPtrFloat("phoSCPhiWidth");
    int* phoEleVeto                = data->GetPtrInt("phoEleVeto");           
    float* phoR9                   = data->GetPtrFloat("phoR9");
    float* phoHoverE               = data->GetPtrFloat("phoHoverE");
    float* phoESEffSigmaRR         = data->GetPtrFloat("phoESEffSigmaRR");
    float* phoSigmaIEtaIEtaFull5x5 = data->GetPtrFloat("phoSigmaIEtaIEtaFull5x5");
    float* phoSigmaIEtaIPhiFull5x5 = data->GetPtrFloat("phoSigmaIEtaIPhiFull5x5");
    float* phoE2x2Full5x5          = data->GetPtrFloat("phoE2x2Full5x5");
    float* phoE5x5Full5x5          = data->GetPtrFloat("phoE5x5Full5x5");
    float* phoR9Full5x5            = data->GetPtrFloat("phoR9Full5x5");
    float* phoPFChIso              = data->GetPtrFloat("phoPFChIso");
    float* phoPFPhoIso             = data->GetPtrFloat("phoPFPhoIso");
    float* phoPFChWorstIso         = data->GetPtrFloat("phoPFChWorstIso");
    float* phoIDMVA                = data->GetPtrFloat("phoIDMVA");
    float* phoEcalPFClusterIso     = data->GetPtrFloat("phoEcalPFClusterIso");
    float* phoHcalPFClusterIso     = data->GetPtrFloat("phoHcalPFClusterIso");
    float* phoConeHoverE           = data->GetPtrFloat("phoConeHoverE");
    float* phoCalibEt              = data->GetPtrFloat("phoCalibEt");
    _nPho = nPho;
    convertFlt(nPho, phoEta, _phoEta);
    convertFlt(nPho, phoPhi, _phoPhi);
    convertFlt(nPho, phoEt, _phoEt);
    convertFlt(nPho, phoSCRawE, _phoSCRawE);
    convertFlt(nPho, phoESEnP1, _phoESEnP1);
    convertFlt(nPho, phoESEnP2, _phoESEnP2);
    convertFlt(nPho, phoSCEta, _phoSCEta);
    convertFlt(nPho, phoSCEtaWidth, _phoSCEtaWidth);
    convertFlt(nPho, phoSCPhiWidth, _phoSCPhiWidth);
    convertInt(nPho, phoEleVeto, _phoEleVeto);
    convertFlt(nPho, phoR9, _phoR9);
    convertFlt(nPho, phoHoverE, _phoHoverE);
    convertFlt(nPho, phoESEffSigmaRR, _phoESEffSigmaRR);
    convertFlt(nPho, phoSigmaIEtaIEtaFull5x5, _phoSigmaIEtaIEtaFull5x5);
    convertFlt(nPho, phoSigmaIEtaIPhiFull5x5, _phoSigmaIEtaIPhiFull5x5);
    convertFlt(nPho, phoE2x2Full5x5, _phoE2x2Full5x5);
    convertFlt(nPho, phoE5x5Full5x5, _phoE5x5Full5x5);
    convertFlt(nPho, phoR9Full5x5, _phoR9Full5x5);
    convertFlt(nPho, phoPFChIso, _phoPFChIso);
    convertFlt(nPho, phoPFPhoIso, _phoPFPhoIso);
    convertFlt(nPho, phoPFChWorstIso, _phoPFChWorstIso);
    convertFlt(nPho, phoIDMVA, _phoIDMVA);
    convertFlt(nPho, phoEcalPFClusterIso, _phoEcalPFClusterIso);
    convertFlt(nPho, phoHcalPFClusterIso, _phoHcalPFClusterIso);
    convertFlt(nPho, phoConeHoverE, _phoConeHoverE);
    convertFlt(nPho, phoCalibEt, _phoCalibEt);
    int nEle                    = data->GetInt("nEle");
    int* eleCharge                 = data->GetPtrInt("eleCharge");
    float* eleCalibPt              = data->GetPtrFloat("eleCalibPt");
    float* eleEta                  = data->GetPtrFloat("eleEta");
    float* elePhi                  = data->GetPtrFloat("elePhi");
    _nEle = nEle;
    convertInt(nEle, eleCharge, _eleCharge);
    convertFlt(nEle, eleCalibPt, _eleCalibPt);
    convertFlt(nEle, eleEta, _eleEta);
    convertFlt(nEle, elePhi, _elePhi);
    int nMu                     = data->GetInt("nMu");
    float* muPt                    = data->GetPtrFloat("muPt");
    float* muEta                   = data->GetPtrFloat("muEta");
    float* muPhi                   = data->GetPtrFloat("muPhi");
    int* muCharge                  = data->GetPtrInt("muCharge");       //for roch corr
    int* muType                    = data->GetPtrInt("muType");         //for roch corr
    int* muTrkLayers               = data->GetPtrInt("muTrkLayers");    //for roch corr
    _nMu = nMu;
    convertInt(nMu, muCharge, _muCharge);
    convertInt(nMu, muType, _muType);
    convertInt(nMu, muTrkLayers, _muTrkLayers);
    convertFlt(nMu, muPt, _muPt);
    convertFlt(nMu, muEta, _muEta);
    convertFlt(nMu, muPhi, _muPhi);

}

void phoID::dataReader::InitTree(std::string treename){
    out_tree = new TTree(treename.c_str(), treename.c_str());
    out_tree->Branch("_run"                    , &_run                    );
    out_tree->Branch("_nVtx"                   , &_nVtx                   );
    // out_tree->Branch("_puTrue"                 , &_puTrue                 );
    out_tree->Branch("_rho"                    , &_rho                    );
    out_tree->Branch("_event"                  , &_event                  );

    out_tree->Branch("_nLHE"                   , &_nLHE                   );
    out_tree->Branch("_lhePx"                  , &_lhePx                  );
    out_tree->Branch("_lhePy"                  , &_lhePy                  );
    out_tree->Branch("_lhePz"                  , &_lhePz                  );
    out_tree->Branch("_lheE"                   , &_lheE                   );
    out_tree->Branch("_lhePID"                 , &_lhePID                 );

    out_tree->Branch("_nMC"                    , &_nMC                    );
    out_tree->Branch("_mcPt"                   , &_mcPt                   );
    out_tree->Branch("_mcE"                    , &_mcE                    );
    out_tree->Branch("_mcEta"                  , &_mcEta                  );
    out_tree->Branch("_mcPhi"                  , &_mcPhi                  );
    out_tree->Branch("_mcPID"                  , &_mcPID                  );
    out_tree->Branch("_mcMomPID"               , &_mcMomPID               );
    out_tree->Branch("_mcGMomPID"              , &_mcGMomPID              );
    out_tree->Branch("_mcStatusFlag"           , &_mcStatusFlag           );

    out_tree->Branch("_nPho"                   , &_nPho                   );
    out_tree->Branch("_phoEta"                 , &_phoEta                 );
    out_tree->Branch("_phoPhi"                 , &_phoPhi                 );
    out_tree->Branch("_phoEt"                  , &_phoEt                  );
    out_tree->Branch("_phoSCRawE"              , &_phoSCRawE              );
    out_tree->Branch("_phoESEnP1"              , &_phoESEnP1              );
    out_tree->Branch("_phoESEnP2"              , &_phoESEnP2              );
    out_tree->Branch("_phoSCEta"               , &_phoSCEta               );
    out_tree->Branch("_phoSCEtaWidth"          , &_phoSCEtaWidth          );
    out_tree->Branch("_phoSCPhiWidth"          , &_phoSCPhiWidth          );
    out_tree->Branch("_phoEleVeto"             , &_phoEleVeto             );
    out_tree->Branch("_phoR9"                  , &_phoR9                  );
    out_tree->Branch("_phoHoverE"              , &_phoHoverE              );
    out_tree->Branch("_phoESEffSigmaRR"        , &_phoESEffSigmaRR        );
    out_tree->Branch("_phoSigmaIEtaIEtaFull5x5", &_phoSigmaIEtaIEtaFull5x5);
    out_tree->Branch("_phoSigmaIEtaIPhiFull5x5", &_phoSigmaIEtaIPhiFull5x5);
    out_tree->Branch("_phoE2x2Full5x5"         , &_phoE2x2Full5x5         );
    out_tree->Branch("_phoE5x5Full5x5"         , &_phoE5x5Full5x5         );
    out_tree->Branch("_phoR9Full5x5"           , &_phoR9Full5x5           );
    out_tree->Branch("_phoPFChIso"             , &_phoPFChIso             );
    out_tree->Branch("_phoPFPhoIso"            , &_phoPFPhoIso            );
    out_tree->Branch("_phoPFChWorstIso"        , &_phoPFChWorstIso        );
    out_tree->Branch("_phoIDMVA"               , &_phoIDMVA               );
    out_tree->Branch("_phoEcalPFClusterIso"    , &_phoEcalPFClusterIso    );
    out_tree->Branch("_phoHcalPFClusterIso"    , &_phoHcalPFClusterIso    );
    out_tree->Branch("_phoConeHoverE"          , &_phoConeHoverE          );
    out_tree->Branch("_phoCalibEt"             , &_phoCalibEt          );

    out_tree->Branch("_nEle"                   , &_nEle                   );
    out_tree->Branch("_eleCharge"              , &_eleCharge              );
    out_tree->Branch("_eleCalibPt"             , &_eleCalibPt             );
    out_tree->Branch("_eleEta"                 , &_eleEta                 );
    out_tree->Branch("_elePhi"                 , &_elePhi                 );

    out_tree->Branch("_nMu"                    , &_nMu                    );
    out_tree->Branch("_muPt"                   , &_muPt                   );
    out_tree->Branch("_muEta"                  , &_muEta                  );
    out_tree->Branch("_muPhi"                  , &_muPhi                  );
    out_tree->Branch("_muCharge"               , &_muCharge               );
    out_tree->Branch("_muType"                 , &_muType                 );
    out_tree->Branch("_muTrkLayers"            , &_muTrkLayers            );

    out_tree->Branch("_phoIsPrompt"            , &_phoIsPromt);
}

void phoID::dataReader::save_minitree(std::string out_path){
    TFile *fo = TFile::Open(out_path.c_str(), "RECREATE");
    if (!fo || fo->IsZombie())  FATAL("TFile::Open() failed");
    fo->cd();
    out_tree->Write();
    fo->Close();
}

void phoID::dataReader::print_progress(const long int& progress, const long int& total){
    std::cout << "[";
    float percent = (progress + 1) * 100./ total;
    float unit_length = 100. / barWidth;
    for(int ibar = 0; ibar < barWidth; ++ibar){
        if(ibar * unit_length < percent)
            std::cout << "#";
        else
            std::cout << " ";
    }
    std::cout << "]"
                << std::setw(3) << std::ceil(percent) << "% \r"
                << std::flush;
}

std::vector<std::string> phoID::dataReader::find_files(const char* patt){
    /* Returns sorted list of paths to root files matching the path pattern given.
        *
        * Documentation is given in the out_treeReader(const char*, const char*)
        * constructor.
        */

    // to hide useless printouts and restore the log level afterwards
    int lvl = gErrorIgnoreLevel;

    std::vector<std::string> paths;

    TString p(patt);

    if (p.EndsWith(".root")) {
        // check whether target path already exists
        FileStat_t st;
        gErrorIgnoreLevel = kBreak;
        if (!gSystem->GetPathInfo(patt, st)) {
            gErrorIgnoreLevel = lvl;
            paths.push_back(patt);
            return paths;
        }
        gErrorIgnoreLevel = lvl;
    } else
        // append the file search pattern
        p += (p.EndsWith("/") ? "*.root" : "/*.root");

    // find existing base directory
    TString base = p;
    do {
        Ssiz_t i = TString(base(0, base.Length() - 1)).Last('/');

        if (i == kNPOS) 
        FATAL("no input files found");      

        base = TString(base(0, i + 1));  // keep all "/" at the end

        void* dir = gSystem->OpenDirectory(base);
        if (!dir)
            FATAL("code bug: gSystem->OpenDirectory() returned NULL");

        gErrorIgnoreLevel = kBreak;
        if (gSystem->GetDirEntry(dir)) {
            gErrorIgnoreLevel = lvl;
            gSystem->FreeDirectory(dir);
            break;
        }
        gErrorIgnoreLevel = lvl;

        gSystem->FreeDirectory(dir);
    } while (base.Length() > 0);

    if (base.Length() < 1) 
        FATAL("no input files found");

    // get rid of all "//" in p beyond the base directory
    TString trail = p(base.Length(), p.Length());
    Ssiz_t siz = trail.Length();
    while (trail.ReplaceAll("//", "/").Length() != siz)
        siz = trail.Length();

    // NOTE: trail never starts with "/"
    p = base + trail;

    std::vector<std::string> dirs;
    dirs.push_back(base.Data());

    // walk though matching subdirectories, search for matching files
    while (dirs.size() > 0) {
        TString dirpath = dirs.back();
        dirs.pop_back();

        void* dir = gSystem->OpenDirectory(dirpath);
        if (!dir)
            FATAL("code bug: gSystem->OpenDirectory() returned NULL");

        // const char* fname;

        gErrorIgnoreLevel = kBreak;
        while (const char* fname = gSystem->GetDirEntry(dir)) {
            gErrorIgnoreLevel = lvl;

            TString path = dirpath + fname;
            if (TString(fname) == "." || TString(fname) == "..") continue;

            FileStat_t st;
            if (gSystem->GetPathInfo(path, st))
                FATAL(("gSystem->GetPathInfo() failed: " + path).Data());

            if (R_ISDIR(st.fMode)) {
                // search for a match
                Ssiz_t i = p.Last('/');
                while (i != kNPOS) {
                if (fnmatch(TString(p(0, i)), path, FNM_PATHNAME) == 0) {
                    dirs.push_back((path + "/").Data());
                    break;
                }
                i = TString(p(0, i)).Last('/');
                }

            } else if (TString(fname).EndsWith(".root")) {
        if (fnmatch(p, path, FNM_PATHNAME) == 0) {
            //Printf("out_treeReader: adding %s", path.Data());
            paths.push_back(path.Data());
        }
            }

            gErrorIgnoreLevel = kBreak;
        }
        gErrorIgnoreLevel = lvl;

        gSystem->FreeDirectory(dir);
    }

    if (paths.size() < 1) {
        FATAL("no input files found");
    }

    // sort to return well-defined order
    std::sort(paths.begin(), paths.end());

    //    Printf("find_files(): %lu file%s found", paths.size(),
    //                                             paths.size() == 1 ? "" : "s");

    return paths;
}


std::vector<int> phoID::dataReader::select_PromtPho_Back(){
    std::vector<int> idx_mat = doMatching_pho();
    std::vector<int> retval;
    for(int i=0; i<_nPho; i++){
        int idx = idx_mat[i];
        if (idx == -999){
            retval.push_back(0);
            continue;
        }
        if (_mcPID[idx] != 22){
            retval.push_back(0);
            continue;
        }
        if (((_mcStatusFlag[idx] >> 0) & 1) == 0){
            retval.push_back(0);
            continue;
        }
        if (((_mcStatusFlag[idx] >> 1) & 1) == 0){
            retval.push_back(0);
            continue;
        }
        retval.push_back(1);
    }
    return retval;
}
std::vector<int> phoID::dataReader::select_PromtPho_Signal(){

    std::vector<int> idx_mat = doMatching_pho();
    std::vector<int> retval;
    for(int i=0; i<_nPho; i++){
        int idx = idx_mat[i];
        if (idx == -999){
            retval.push_back(0);
            continue;
        }
        if (_mcPID[idx] != 22){
            retval.push_back(0);
            continue;
        }
        if (_mcMomPID[idx] != 25){
            retval.push_back(0);
            continue;
        }
        if (((_mcStatusFlag[idx] >> 0) & 1) == 0){
            retval.push_back(0);
            continue;
        }
        if (((_mcStatusFlag[idx] >> 1) & 1) == 0){
            retval.push_back(0);
            continue;
        }
        retval.push_back(1);
    }
    return retval;
}

std::vector<int> phoID::dataReader::doMatching_pho(){
    std::vector<int> retval;
    TVector3 genPar, recoPar;
    for (int i = 0; i<_nPho; i++) {  
        recoPar.SetPtEtaPhi(_phoEt[i], _phoEta[i], _phoPhi[i]);
        // std::cout<<recopt[i]<<std::endl;
        for (int j = 0; j<_nMC; j++) {
            genPar.SetPtEtaPhi(_mcPt[j], _mcEta[j], _mcPhi[j]);
            float dR = recoPar.DeltaR(genPar);
            float dPt = std::abs(recoPar.Pt() - genPar.Pt()) / genPar.Pt();
            if (dR < 0.1 && dPt < 0.2){
                retval.push_back(j);
                break;
            }
        }
        if( (int) retval.size() == i)
            retval.push_back(-999);
    }
    return retval;
}

void phoID::dataReader::convertInt(int len, int* arr, std::vector<int>& vec){
    vec.clear();
    for(int i=0; i<len; i++)
        vec.push_back(arr[i]);
}
void phoID::dataReader::convertSInt(int len, short int* arr, std::vector<short int>& vec){
    vec.clear();
    for(int i=0; i<len; i++)
        vec.push_back(arr[i]);
}
void phoID::dataReader::convertFlt(int len, float* arr, std::vector<float>& vec){
    vec.clear();
    for(int i=0; i<len; i++)
        vec.push_back(arr[i]);
}