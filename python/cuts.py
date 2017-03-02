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

#pt_tau > 20 && pt_tau < 50 && njets==0 && mt < 50 

def gettriggger(pair):
    triggers = ['HLT_IsoMu18_v3', 'HLT_IsoMu20_v4', 'HLT_IsoMu22_v3', 'HLT_IsoMu22_eta2p1_v2']

cuts = [
    
    #inclusive
    cut('inclusive', f = lambda mu, tau, pair, evt, jets : True if \
            pair.diq() == -1 and mu.mt() < 50 and pair.PostSynchSelection() and pair.trigger('HLT_IsoMu22') and mu.iso() < 0.1 and  tau.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits") and mu.pt() > 23 and tau.pt() > 30\
            else False  ),

    cut('qcdinclusive', f = lambda mu, tau, pair, evt, jets : True if\
            pair.diq() == 1 and mu.mt() < 50  and pair.PostSynchSelection() and pair.trigger('HLT_IsoMu22') and mu.iso() < 0.1 and  tau.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits") and mu.pt() > 23 and tau.pt() > 30 \
            else False),

    cut('wscaleinclusive', f = lambda mu, tau, pair, evt, jets : True if\
            pair.diq() == -1 and mu.mt() > 80 and pair.PostSynchSelection() and pair.trigger('HLT_IsoMu22') and mu.iso() < 0.1 and  tau.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits") and mu.pt() > 23 and tau.pt() > 30\
            else False),

    cut('qcdwscaleinclusive', f = lambda mu, tau, pair, evt, jets : True if\
            pair.diq() == 1 and mu.mt() > 80 and pair.PostSynchSelection() and pair.trigger('HLT_IsoMu22') and mu.iso() < 0.1 and  tau.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits") and mu.pt() > 23 and tau.pt() > 30\
            else False),

    cut('smoothinclusive', f = lambda mu, tau, pair, evt, jets : True if \
            pair.diq() == -1 and mu.mt() < 50  and pair.PostSynchSelection() and pair.trigger('HLT_IsoMu22') and mu.pt() > 23 and tau.pt() > 30\
            else False  ),
#mt < 50 && (njets==1 or (njets==2 && mjj < 500)) && ((pt_tau > 30 && pt_tau < 40) or (pt_tau > 40 && Higgs_pt < 140)) 

]

cuts_spare = [
    #inclusive_iso
    cut('inclusive_iso', f = lambda mu, tau, pair, evt, jets : True if \
            pair.diq() == -1 and mu.mt() < 50 and mu.iso() < 0.1 and tau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")\
            else False  ),


    cut('qcdinclusive_iso', f = lambda mu, tau, pair, evt, jets : True if\
            pair.diq() == 1 and mu.mt() < 50 and mu.iso() < 0.1 and tau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")\
            else False),

    cut('wscaleinclusive_iso', f = lambda mu, tau, pair, evt, jets : True if\
            pair.diq() == -1 and mu.mt() > 80 and mu.iso() < 0.1 and tau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")\
            else False),

    cut('qcdwscaleinclusive_iso', f = lambda mu, tau, pair, evt, jets : True if\
            pair.diq() == 1 and mu.mt() > 80 and mu.iso() < 0.1 and tau.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")\
            else False),

    #0_jet_low
    cut('0jet_low', f = lambda mu, tau, pair, evt, jets : True if \
            tau.pt() > 20 and tau.pt() < 50 and len(jets) == 0 and mu.mt() < 50 and pair.diq() == -1 \
            else False ),


    cut('qcd0jet_low', f = lambda mu, tau, pair, evt, jets : True if \
            tau.pt() > 20 and tau.pt() < 50 and len(jets) == 0 and mu.mt() < 50 and pair.diq() == 1 \
            else False ),


    cut('wscale0jet_low', f = lambda mu, tau, pair, evt, jets : True if \
            tau.pt() > 20 and tau.pt() < 50 and len(jets) == 0 and mu.mt() > 80 and pair.diq() == -1 \
            else False ),


    cut('qcdwscale0jet_low', f = lambda mu, tau, pair, evt, jets : True if \
            tau.pt() > 20 and tau.pt() < 50 and len(jets) == 0 and mu.mt() > 80 and pair.diq() == 1 \
            else False ),



    #0_jet_high
    cut('0jet_high', f = lambda mu, tau, pair, evt, jets : True if \
            tau.pt() > 50 and len(jets) == 0 and mu.mt() < 50 and pair.diq() == -1 \
            else False ),


    cut('qcd0jet_high', f = lambda mu, tau, pair, evt, jets : True if \
            tau.pt() > 50 and len(jets) == 0 and mu.mt() < 50 and pair.diq() == 1 \
            else False ),


    cut('wscale0jet_high', f = lambda mu, tau, pair, evt, jets : True if \
            tau.pt() > 50 and len(jets) == 0 and mu.mt() > 80 and pair.diq() == -1 \
            else False ),


    cut('qcdwscale0jet_high', f = lambda mu, tau, pair, evt, jets : True if \
            tau.pt() > 50 and len(jets) == 0 and mu.mt() > 80 and pair.diq() == 1 \
            else False ),


]