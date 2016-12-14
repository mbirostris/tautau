####################INCLUSIVE CUTS#######################
#cuts = ['inc', 'loose', 'qcd', 'nomt', 'nomtqcd', 'wscale', 'wscaleqcd']
#
#def getcut(mu, tau, pair, evt):
#    r = {}
#    for i in cuts:
#        r[i] = False
#
#    if not (tau.pt() > 20 and mu.pt()>18 and mu.iso() < 3.):
#        return r;
#
#    if mu.mt() < 45:
#        r['loose'] = True;
#
#    if(pair.diq() == -1 and mu.iso() < 0.1):
#        r['nomt'] = True;
#        if mu.mt() < 160.:
#            r['inc'] = True;
#        if mu.mt() > 70:
#            r['wscale'] = True;
#
#    if(pair.diq() == 1 and mu.iso() < 0.1):
#        r['nomtqcd'] = True;
#        if mu.mt() < 160.:
#            r['qcd'] = True;
#        if mu.mt() > 70:
#            r['wscaleqcd'] = True;
#    return r



####################INCLUSIVE CUTS v2#######################


class cut(object):

    def __init__(self, name, f):
        self.cut_name = name
        self.calculate = f

    def getname(self):
        return self.cut_name

    def setcuts(self, f):
        self.calculate = f



cuts = [

    cut('inclusive', f = lambda mu, tau, pair, evt : True if \
            tau.pt() > 30 and mu.pt()>20 and mu.iso() < 3. and mu.isTightMuon() and pair.diq() == -1 and mu.iso() < 0.1 and mu.mt() < 45.\
            else False  ),


    cut('qcd', f = lambda mu, tau, pair, evt : True if\
            tau.pt() > 30 and mu.pt()>20 and mu.iso() < 3. and  mu.isTightMuon() and pair.diq() == 1 and mu.iso() < 0.1 and mu.mt() < 45. \
            else False)

]
