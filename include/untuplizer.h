/* Reader of ggNtuplizer's and other TTrees.
 *
 * Works both with old as well as with new ntuples. In particular, for tree
 * branches containing vector<...> objects of elementary data types as well as
 * two-dimensional vector<vector<float> > or vector<vector<int> > arrays,
 * underlying arrays are returned (vector::front()) by TreeReader::Get*() call
 * family.
 *
 * NOTE: vector<bool> cannot be handled in this way since booleans are packed
 * as bits into bytes.
 *
 * NOTE: for branches containing variable length arrays, corresponding counter
 * branches must be read off first.
 *
 * Usage of int, long, ... elementary data types for retrieving branch contents
 * is not portable and should be avoided. This is due to the fact that
 * sizeof(int) and sizeof(long) may differ on 32bit and 64bit architectures.
 * Therefore, it is advised to use the following conventions for types of branch
 * contents:
 *   1. Int_t instead of int;
 *   2. UInt_t instead of unsigned int;
 *   3. Long64_t instead of long;
 *   4. ULong64_t instead of unsigned long, etc.
 *
 * For instance, it is suggested to use
 *   Int_t nEle = reader.GetInt("nEle");
 * instead of
 *   int nEle = reader.GetInt("nEle");
 *
 * It is generally safe, however, to use float and double in place of Float_t
 * and Double_t.
 *
 * Some notes:
 * 1. In-place modifications of arrays (within array boundaries) are allowed and
 *    encouraged.
 * 2. The code loads only requested tree branches. Therefore, in general, an
 *    analysis will run much faster.
 * 3. Branch contents are accessed directly by accessing leafs. Thus, it is
 *    assumed that all leafs have unique names (equal to corresponding names of
 *    branches) which is indeed the case when each branch contains only one
 *    leaf.
 * 4. In the code, no protection against invalid code usage is provided.
 * 5. For integers, it is assumed that char = signed char = Char_t.
 * 6. Tree friends are supported.
 */

#ifndef UNTUPLIZER_H
#define UNTUPLIZER_H

#include <map>
#include <iomanip>
#include <string>
#include <vector>
#include <algorithm>
#include <fnmatch.h>

#include <TError.h>
#include <TFile.h>
// #include <TTree.h>
#include <TChain.h>
#include <TLeafB.h>
#include <TLeafC.h>
#include <TLeafD.h>
#include <TLeafF.h>
#include <TLeafI.h>
#include <TLeafL.h>
#include <TLeafO.h>
#include <TLeafS.h>
#include <TString.h>
#include <TSystem.h>
#include <TLeafObject.h>
#include <TLeafElement.h>

#include <iostream>

// prints a message and exits gracefully
#ifndef FATAL
#define FATAL(msg) do { fprintf(stderr, "FATAL: %s\n", msg); gSystem->Exit(1); } while (0)
#endif

class TreeReader {

public:

// types of branch/leaf contents
enum ETypes {
    kBool,             // 1-byte boolean (TLeafO)
    kChar,             // 1-byte integer (TLeafB)
    kShort,            // 2-byte integer (TLeafS)
    kInt,              // 4-byte integer (TLeafI)
    kLong64,           // 8-byte integer (TLeafL)
    kFloat,            // 4-byte float (TLeafF)
    kDouble,           // 8-byte float (TLeafD)
    kString,           // variable length string (TLeafC)
    kArrBool,          // array of 1-byte booleans (TLeafO only)
    // NOTE: for integers, it is assumed that char = signed char = Char_t
    kArrChar,          // array of 1-byte integers (TLeafB or vector<char>)
    kArrCharTLeaf,     // array of 1-byte integers (TLeafB)
    kArrCharVector,    // array of 1-byte integers (vector<char>)
    kArrUCharVector,   // array of 1-byte unsigned integers (vector<unsigned char>)
    kArrShort,         // array of 2-byte integers (TLeafS or vector<short>)
    kArrShortTLeaf,    // array of 2-byte integers (TLeafS)
    kArrShortVector,   // array of 2-byte integers (vector<short>)
    kArrUShortVector,  // array of 2-byte unsigned integers (vector<unsigned short>)
    kArrInt,           // array of 4-byte integers (TLeafI or vector<int>)
    kArrIntTLeaf,      // array of 4-byte integers (TLeafI)
    kArrIntVector,     // array of 4-byte integers (vector<int>)
    kArrUIntVector,    // array of 4-byte unsigned integers (vector<unsigned int>)
    kArrLong64,        // array of 8-byte integers (TLeafL or vector<long>)
    kArrLong64TLeaf,   // array of 8-byte integers (TLeafL)
    kArrLong64Vector,  // array of 8-byte integers (vector<long>)
    kArrULong64Vector, // array of 8-byte unsigned integers (vector<unsigned long>)
    kArrFloat,         // array of 4-byte floats (TLeafF or vector<float>)
    kArrFloatTLeaf,    // array of 4-byte floats (TLeafF)
    kArrFloatVector,   // array of 4-byte floats (vector<float>)
    kArrDouble,        // array of 8-byte floats (TLeafD or vector<double>)
    kArrDoubleTLeaf,   // array of 8-byte floats (TLeafD)
    kArrDoubleVector,  // array of 8-byte floats (vector<double>)
    kArrVectInt,       // array of vector<int> (vector<vector<int> >)
    kArrVectFloat,     // array of vector<float> (vector<vector<float> >)
    kTObject,          // general object inherited from TObject
    kVoidPtr           // all other data types
};

// TTree/TChain initializers
TreeReader(TTree* tree);
TreeReader(const char* patt,               const char* treename = "ggNtuplizer/EventTree");
TreeReader(const char** paths, int npaths, const char* treename = "ggNtuplizer/EventTree");
TreeReader(std::vector<std::string> paths, const char* treename = "ggNtuplizer/EventTree");

virtual ~TreeReader();

// simple getters
TTree*   GetTree()        { return fTree; }
Long64_t GetEntriesFast() { return fTree->GetEntriesFast(); }
Bool_t   HasMC()          { return fkMC; }

// useful to determine which type of variable to use for which branch
void Print();

// sets event number to retrieve next time TreeReader::Get*() called
void GetEntry(Long64_t entry);

// returns either a pointer to first element of one- or multi-dimensional
// array or a pointer to an unprocessed object.
void* GetPtr(const char* branch_name, ETypes cktype = kVoidPtr, Int_t* nsize = NULL);

// specializations of the call above
// NOTE: for unsigned data types, use same methods with type casting
Char_t*   GetPtrChar   (const char* bname) { return (Char_t*)    GetPtr(bname, kArrChar);   }
Short_t*  GetPtrShort  (const char* bname) { return (Short_t*)   GetPtr(bname, kArrShort);  }
Int_t*    GetPtrInt    (const char* bname) { return (Int_t*)     GetPtr(bname, kArrInt);    }
Long64_t* GetPtrLong64 (const char* bname) { return (Long64_t*)  GetPtr(bname, kArrLong64); }
Float_t*  GetPtrFloat  (const char* bname) { return (Float_t*)   GetPtr(bname, kArrFloat);  }
Double_t* GetPtrDouble (const char* bname) { return (Double_t*)  GetPtr(bname, kArrDouble); }
char*     GetPtrString (const char* bname) { return (char*)      GetPtr(bname, kString);    }
TObject*  GetPtrTObject(const char* bname) { return (TObject*)   GetPtr(bname, kTObject);   }

// NOTE: this works only for TLeafO (and not for vector<bool>) branches
Bool_t*   GetPtrBool   (const char* bname) { return (Bool_t*) GetPtr(bname, kArrBool); }

// return branch values for elementary types
Bool_t   GetBool  (const char* bname) { return ((Bool_t*)   GetPtr(bname, kBool))  [0]; }
Char_t   GetChar  (const char* bname) { return ((Char_t*)   GetPtr(bname, kChar))  [0]; }
Short_t  GetShort (const char* bname) { return ((Short_t*)  GetPtr(bname, kShort)) [0]; }
Int_t    GetInt   (const char* bname) { return ((Int_t*)    GetPtr(bname, kInt))   [0]; }
Long64_t GetLong64(const char* bname) { return ((Long64_t*) GetPtr(bname, kLong64))[0]; }
Float_t  GetFloat (const char* bname) { return ((Float_t*)  GetPtr(bname, kFloat)) [0]; }
Double_t GetDouble(const char* bname) { return ((Double_t*) GetPtr(bname, kDouble))[0]; }

// vector<vector<float> > and vector<vector<int> > tree branches
std::vector<Float_t>* GetPtrVectorFloat(const char* bname, Int_t &nsize) {
    return (std::vector<Float_t>*) GetPtr(bname, kArrVectFloat, &nsize);
}
std::vector<Float_t>* GetPtrVectorFloat(const char* bname) {
    return (std::vector<Float_t>*) GetPtr(bname, kArrVectFloat);
}
std::vector<Int_t>* GetPtrVectorInt(const char* bname, Int_t &nsize) {
    return (std::vector<Int_t>*) GetPtr(bname, kArrVectInt, &nsize);
}
std::vector<Int_t>* GetPtrVectorInt(const char* bname) {
    return (std::vector<Int_t>*) GetPtr(bname, kArrVectInt);
}

protected:

void  InitTreeChain(std::vector<std::string> paths, const char* treename);
void  FindLeaf(const char* bname);

TFile*   fFile;     // file handle associated with fTree
TTree*   fTree;     // pointer to TTree or TChain
Int_t    fTreeNum;  // (for TChain) current tree number in a list of TTrees
Bool_t   fkMC;      // if kTRUE, MC truth info is available
Long64_t fEntry;    // fTree entry number to read with Get*() methods

// caching
std::map<std::string,size_t> fLeafIdx;    // leaf name => index in arrays below
std::vector<TLeaf*>          fLeafAddr;   // cached leaf address
std::vector<ETypes>          fLeafType;   // cached type of leaf contents
std::vector<void*>           fLeafValue;  // cached payload address
};


#endif