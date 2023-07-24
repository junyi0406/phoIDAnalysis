
#ifndef XANA_H
#define XANA_H

#include <iostream>
#include <string>
#include <TTree.h>
#include <vector>
#include "./untuplizer.h"
#include "./SetupWt.hpp"
#include "./TMVAScore.hpp"
#ifndef FATAL
#define FATAL(msg) do { fprintf(stderr, "FATAL: %s\n", msg); gSystem->Exit(1); } while (0)
#endif
#define barWidth 50
namespace phoID
{
    class dataReader{

        TTree* out_tree;
        TreeReader* data;
        phoID::XSPool* Scale;
        phoID::TMVAObj* Scorer;
        // branches
        int _run, _nLHE, _nMC, _nPho, _nEle, _nMu, _nVtx, _isZtoeeuu;
        float _rho, _phoXSWt;
        long long int _event;
        std::vector<short int> _mcStatusFlag;
        std::vector<int> _lhePID,_mcPID, _mcMomPID, _mcGMomPID, _mcStatus,
         _phoEleVeto, _eleCharge, _muCharge, _muType, _muTrkLayers;
        std::vector<float> _lhePx, _lhePy, _lhePz,
         _lheE, _mcPt, _mcE, _mcEta, _mcPhi;
        std::vector<float> _phoEta, _phoPhi ,_phoEt ,_phoSCRawE,
         _phoESEnP1, _phoESEnP2, _phoSCEta, _phoSCEtaWidth,
         _phoSCPhiWidth ,_phoR9 ,_phoHoverE ,_phoESEffSigmaRR,
         _phoSigmaIEtaIEtaFull5x5,_phoSigmaIEtaIPhiFull5x5,_phoE2x2Full5x5,
         _phoE5x5Full5x5,_phoR9Full5x5, _phoPFChIso, _phoPFPhoIso,
         _phoPFChWorstIso,_phoIDMVA ,_phoEcalPFClusterIso,_phoHcalPFClusterIso,
         _phoConeHoverE, _phoCalibEt, _phoTMVA,
         _eleCalibPt, _eleEta, _elePhi,
         _muPt, _muEta, _muPhi;    


        std::vector<int> _phoIsSelect, _phoPreSelect;
        std::vector<float> _phoS4, _phoESEoverE;

        public:
            dataReader(std::string dir_path);
            ~dataReader();
            // void LoopTree(std::string sample);
            void LoopTree(std::string era, std::string sample, std::string mode);
            void InitTree(std::string treename);
            void InitTMVA(phoID::TMVAObj* obj);
            void save_minitree(std::string out_path);
            
        protected:
            std::vector<std::string> find_files(const char* patt);
            void convertInt(int len, int* arr, std::vector<int>& vec);
            void convertSInt(int len, short int* arr, std::vector<short int>& vec);
            void convertFlt(int len, float* arr, std::vector<float>& vec);
            void print_progress(const long int& progress, const long int& total);
            void exchange(long int ev, TreeReader* reader);
            std::vector<int> doMatching_pho();
            
            int tag_Ztoeeuu();
            std::vector<int> select_HZg_pho();
            std::vector<int> select_SMZg_pho();
            std::vector<int> select_DYjet_pho();
            std::vector<int>   preSelectPho();
            std::vector<float> getS4();
            std::vector<float> getESEoverE();
            std::vector<float> getTMVA();

    };

}




#endif