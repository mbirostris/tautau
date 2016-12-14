from ROOT import *
import datafiles




def getgenweights(name):
    if name == 'data':
        return 1.
    f1 = TFile(datafiles.files[name])
    h1 = f1.Get('ininfo/evtweight')
    return h1.GetBinContent(3)


xsec = {
    'data' : 1.,
    'wjets' : 3*20508.9,
    'ttbar' : 831.76,
    'dy' : 3*2008.4,
    'dylow' : 71310.0
};

def get_weight(xsec, lumi, genweight):
    return xsec*lumi/genweight

def get(name):
    if name == 'data':
        return 1.
    return xsec[name]*lumi/getgenweights(name)


def wjetsnorm():
    nazwy = [k for k in datafiles.files.keys()]
    files = {i : TFile('./root/'+i+'.root') for i in nazwy}
    dataInt = 0; wjetsInt = 0;
    for i in files:
        #print i, files[i].Get('mumt'+'wscale').Integral()*get(i)
        if 'data' in i:
            dataInt += files[i].Get('mumt'+'wscale').Integral()*get(i);
        elif 'wjets' in i:
            wjetsInt +=  files[i].Get('mumt'+'wscale').Integral()*get(i);
        else:
            dataInt -= files[i].Get('mumt'+'wscale').Integral()*get(i);

    #print dataInt, wjetsInt, dataInt/wjetsInt;
    return dataInt/wjetsInt;


