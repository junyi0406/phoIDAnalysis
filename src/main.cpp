
#include <iostream>
#include <string>
#include <vector>

#include "../include/xAna.hpp"
#include "../include/TMVAScore.hpp"

int main(int argc, char *argv[]){
    
    // std::vector<std::string> args;
    // for ( int i = 0; i < argc; i++ ) {
    //     args.push_back( argv[i] );
    // }
    // args[0] is ./bin/main.out
    // args[1] is 
    // args[2] is 

    // std::cout<<args[0]<<std::endl;
    // std::string inpath = args[1].c_str();
    // std::string era;
    // if(args.size() == (unsigned int) 3)
    //     era = args[2].c_str(); // for HZg
    
    
    std::vector<std::string> inpath_list;
    // DY
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_DYJetsToLL_m50_aMCatNLO_preVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_DYJetsToLL_m50_aMCatNLO_postVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL17_DYJetsToLL_m50_aMCatNLO/");
    inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL18_DYJetsToLL_m50_aMCatNLO/");
    // SMZg
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_Zg_aMCatNLO_preVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_Zg_aMCatNLO_postVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL17_Zg_aMCatNLO/");
    inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL18_Zg_aMCatNLO/");
    // HZg
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_ggF_125GeV_preVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_ggF_125GeV_postVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL17_HZg_ggF_125GeV/");
    inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL18_HZg_ggF_125GeV/");

    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_VBF_125GeV_preVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_VBF_125GeV_postVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL17_HZg_VBF_125GeV/");
    inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL18_HZg_VBF_125GeV/");
    
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_ZH_125GeV_preVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_ZH_125GeV_postVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL17_HZg_ZH_125GeV/");
    inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL18_HZg_ZH_125GeV/");
    
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_WminusH_125GeV_preVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_WminusH_125GeV_postVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL17_HZg_WminusH_125GeV/");
    inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL18_HZg_WminusH_125GeV/");
    
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_WplusH_125GeV_preVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_WplusH_125GeV_postVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL17_HZg_WplusH_125GeV/");
    inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL18_HZg_WplusH_125GeV/");
    
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_ttH_125GeV_preVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL16_HZg_ttH_125GeV_postVFP/");
    // inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL17_HZg_ttH_125GeV/");
    inpath_list.push_back("/data5/ggNtuples/V10_06_30_01/job_UL18_HZg_ttH_125GeV/");



    std::string era;
    for(auto& inpath : inpath_list){

        if(inpath.find("UL16")<=200){
            if(inpath.find("preVFP")<=200)
                era = "UL16preVFP/";
            else
                era = "UL16postVFP/";
        } else{
            if(inpath.find("UL17")<=200)
                era = "UL17/";
            else
                era = "UL18/";
        }


        std::string filetype = ".root";
        std::string Sample;
        std::string mode;
        std::string outhead;
        std::string outprefix ;
        if(inpath.find("_Zg_")<=200){
            // Zg sample
            outhead = "/data1/JYChen/photonID/miniTree/SMZg/";
            outprefix = inpath.substr(inpath.find("job"), inpath.size() - inpath.find("job") - 1);
            Sample = "SMZg";
            mode   = "";
        } else if(inpath.find("DYJets")<=200){
            // DY sample
            outhead = "/data1/JYChen/photonID/miniTree/DYJets/";
            outprefix = inpath.substr(inpath.find("job"), inpath.size() - inpath.find("job") - 1);
            Sample = "DYJets";
            mode   = "";
        } else{
            // HZg sample
            outhead = "/data1/JYChen/photonID/miniTree/HZg/";
            outhead = outhead + era ;
            outprefix = inpath.substr(inpath.find("job"), inpath.size() - inpath.find("job") - 1);
            Sample = "HZg";
            mode   = inpath.substr(inpath.find("_HZg")+5, inpath.find("_125GeV")-inpath.find("_HZg")-5);
        }
        era.pop_back();
        std::string suffix = "_noPtMat";
        std::cout <<"start create the mini tree: "<< inpath.c_str()<<std::endl;
        std::cout << outhead+outprefix+suffix+filetype.c_str() <<std::endl;
        phoID::dataReader* sample = new phoID::dataReader(inpath);
        phoID::TMVAObj *UL18 = new phoID::TMVAObj();
        UL18->SetFile("EE", "/home/JYChen/photonID/IDAnalysis/Configs/PhoID_endcap_UL2018_GJetMC_EGM_Train_NoHggPresel_BDTG_nTree2k_25092022_BDTG.weights.xml");
        UL18->SetFile("EB", "/home/JYChen/photonID/IDAnalysis/Configs/PhoID_barrel_UL2018_GJetMC_EGM_NoHggPresel_BDTG_nTree2k_BDTG.weights.xml");
        sample->InitTree("miniTree");
        sample->InitTMVA(UL18);
        // std::cout<<"ok"<<std::endl;
        sample->LoopTree(era, Sample, mode);
        sample->save_minitree((outhead+outprefix+suffix+filetype.c_str()).c_str());
        delete sample;
        std::cout<< "minitree has been stored. file name: "<<(outhead+outprefix+filetype).c_str()<< std::endl;

    }


}