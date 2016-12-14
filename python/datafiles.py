

import os
class files(object):
    """class with list of fiels for sepatate background/data files"""
    def __init__(self, name, xsec, directory, files = []):
        self.name = name
        self.files = [] 
        self.get_files_from_dir(directory, files)
        self.xsec = xsec;
        
    def add_files(self, *args):
        for i in args: self.files.append(i)

    def get_files(self):
        return self.files

    def get_name(self):
        return self.name

    def get_xsec(self):
        return self.xsec;

    def get_files_from_dir(self, directory, files = []):
        for dirname, dirnames, filenames in os.walk(directory):
            if not files:
                for filename in filenames:
                    if '.root' in filename:
                        self.files.append("file:"+directory+filename);
            else:
                for filename in filenames:
                    if any(filename in s for s in files):
                        self.files.append("file:"+directory+filename);



###############################################################################
# define samples to be processed. You pass name and folder with sample files,
#for more read class def.
###############################################################################

#Example how to precess only some files
#DYJetsToLL = files('DYJetsToLL', 5454.8, '/afs/cern.ch/work/m/molszews/CMSSW/Data/ntuple/01/crab_DYJetsToLL_M_50_TuneCUETP8M1_13TeV_madgraphMLM_pythia8_v1/results/', ['ntuple_11.root', 'ntuple_12.root'])

files_to_analysis = [

    files('DYJetsToLL', 5765.4, '/scratch/olszew/data/DYJetsToLLM50_v3/', []),
    files('TTTuneCUETP8M113TeV_ext3_v1', 831.76, '/scratch/olszew/data/TTTuneCUETP8M113TeV_ext3_v1/', []),
    files('GluGluHToTauTau', 44.14 * 0.0627, '/scratch/olszew/data/GluGluHToTauTauM12513TeV_v1/', []),
    files('VBFHToTauTauM12513TeV_v1', 3.935 * 0.0698, '/scratch/olszew/data/VBFHToTauTauM12513TeV_v1/', []),
    files('WJetsToLNuTuneCUETP8M113TeV_ext1_v1', 61526.7, '/scratch/olszew/data/WJetsToLNuTuneCUETP8M113TeV_ext1_v1/', []),
    files('MuonEGRun2016BPromptReco_v2_v2', 1, '/scratch/olszew/data/MuonEGRun2016BPromptReco_v2_v2/', []),
    files('SingleElectronRun2016BPromptReco_v2_v2', 1, '/scratch/olszew/data/SingleElectronRun2016BPromptReco_v2_v2/', []),
    files('SingleMuonRun2016BPromptReco_v2_v2', 1, '/scratch/olszew/data/SingleMuonRun2016BPromptReco_v2_v2/', [])
]