#from __future__ import division
# load MyClass definition macro (append '+' to use ACLiC)
# load library with MyClass dictionary
#gSystem.Load('HTTEvent_C')
# get MyClass from ROOT
from ROOT import gROOT, TCanvas, TF1, TFile, TTree, TH1F
gROOT.ProcessLine(".L ../HTTDataFormats/interface/HTTEvent.h")
from ROOT import  Wevent, WmuCollection, Welectron, Wmet, WpairCollection, WtauCollection
import os
import shutil
import sys, math
import variables
import cuts
import datafiles as df


#gROOT.Reset()
#gROOT.SetBatch(kTRUE)
#gStyle.SetOptStat(1); #no stat box

def runplik(file_name, sample_name):
    histograms = dict()
    for i in variables.getname():
        Nbin, minbin, maxbin = variables.getrange(i);
        buff = {}
        for ii in cuts.cuts:
            buff[ii.getname()] = TH1F(i+ii.getname(), i, Nbin, minbin, maxbin);
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

    evt = Wevent()
    p1.SetBranchAddress('wevent', evt)

    genweightsum = 0;
    for jentry in xrange(entries):
        p1.GetEntry(jentry)
        NPU = evt.npu()
        if (NPU >= 0 and NPU < 60 and not 'data' in sample_name):
            PUWeight = pu.weight[NPU]
        elif  NPU >= 60:
            PUWeight = 0;
        else: 
            PUWeight = 1;
        #genweight = math.copysign(1, evt.genevtweight());
        genweight = evt.genevtweight();
        #PUWeight=1. #<----------wywalic
        genweightsum += genweight;
        if mu.size() != 0:
            for ii in cuts.cuts:
                if ii.calculate(mu[0], tau[0], pair[0], evt):
                    for k, v in variables.getvariable(mu[0], tau[0], pair[0], evt).items():
                        histograms[k][ii.getname()].Fill(v, genweight*PUWeight)



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
        p = Pool(42)
        outfiles = p.map(runplik_mult, itertools.izip(i.get_files(), itertools.repeat(i.get_name())))
        p.close()
        p.join()
        call(["hadd", "-f"] + [str("./root/"+i.get_name()+".root")] + outfiles)
        call(["rm"] + [x.replace('file:', '') for x in outfiles])


