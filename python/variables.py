variables = ['mvis', 'mueta', 'taueta', 'mumt', 'taumt', 'mupt', 'taupt', 'npv', 'npu'];

def getname():
    for i in variables:
        yield i;


def getrange(s):
    przedzialy = {
        'mvis': ( 30 ,0, 300),
        'mueta' : ( 24 ,-2.4, 2.4),
        'taueta' : ( 24 , -2.4 , 2.4),
        'mumt' : ( 40, 0, 160),
        'taumt' : ( 30, 0, 300),
        'mupt' : ( 10 ,0, 100),
        'taupt' : ( 10 , 0 , 100),
        'npv' : (50,0,50),
        'npu' : (50,0,50)
    }
    return przedzialy[s];


def getvariable(mu, tau, pair, evt):
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
    return ret

