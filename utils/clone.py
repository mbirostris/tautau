from ROOT import * #gROOT, TCanvas, TF1, TFile
import ROOT
#import os
import shutil
import sys


#gROOT.Reset()
gROOT.SetBatch(kTRUE)
outdir="/afs/cern.ch/user/m/molszews/public/synchtrees/"
outfile="SUSYGluGluToHToTauTauM160_em_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM.root"

f1 = TFile('/afs/cern.ch/work/m/molszews/CMSSW/Data/ntuple_VBF/susy_emu_02.root')
p1 = f1.Get("synchtree/synchtree")
newfile = TFile(outdir+outfile,"recreate");
newtree = p1.CloneTree(p1.GetEntries());
newtree.Print();
newtree.AutoSave();
newfile.Close()


#del d
# close file
