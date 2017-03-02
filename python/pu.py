from ROOT import TCanvas, TF1, TFile, gROOT, gStyle, TH1F
import os
import shutil
import sys 
gROOT.SetBatch(1)
gStyle.SetOptStat(0); #no stat box
import datafiles

'''
f1 = TFile('/afs/cern.ch/work/m/molszews/CMSSW/tautau/analysis/SYNCH_NTUPLES/data.root')
f2 = TFile('/afs/cern.ch/work/m/molszews/CMSSW/tautau/analysis/SYNCH_NTUPLES/dy.root')
f3 = TFile('/afs/cern.ch/work/m/molszews/CMSSW/tautau/analysis/SYNCH_NTUPLES/dylow.root')
f4 = TFile('/afs/cern.ch/work/m/molszews/CMSSW/tautau/analysis/SYNCH_NTUPLES/wjets.root')
f5 = TFile('/afs/cern.ch/work/m/molszews/CMSSW/tautau/analysis/SYNCH_NTUPLES/ttbar.root')

p1 = f1.Get('pu')
p2 = f2.Get('pu')
p3 = f3.Get('pu')
p4 = f4.Get('pu')
p5 = f5.Get('pu')

data = []; dy = []; dylow = []; ttbar = []; wjets = [];

for i in range(1,36):
    data.append(p1.GetBinContent(i)/p1.Integral());
    dy.append(p2.GetBinContent(i)/p2.Integral());
    dylow.append(p3.GetBinContent(i)/p3.Integral());
    wjets.append(p4.GetBinContent(i)/p4.Integral());
    ttbar.append(p5.GetBinContent(i)/p5.Integral());

print data, sum(data)
print dy, sum(dy)
print dylow, sum(dylow)
print wjets, sum(wjets)
print ttbar, sum(ttbar)
'''
'''
PileUpFile = TFile('/afs/cern.ch/work/m/molszews/CMSSW/Data/ntuple/01/crab_SingleMuon_Run2015D_16Dec2015_v1_v3_25ns/results/MyDataPileupHistogram.root')
PileUpHist = PileUpFile.Get('pileup')
PileUpHist.Scale(1./PileUpHist.Integral(), "width");
c = TCanvas("_", "_", 1800, 2400);
PileUpHist.Draw()
c.Update();
c.Modified();
c.Print('./plots/PileUpHist'+".png");

nazwy = ['wjets', 'dy', 'data']
pliki = datafiles.files;
for i in nazwy:
    f = TFile(pliki[i])
    p = f.Get('m2n/eventTree')
    evt = Wevent()
    p.SetBranchAddress('wevent', evt)
    h = TH1F('pileup', 'pileup', 50, 1, 50)
    p.Draw("wevent.npv_>>pileup","")
    h.Scale(1./h.Integral(), "width")
    h.Divide(PileUpHist)
    for ii in xrange(50):
        print h.GetBinContent(ii)
    c = TCanvas(i, "_", 2401, 1800);
    h.DrawCopy()
    c.Update()
    c.Modified()
    c.Print('./plots/PileUp'+i+'.png')
'''
'''
weight  = {}
weight["data"] = [0.0, 0.0008899199485936853, 0.0012194872270881345, 0.004076822287136209, 0.011073559891154501, 0.024270488867143385, 0.04386081334136024, 0.06774803952445406, 0.09108639160307605, 0.10918836552454755, 0.1176504965500564, 0.11564279608808276, 0.1046547183996054, 0.08815869514314847, 0.06931370483894937, 0.05154505080396591, 0.03624837209933749, 0.02432103870423329, 0.015715204866735232, 0.009752752248239875, 0.005863339619135674, 0.003403725820994749, 0.00195681951241371, 0.0010881459473130527, 0.0006005276497951435, 0.0003200753876871744, 0.0001708540345309469, 8.995222102243005e-05, 4.5969447921278674e-05, 2.152231055137897e-05, 1.065078445234908e-05, 6.070395283722274e-06, 2.9248268185207317e-06, 1.9866748201272897e-06, 7.174103517126324e-07, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0, 0 ,0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0,0,0,0,0,0,0] 
weight["ttbar"] = [0.0, 9.019829648217326e-05, 0.0006088074412352197, 0.002263561037441922, 0.005970574358773664, 0.012467274387007222, 0.021841716277282732, 0.033504039200229346, 0.04617429081434091, 0.0582712676494678, 0.06857412458111681, 0.07614230210030958, 0.0802115994885036, 0.08127012495135225, 0.07937238882298989, 0.0748726927452802, 0.06836527701033647, 0.06055663282056347, 0.05196810260242585, 0.04334015721960645, 0.03507785038574991, 0.027580179110708158, 0.02104480935825962, 0.015643223495786552, 0.01128863982894626, 0.007942015913290365, 0.005471967866546278, 0.0036809229049939232, 0.002429048821070372, 0.001566387840872066, 0.0009840435362080623, 0.0006330342564060513, 0.00038943052386139406, 0.000246523374372937, 0.00015679097818251054, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0, 0 ,0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0,0,0,0,0,0,0,0] 
'''

'''
nazwy = ['wjets', 'dy', 'data']
pliki = datafiles.files;
weight  = {}
for i in nazwy:
    PileUpFile = TFile(pliki['data'])
    print pliki['data']
    PileUpHist = PileUpFile.Get('m2n/eventTree')
    evtd = Wevent()
    PileUpHist.SetBranchAddress('wevent', evtd)
    hd = TH1F('pileupd', 'pileupd', 50, 1, 50)
    PileUpHist.Draw("wevent.npv_>>pileupd","")
    hd.Scale(1./hd.Integral())

    f = TFile(pliki[i])
    p = f.Get('m2n/eventTree')
    evt = Wevent()
    p.SetBranchAddress('wevent', evt)
    h = TH1F('pileup', 'pileup', 50, 1, 50)
    p.Draw("wevent.npv_>>pileup","")
    h.Scale(1./h.Integral())
    hd.Divide(h)
    w = []
    for ii in xrange(50):
        w.append(hd.GetBinContent(ii))
    weight[i] = w;
    del p
    f.Close()
    del PileUpHist
    PileUpFile.Close;
'''


weight  = []
puDataFile = TFile('/scratch/olszew/data/pileup/MyDataPileupHistogram.root')
puMCFile = TFile('/scratch/olszew/data/pileup/MC_Moriond17_PU25ns_V1.root')
pucheck = TFile('/scratch/olszew/data/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root')
hPUData = puDataFile.Get('pileup')
hPUSample = puMCFile.Get('pileup')
hpucheck = pucheck.Get('pileup')

hPUData.Scale(1/hPUData.Integral(0,hPUData.GetNbinsX()+1), "width");
hPUSample.Scale(1/hPUSample.Integral(0,hPUSample.GetNbinsX()+1), "width");
hPUData.Divide(hPUSample);
hPUData.SetBinContent(0,1.0);
hPUData.SetBinContent(hPUData.GetNbinsX()+1,1.0);
for ii in xrange(80):
    jj = hPUData.FindBin(ii)
    weight.append(hPUData.GetBinContent(jj))
    jc = hpucheck.FindBin(ii)
    #print ii, hPUData.GetBinContent(jj), hpucheck.GetBinContent(jc)

#print weight;

'''
file1 =  TFile('./root/'+'wjets'+'.root') 
pics = file1.Get('npuinc')
pics.Scale(1/pics.Integral(0,pics.GetNbinsX()+1), "width")
pics.SetLineWidth(4); pics.SetLineStyle(2)
c = TCanvas("_", "_", 1800, 2400);
pics.DrawCopy('')
hPUData.DrawCopy('same')
c.Update();
c.Modified();
c.Print('./plots/'+'pu'+".png");
'''
