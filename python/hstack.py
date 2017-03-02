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



#lumi = (5396010449.512+2395577279.972+4244828925.70+2986294714.357+2540039267.750)*1e-6
lumi = 0.999*(5396010449.512)*1e-6


def getcolor(i):
    if 'Run' in i: return kWhite
    if 'WJets' in i: return kRed+2
    if 'W1Jets' in i: return kRed+2
    if 'DYJets' in i and 'M50' in i: return kOrange-4
    if 'DYJets' in i and 'M10' in i: return kOrange+8
    if 'DY1Jets' in i: return kOrange+12
    if 'TT' in i: return  kBlue
    if 'ZZ' in i: return  kGreen
    if 'QCD' in i: return kMagenta-10
    return kWhite

def get_xsec(name):
    for item in df.files_to_analysis:
        if item.get_name() == name: 
            return item.get_xsec()

def qcd(datafiles, var, cut, WJetsWeight = 1):
    data = main_data(datafiles, var, 'qcd'+cut)
    inclusive_histogram = {i : datafiles[i].Get(var+'qcd'+cut) for i in datafiles.keys() if 'Run' not in i};
    genweight = {i : datafiles[i].Get('evtweight').GetBinContent(3) for i in datafiles.keys()}
    for k, v in inclusive_histogram.items(): 
        v.Scale(weights.get(get_xsec(k), lumi, genweight[k]))
        if 'WJets' in k or 'W1Jets' in k:
            v.Scale(WJetsWeight)
    for k, v in inclusive_histogram.items():
        data.Add(v, -1)
    data.SetFillColor(getcolor('QCD'))
    data.Scale(1.06)
    return data


def main_backgrounds(datafiles, var, cut, WJetsWeight = 1):
    inclusive_histogram = {i : datafiles[i].Get(var+cut) for i in datafiles.keys() if 'Run' not in i};
    for k, v in inclusive_histogram.items(): v.SetFillColor(getcolor(k))
    genweight = {i : datafiles[i].Get('evtweight').GetBinContent(3) for i in datafiles.keys()}
    for i in datafiles.keys(): print i,0, datafiles[i].Get('evtweight').GetBinContent(0)
    for i in datafiles.keys(): print i,1, datafiles[i].Get('evtweight').GetBinContent(1)
    for i in datafiles.keys(): print i,2, datafiles[i].Get('evtweight').GetBinContent(2)
    for i in datafiles.keys(): print i,3, datafiles[i].Get('evtweight').GetBinContent(3)
    for k, v in inclusive_histogram.items(): 
        v.Scale(weights.get(get_xsec(k), lumi, genweight[k]))
        if "WJets" in k or 'W1Jets' in k:
            v.Scale(WJetsWeight)
    qcd_hist = qcd(datafiles, var, cut, WJetsWeight)
    hs = THStack("hs",var);
    hs.Add(qcd_hist)
    for k, v in inclusive_histogram.items():
        if 'TT' in k: hs.Add(v)
    inclusive_histogram_smooth = {i : datafiles[i].Get(var+'smooth'+cut) for i in datafiles.keys() if 'Run' not in i};
    for k, v in inclusive_histogram_smooth.items(): v.SetFillColor(getcolor(k))
    for k, v in inclusive_histogram_smooth.items():
        if 'WJet' in k:
            v.Scale(inclusive_histogram[k].Integral()/v.Integral())
            hs.Add(v)
    #for k, v in inclusive_histogram.items():
    #    if 'WJets' in k: hs.Add(v)
    for k, v in inclusive_histogram.items():
        if 'DY' in k: hs.Add(v)
    return hs


def main_data(datafiles, var, cut):
    inclusive_histogram = {i : datafiles[i].Get(var+cut) for i in datafiles.keys() if 'SingleMuonRun2016BPromptReco' in i};
    for k, v in inclusive_histogram.items(): v.SetFillColor(getcolor(k))
    for k, v in inclusive_histogram.items(): v.SetMarkerStyle(20)
    for k, v in inclusive_histogram.items(): v.SetMarkerSize(2)
    res = inclusive_histogram.itervalues().next()
    iterhist = iter(inclusive_histogram.keys())
    next(iterhist)
    for k in iterhist:
        res.Add(inclusive_histogram[k])
    #res.Sumw2();
    return res

def wjetsnorm(datafiles, cut):
    dataInt = 0; wjetsInt = 0;
    genweight = {i : datafiles[i].Get('evtweight').GetBinContent(3) for i in datafiles.keys()}
    for i in datafiles:
        #print i, datafiles[i].Get('mumt'+'wscale').Integral()
        if 'Run' in i:
            dataInt += datafiles[i].Get('mumt'+'wscale'+ cut).Integral();
        elif 'WJets' in i or 'W1Jets' in i:
            wjetsInt +=  datafiles[i].Get('mumt'+'wscale'+ cut).Integral()*weights.get(get_xsec(i), lumi, genweight[i]);
        else:
            dataInt -= datafiles[i].Get('mumt'+ 'wscale'+ cut).Integral()*weights.get(get_xsec(i), lumi, genweight[i]);
    dataInt -= qcd(datafiles, 'mumt', 'wscaleinclusive').Integral()
    print dataInt, wjetsInt, dataInt/wjetsInt;
    return dataInt/wjetsInt;

datafiles = {i.replace('.root', '') :  TFile('./root/'+i) for i in  [i[2] for i in os.walk('./root/')][0] if '.root' in i}
a_cut = 'inclusive' #'0jet_low'
WJetsWeight = wjetsnorm(datafiles, a_cut);
#print WJetsWeight
#WJetsWeight = 1

def getlegendentries(i):
    if 'Run' in i: return 'Data'
    if 'WJets' in i: return kRed+2
    if 'W1Jets' in i: return kRed+2
    if 'DYJets' in i and 'M50' in i: return kOrange-4
    if 'DYJets' in i and 'M10' in i: return kOrange+8
    if 'DY1Jets' in i: return kOrange+12
    if 'TT' in i: return  kBlue
    if 'ZZ' in i: return  kGreen
    if 'QCD' in i: return kMagenta-10
    return kWhite


from os import walk
def rysunek(var):

    hs = main_backgrounds(datafiles, var, a_cut, WJetsWeight)
    data = main_data(datafiles, var, a_cut)

    c = TCanvas("_", "_", 1800, 2400);
    c1 = TPad("pad1", "The pad 80% of the height",0.0,0.3,1.0,1.0) #mozna dodac kolor jako ostatanie cyfra
    c2 = TPad("pad2", "The pad 20% of the height",0.0,0.05,1.0,0.25)
    #c1 = TPad("pad1", "The pad 90% of the height",0.0,0.0,1.0,1.0) #mozna dodac kolor jako ostatanie cyfra
    #c2 = TPad("pad2", "The pad 10% of the height",0.0,0.0,1.0,0.0)
    c2.SetGrid();
    c1.Draw()
    c2.Draw()
    c1.cd()
    hs.Draw('hist')
    hs.GetHistogram().GetXaxis().SetTitle(var);
    hs.GetHistogram().GetYaxis().SetTitle('Events');
    hs.GetHistogram().GetYaxis().SetTitleOffset(1.2)

    data.Draw('same p')
    leg = TLegend(0.75,0.75,0.96,0.96)
    leg.SetFillStyle(0);
    leg.SetBorderSize(0);
    leg.SetFillColor(10);
    leg.SetTextSize(0.02);
    for var_name in (datafiles.keys()):
        if 'Run' in var_name or 'VBF' in var_name: continue
        leg.AddEntry(datafiles[var_name].Get(var+a_cut), var_name[:5],"f")
#    leg.AddEntry(pics['data'], "observed: ", "pl")
#    leg.AddEntry(pics['dylow'], "Z#rightarrow ll (embedded, 5 < M < 50)", "f")
    
    #leg.AddEntry(DYJetsToLL_inclusive_histogram, "Z#rightarrow ll (embedded, M > 50)", "f")
    #leg.AddEntry(TT_TuneCUETP8M1_inclusive_histogram, 't#bar{t}', "f")
#    leg.AddEntry(pics['wjets'], "WJets", "f")
#    leg.AddEntry(qcd, "QCD", "f")
    leg.SetHeader("#splitline{CMS Preliminary #sqrt{s}=13 TeV}{%.3f fb^{-1} #tau_{#mu}#tau_{had}}" % (lumi*1e-3) );
    leg.Draw()

    #c1.BuildLegend()
    #Dolny rysunek
    c2.cd()


    #'''
    hista = data.Clone(); hsc = hs
    for  ii in hsc.GetHists():
        hista.Add(ii, -1)
    '''
    for i in pics:
        if 'data' in i:
            continue;
        hista.Add(pics[i],-1)
    '''
    hista.Divide(data)
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
    #'''
    c.Update();
    c.Modified();
    c.Print('./plots/'+var+".png");
    del hista, data, hs, c, maxYvalue, minYvalue, c1, c2


for i in variables.variables:
    rysunek(i)

