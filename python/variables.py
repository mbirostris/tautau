variables = ['mvis', 'mueta', 'taueta', 'mumt', 'taumt', 'mupt', 'taupt', 'npv', 'npu', 'njets30', 'metpt', 'HLT', 'PostSynchSelection', 'HLT_IsoMu22', 'HLT_IsoTkMu22', 'muphi', 'tauphi'];

def getname():
    for i in variables:
        yield i;

'''
def getrange_old(s):
    przedzialy = {
        'mvis': (30 ,0, 300),
        'mueta' : (24 ,-2.4, 2.4),
        'taueta' : ( 24 , -2.4 , 2.4),
        'mumt' : ( 40, 0, 160),
        'taumt' : ( 30, 0, 300),
        'mupt' : ( 10 ,0, 100),
        'taupt' : ( 10 , 0 , 100),
        'npv' : (50,0,50),
        'npu' : (50,0,50),
    }
    return przedzialy[s];
'''

def ls(lower, upper, length):
    return [lower + x*(upper-lower)/length for x in range(length+1)]

from array import array
def getrange(s):
    przedzialy = {
        'mvis': ls(0,300,30),# [0,60,65,70,75,80,85,90,95,100,105,110,400],
        'mueta' : ls(-2.4, 2.4, 24),
        'taueta' : ls( -2.4 , 2.4, 24),
        'mumt' : ls(0, 150, 50),
        'taumt' : ls( 0, 300, 30),
        'mupt' : ls( 0, 100, 50),
        'taupt' : ls(0,100, 50),# [30,35,40,45,50,55,300],
        'npv' : ls(0,50, 50),
        'npu' : ls(0,50, 50),
        'njets30' : ls(0,6, 6),
        'metpt' : ls(0,200, 20),
        'HLT' : ls(0,2,2),
        'PostSynchSelection' : ls(0,2,2),
        'HLT_IsoMu22' : ls(0,2,2),
        'HLT_IsoTkMu22' : ls(0,2,2),
        'muphi' : ls(-2.4, 2.4, 24),
        'tauphi' : ls(-2.4, 2.4, 24)
    }
    return array('d', przedzialy[s]);


def getvariable(mu, tau, pair, evt, jets):
    ret = {}
    ret['mvis'] = pair.m_vis()
    ret['mueta'] = mu.eta() 
    ret['taueta'] = tau.eta() 
    ret['mumt'] = mu.mt() 
    ret['taumt'] = tau.mt() 
    ret['mupt'] = mu.pt() 
    ret['taupt'] = tau.pt() 
    ret['npv'] = evt.npv() 
    ret['npu'] = evt.npu() 
    ret['njets30'] = len(jets)
    ret['metpt'] = pair.metpt()
    ret['HLT'] = pair.trigger('HLT')
    ret['PostSynchSelection'] = pair.PostSynchSelection()
    ret['HLT_IsoMu22'] = pair.trigger('HLT_IsoMu22')
    ret['HLT_IsoTkMu22'] = pair.trigger('HLT_IsoTkMu22')
    ret['muphi'] = mu.phi()
    ret['tauphi'] = tau.phi()
    return ret
