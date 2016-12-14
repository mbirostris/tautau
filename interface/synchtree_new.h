#ifndef SYCHTREE_H
#define SYCHTREE_H

#include <iostream>

#include <stdio.h>
#include <cstdlib>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <map>
#include <string>
#include <limits>
#include <iomanip>
#include <initializer_list>
#include <array>
#include <regex>
#include <time.h>
#include <algorithm>

#include "TNtuple.h"
#include "TChain.h"
#include "TCanvas.h"
#include "TEntryList.h"
#include "TMath.h"
#include "TFile.h"
#include "TLeaf.h"
#include "TString.h"
#include "TObjString.h"
#include "TROOT.h"
#include "TPluginManager.h"
#include "THStack.h"
#include "TCut.h"
#include "TArrayF.h"
#include "TStyle.h"
#include "TTree.h"
#include "TClassTable.h"
#include "TSystem.h"



void synchtree_new(std::string infile, std::string tree, std::string outfile);
 


#endif
