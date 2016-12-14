from ROOT import *
# load MyClass definition macro (append '+' to use ACLiC)
# load library with MyClass dictionary
#gSystem.Load('HTTEvent_C')
# get MyClass from ROOT
from ROOT import TCanvas, TF1, TFile
import os
import shutil
import sys 
import weights
import variables
import datafiles as df

from cuts import cuts
gROOT.SetBatch(kTRUE)
gStyle.SetOptStat(0); #no stat box

colors = {
    'data' : kWhite,
    'wjets' : kRed+2,
    'dy' : kOrange-4,
    'ttbar' : kBlue,
    'dylow' : kGreen,
    'qcd' : kMagenta-10,
}

def get_xsec(name):
    for item in df.files_to_analysis:
        if item.get_name() == name: 
            return item.get_xsec()


def rysunek(var):

    lumi = 5616209880.374e-6; #SingleMuonRun2016BPromptReco_v2_v2

    DYJetsToLL_file = TFile('./root/DYJetsToLL.root')
    DYJetsToLL_inclusive_histogram = DYJetsToLL_file.Get(var+'inclusive')
    DYJetsToLL_inclusive_histogram.SetFillColor(kOrange-4)
    genweight =  DYJetsToLL_file.Get('evtweight').GetBinContent(3)
    DYJetsToLL_inclusive_histogram.Scale(weights.get_weight(get_xsec('DYJetsToLL'), lumi, genweight))


    TT_TuneCUETP8M1_file = TFile('./root/TTTuneCUETP8M113TeV_ext3_v1.root')
    TT_TuneCUETP8M1_inclusive_histogram = TT_TuneCUETP8M1_file.Get(var+'inclusive')
    TT_TuneCUETP8M1_inclusive_histogram.SetFillColor(kBlue)
    genweight = TT_TuneCUETP8M1_file.Get('evtweight').GetBinContent(3)
    TT_TuneCUETP8M1_inclusive_histogram.Scale(weights.get_weight(get_xsec('TTTuneCUETP8M113TeV_ext3_v1'), lumi, genweight))


    WJetsToLNu_file = TFile('./root/WJetsToLNuTuneCUETP8M113TeV_ext1_v1.root')
    WJetsToLNu_inclusive_histogram = WJetsToLNu_file.Get(var+'inclusive')
    WJetsToLNu_inclusive_histogram.SetFillColor(kRed+2)
    genweight =  WJetsToLNu_file.Get('evtweight').GetBinContent(3)
    WJetsToLNu_inclusive_histogram.Scale(weights.get_weight(get_xsec('WJetsToLNuTuneCUETP8M113TeV_ext1_v1'), lumi, genweight))


    SingleMuonRun2016BPromptReco_v2_v2_file = TFile('./root/SingleMuonRun2016BPromptReco_v2_v2.root')
    SingleMuonRun2016BPromptReco_v2_v2_inclusive_histogram = SingleMuonRun2016BPromptReco_v2_v2_file.Get(var+'inclusive')
    SingleMuonRun2016BPromptReco_v2_v2_inclusive_histogram.SetFillColor(kBlack)
    #genweight = SingleMuonRun2016BPromptReco_v2_v2_file.Get('evtweight').GetBinContent(3)
    #SingleMuonRun2016BPromptReco_v2_v2_inclusive_histogram.Scale(0.00017)

    '''
    wjetOSweight = weights.wjetsnorm();
    wjetSSweight = 1.;

    pics = {i : files[i].Get(var+'inc') for i in nazwy};

    pics['data'].SetMarkerStyle(20)
    pics['data'].SetMarkerSize(2)

    #print pics[1].Integral();
    #print files, pics, weights;
    for i in pics:
        if i == 'wjets':
            pics[i].Scale(wjetOSweight*weights.get(i))
        else:
            pics[i].Scale(weights.get(i))


    for k in pics.keys():
        pics[k].SetFillColor(colors[k])

    #QCD
    picsqcd = {i : files[i].Get(var+'qcd') for i in nazwy};
    
    for i in picsqcd:
        if i == 'wjets':
            picsqcd[i].Scale(1.06*wjetOSweight*weights.get(i))
        else:
            picsqcd[i].Scale(1.06*weights.get(i))

    
    qcd = picsqcd['data'];
    for i in picsqcd:
        if i == 'data':
            continue;
        if 'data' in i and i != 'data':
            qcd.Add(picsqcd[i])
        else:
            qcd.Add(picsqcd[i], -1)
    
    qcd.SetFillColor(colors['qcd'])
    '''

    hs = THStack("hs",var);
    #hs.Add(qcd)
    hs.Add(DYJetsToLL_inclusive_histogram)
    hs.Add(TT_TuneCUETP8M1_inclusive_histogram)
    hs.Add(WJetsToLNu_inclusive_histogram)


    c = TCanvas("_", "_", 1800, 2400);
    c1 = TPad("pad1", "The pad 80% of the height",0.0,0.3,1.0,1.0) #mozna dodac kolor jako ostatanie cyfra
    c2 = TPad("pad2", "The pad 20% of the height",0.0,0.05,1.0,0.25)
    c2.SetGrid();
    c1.Draw()
    c2.Draw()
    c1.cd()
    hs.Draw('hist')
    hs.GetHistogram().GetXaxis().SetTitle(var);
    hs.GetHistogram().GetYaxis().SetTitle('Events');
    hs.GetHistogram().GetYaxis().SetTitleOffset(1.2)

    SingleMuonRun2016BPromptReco_v2_v2_inclusive_histogram.SetMarkerStyle(20)
    SingleMuonRun2016BPromptReco_v2_v2_inclusive_histogram.SetMarkerSize(2)
    SingleMuonRun2016BPromptReco_v2_v2_inclusive_histogram.Draw('same p')

#    pics['data1'].Add(pics['data2'])
#    pics['data1'].Add(pics['data3'])
#    pics['data'].Sumw2();
#    pics['data'].Draw('same p')

    leg = TLegend(0.53,0.48,0.85,0.88)
    leg.SetFillStyle(0);
    leg.SetBorderSize(0);
    leg.SetFillColor(10);
    leg.SetTextSize(0.03);
#    leg.AddEntry(pics['data'], "observed: ", "pl")
#    leg.AddEntry(pics['dylow'], "Z#rightarrow ll (embedded, 5 < M < 50)", "f")
    leg.AddEntry(DYJetsToLL_inclusive_histogram, "Z#rightarrow ll (embedded, M > 50)", "f")
    leg.AddEntry(TT_TuneCUETP8M1_inclusive_histogram, 't#bar{t}', "f")
#    leg.AddEntry(pics['wjets'], "WJets", "f")
#    leg.AddEntry(qcd, "QCD", "f")
    leg.SetHeader("#splitline{CMS Preliminary #sqrt{s}=13 TeV}{%.3f fb^{-1} #tau_{#mu}#tau_{had}}" % (lumi*1e-3) );
    leg.Draw()


    #Dolny rysunek
    c2.cd()
    '''
    hista = pics['data'].Clone();
    hista.Add(qcd, -1)
    for i in pics:
        if 'data' in i:
            continue;
        hista.Add(pics[i],-1)
    hista.Divide(pics['data'])
    hista.SetTitle("")
    hista.SetLineStyle(10)
    hista.SetLineWidth(10)
    hista.GetYaxis().SetTitle(r"$\frac{data-MC}{data}$")
    #print hista.GetYaxis().GetTitleSize()
    hista.GetYaxis().SetTitleSize(0.15)
    hista.GetYaxis().SetTitleOffset(0.26)
    hista.GetYaxis().CenterTitle()
    hista.GetYaxis().SetLabelSize(0.08)
    hista.GetXaxis().SetLabelSize(0.08)
    
    maxYvalue = hista.GetMaximum()
    minYvalue = hista.GetMinimum()
    hista.SetMaximum(maxYvalue+ 0.05*abs(minYvalue-maxYvalue))
    hista.SetMinimum(minYvalue- 0.05*abs(minYvalue-maxYvalue))
    hista.Draw("hist")
    '''
    c.Update();
    c.Modified();
    c.Print('./plots/'+var+".png");


for i in variables.variables:
    rysunek(i)

