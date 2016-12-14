#!/bin/sh

source /afs/cern.ch/cms/cmsset_default.sh
cd /afs/cern.ch/work/m/molszews/CMSSW/tautau/WarsawAnalysis/CMSSW_7_6_3/src/SYNCH_NTUPLES/python
cmsenv
time python abrakadabra.py

