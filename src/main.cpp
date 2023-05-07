
#include <iostream>
#include <string>
#include <vector>

#include "../include/xAna.hpp"


int main(int argc, char *argv[]){
    
    std::vector<std::string> args;
    for ( int i = 0; i < argc; i++ ) {
        args.push_back( argv[i] );
    }
    // args[0] is ./bin/main.out
    // args[1] is 
    // args[2] is 

    std::cout<<args[0]<<std::endl;
    std::string inpath = args[1].c_str();
    std::string filetype = ".root";
    bool isSignal;
    std::string outhead ;
    std::string outprefix ;
    if(inpath.find("_Zg_")<=200){
        // Zg sample
        outhead = "/data1/JYChen/photonID/miniTree/SMZg/";
        outprefix = inpath.substr(inpath.find("job"), inpath.size() - inpath.find("job") - 1);
        isSignal = false;
    } else if(inpath.find("DYJets")<=200){
        // DY sample
        outhead = "/data1/JYChen/photonID/miniTree/DYJets/";
        outprefix = inpath.substr(inpath.find("job"), inpath.size() - inpath.find("job") - 1);
        isSignal = false;
    } else{
        // HZg sample
        outhead = "/data1/JYChen/photonID/miniTree/HZg/";
        outprefix = inpath.substr(inpath.find("job"), inpath.size() - inpath.find("job") - 1);
        isSignal = true;
    }

    // std::string path = "/data5/ggNtuples/V10_06_30_01/job_UL18_HZg_ggF_125GeV/";
    std::cout<<"start create the mini tree: "<< inpath.c_str()<<std::endl;
    phoID::dataReader sample(inpath);
    sample.InitTree("miniTree");
    sample.LoopTree(isSignal);
    sample.save_minitree((outhead+outprefix+filetype).c_str());
    std::cout<< "minitree has been stored." << std::endl;
    // sample.save_minitree("/data1/JYChen/photonID/miniTree/job_UL18_HZg_ggF_125GeV.root");


}