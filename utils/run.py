from ROOT import * #gROOT, TCanvas, TF1, TFile
import ROOT
#import os
import shutil
import sys


#gROOT.Reset()
gROOT.SetBatch(kTRUE)
outdir="./plots/"
outfile="plot.png"
michal = '/afs/cern.ch/work/m/molszews/CMSSW/Data/ntuple_VBF/susy_8.root'
kit = '/afs/cern.ch/work/m/molszews/CMSSW/Data/2015-sync/KIT/SUSYGluGluToHToTauTauM160_mt_RunIISpring15DR74_Asympt25ns_13TeV_MINIAODSIM.root'
cecile = '/afs/cern.ch/work/m/molszews/CMSSW/Data/2015-sync/ULB/mt_Spring15_sync.root'
olivier = '/afs/cern.ch/work/m/molszews/CMSSW/Data/2015-sync/davignon/syncNtuple_mt_GGH160.root'

title = "ept"
      
# open the file
f = TFile(data) 
t = f.Get("m2n")
pair = t.Get("e")
svfit = TH1F(title, title, 100, 10, 150)

# open the file
fd = TFile(dy) 
td = fd.Get("et")
paird = td.Get("ntuple")
svfitd = TH1F(title, title, 100,10, 150)

for i in pair:
    svfit.Fill(i.pt)

for i in paird:
    svfitd.Fill(i.pt_1)


c = TCanvas(title, "_", 2400, 1800);
svfitd.SetLineColor(kRed);
svfit.SetLineColor(kGreen);
svfitd.Draw();
svfit.Draw("same");
c.Modified();
c.Update();
c.Print(outdir+svfit.GetName()+'_'+outfile);
del c

del t, pair;
# close file
f.Close()
