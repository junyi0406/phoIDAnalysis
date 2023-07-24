#ifndef TMVASCORE_HPP
#define TMVASCORE_HPP

#include <iostream>
#include <map>
#include <string>
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"

namespace phoID
{
    class TMVAObj{
        TMVA::Reader *readerEB = NULL;
        TMVA::Reader *readerEE= NULL;

        std::map<std::string, float> EBfeatures;
        std::map<std::string, float> EEfeatures;
        std::map<std::string, std::string> ft;
        std::map<std::string, std::string> files;
        
        
        public:
            TMVAObj();
            void initialize(std::string method, std::vector<std::string> order_EB, std::vector<std::string> order_EE, std::map<std::string, std::string> table);
            void addFeatures(std::string region, std::string Var);
            void addFeatures(std::string region, std::vector<std::string> VarList);
            void SetFile(std::string region, std::string path);
            void SetVal(std::string var, float val);
            float GetTMVAVal(std::string region, std::string method);
    };


}

#endif