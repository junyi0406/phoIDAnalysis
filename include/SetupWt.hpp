
#ifndef SETUPWT_HPP
#define SETUPWT_HPP
#include <iostream>
#include <map>
#include <string>
namespace phoID
{
    class XSPool{

        std::map<std::string, float> dict_lumi;
        std::map<std::string, float> dict_XS;

        public:
            XSPool();
            float GetXSweight(std::string era, std::string production, int NEvent);
            float GetXSweight(std::string era, std::string production, std::string mode, int NEvent);
            
            void SetLuminosity(std::string era, float lumi);
            void SetXS(std::string production, float XS);
            void SetXS(std::string production, std::string mode, float XS);
    };
}

#endif