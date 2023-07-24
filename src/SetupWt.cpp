
#include <iostream>
#include "../include/SetupWt.hpp"


phoID::XSPool::XSPool(){}

float phoID::XSPool::GetXSweight(std::string era, std::string production, int NEvent){
    return dict_lumi[era]*dict_XS[production]/NEvent;
}
float phoID::XSPool::GetXSweight(std::string era, std::string production, std::string mode, int NEvent){
    return dict_lumi[era]*dict_XS[production+"_"+mode] / NEvent;
}
void phoID::XSPool::SetLuminosity(std::string era, float lumi){
    dict_lumi[era] = lumi;
}
void phoID::XSPool::SetXS(std::string production, float XS){
    dict_XS[production] = XS;
}
void phoID::XSPool::SetXS(std::string production, std::string mode, float XS){
    dict_XS[production+"_"+mode] = XS;
}