

import os
class files(object):
    """class with list of fiels for sepatate background/data files"""
    def __init__(self, name, xsec, directory, max_files_number = 0, files = []):
        self.name = name
        self.files = [] 
        self.get_files_from_dir(directory, max_files_number, files)
        self.xsec = xsec;
        
    def add_files(self, *args):
        for i in args: self.files.append(i)

    def get_files(self):
        return self.files

    def get_name(self):
        return self.name

    def get_xsec(self):
        return self.xsec;

    def get_files_from_dir(self, directory, max_files_number = 0, files = []):
        for dirname, dirnames, filenames in os.walk(directory):
            if not files:
              if not max_files_number or 'Run' in self.name:
                for filename in filenames:
                    if '.root' in filename:
                        self.files.append("file:"+directory+filename);
              else:
                file_counter = 0
                for filename in filenames:
                  if file_counter >= max_files_number:
                    break;
                  if '.root' in filename:
                      self.files.append("file:"+directory+filename);
                      file_counter += 1;
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

def xsec_dict(i):
  if 'DYJets' in i and 'M50' in i: return 5765.4;
  if 'DYJets' in i and 'M10to50' in i: return 18610;
  if 'DY1Jets' in i: return 1012.5;
  if 'TT' in i: return 831.76;
  if 'GluGlu' in i: return 44.14 * 0.0627;
  if 'VBF' in i: return 3.935 * 0.0698;
  if 'WJets' in i: return 61526.7;
  if 'W1Jets' in i: return 9644.5;
  if 'ZZTo4L' in i: return 1.212;
  if 'VVTo2L2Nu' in i: return 11.95;
  if 'Run' in i: return 1;
  print "No xsec for sample ", i
  return 0;

import os


data_dir  = '/scratch/olszew/data/samples/'
max_files_number = 0 #0 for all
skip_dirs = ['crab_SingleMuonRun2016CPromptReco_v2_v20', 'crab_SingleMuonRun2016DPromptReco_v2_v20', 'crab_SingleMuonRun2016EPromptReco_v2_v20', 'crab_SingleMuonRun2016FPromptReco_v1_v20', 'crab_GluGluHToTauTauM12513TeV_v20', 'crab_DY1JetsToLLM50_v20']
#for i in xrange(len(skip_dirs)): skip_dirs[i] = data_dir+skip_dirs[i]
#sample_dirs = [i[0] for i in os.walk(data_dir)][1:]
sample_dirs = [os.path.join(data_dir,i) for i in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir,i)) and i not in skip_dirs]
#samples = [i.split('/')[-1].replace('crab_', '') for i in sample_dirs]
files_to_analysis = [files(i.split('/')[-1].replace('crab_', ''), xsec_dict(i.split('/')[-1]), i+'/results/', max_files_number) for i in sample_dirs]

