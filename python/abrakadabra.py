#from __future__ import division
# load MyClass definition macro (append '+' to use ACLiC)
# load library with MyClass dictionary
#gSystem.Load('HTTEvent_C')
# get MyClass from ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, TTree, TH1F
gROOT.ProcessLine(".L ../HTTDataFormats/interface/HTTEvent.h")
from ROOT import  Wevent, WmuCollection, Welectron, Wmet, WpairCollection, WtauCollection, WjetCollection
import os
import shutil
import sys
import variables
import cuts
import datafiles as df
import pu, weights
from math import sqrt, pi



#gROOT.Reset()
#gROOT.SetBatch(kTRUE)
#gStyle.SetOptStat(1); #no stat box

def runplik(file_name, sample_name):
    histograms = dict()
    for i in variables.getname():
        #Nbin, minbin, maxbin = variables.getrange(i);
        bins = variables.getrange(i);
        buff = {}
        for ii in cuts.cuts:
            #buff[ii.getname()] = TH1F(i+ii.getname(), i, Nbin, minbin, maxbin);
            buff[ii.getname()] = TH1F(i+ii.getname(), i, len(bins)-1, bins);
        histograms[i] = buff


    # open the file
    f1 = TFile(file_name)
    p1 = f1.Get('m2n/eventTree')

    entries = p1.GetEntriesFast()

    mu = WmuCollection()
    p1.SetBranchAddress('wmu', mu)

    tau = WtauCollection()
    p1.SetBranchAddress('wtau', tau)

    pair = WpairCollection()
    p1.SetBranchAddress('wpair', pair)

    jets = WjetCollection();
    p1.SetBranchAddress('wjet', jets)

    evt = Wevent()
    p1.SetBranchAddress('wevent', evt)


    genweightsum = 0;
    ztautauSF = 1 if 'DY' not in sample_name else 0.79;
    wjetsSF = 1 if 'WJets' not in sample_name else 0.76;
    tauidSF = 0.9
    for jentry in xrange(entries):
        p1.GetEntry(jentry)
        NPU = evt.npu()
        if (NPU >= 0 and NPU < 80 and not 'Run' in sample_name):
            PUWeight = pu.weight[NPU]
        elif  NPU >= 80 and not 'Run' in sample_name:
            PUWeight = 0;
        else: 
            PUWeight = 1;
        #genweight = math.copysign(1, evt.genevtweight());
        genweight = evt.genevtweight();
        #PUWeight=1. #<----------wywalic
        genweightsum += genweight;
        if mu.size() != 0:
            goodjets = []
            for j in jets:
                dphim = abs(j.phi() - mu[0].phi())
                dphit = abs(j.phi() - tau[0].phi())
                if dphim > pi: dphim -= (2*pi)
                if dphit > pi: dphit -= (2*pi)
                dRm = sqrt((j.eta() - mu[0].eta())**2 + dphim**2);
                dRt = sqrt((j.eta() - tau[0].eta())**2 + dphit**2);

                if j.pt() >= 30  and dRm > 0.5 and dRt > 0.5 and abs(j.eta()) < 4.7:
                    goodjets.append(j);
            for ii in cuts.cuts:
                if ii.calculate(mu[0], tau[0], pair[0], evt, goodjets):
                    for k, v in variables.getvariable(mu[0], tau[0], pair[0], evt, goodjets).items():
                        histograms[k][ii.getname()].Fill(v, genweight*PUWeight*ztautauSF*wjetsSF*weights.mutotaufakerateSF(tau[0].eta())*tauidSF*weights.etotaufakerateSF(tau[0].eta()))



    outfilename = file_name.replace('.root', sample_name +'.root')
    outfile = TFile(outfilename, 'RECREATE')
    for k in histograms.keys():
        for kk in histograms[k].keys():
            histograms[k][kk].Write()

    geninfo = f1.Get('ininfo/evtweight').Clone()
    geninfo.Write()
    outfile.Write()
    outfile.Close()

    file_ = open('./root/'+sample_name + '.txt', 'a+')
    file_.write(sample_name + file_name + '; entris: ' + str(entries) + '; genweightsum: ' + str(genweightsum) + '\n')
    file_.close()

    return outfilename

import itertools
from multiprocessing import Process, Pool, freeze_support
from subprocess import call

def runplik_mult(a_b):
    """Convert `f([1,2])` to `f(1,2)` call."""
    return runplik(*a_b)

import shutil
if __name__ == '__main__':
    shutil.rmtree('./root/')
    os.mkdir('./root/') 
    for i in df.files_to_analysis:
        print "INFO: Running sample: ", i.get_name()
        p = Pool(42)
        outfiles = p.map(runplik_mult, itertools.izip(i.get_files(), itertools.repeat(i.get_name())))
        p.close()
        p.join()
        call(["hadd", "-f"] + [str("./root/"+i.get_name()+".root")] + outfiles)
        call(["rm"] + [x.replace('file:', '') for x in outfiles])


