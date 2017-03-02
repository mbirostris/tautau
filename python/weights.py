from ROOT import *
import datafiles



def get(xsec, lumi, genweight):
    return xsec*lumi/genweight

def mutotaufakerateSF(eta):
	eta = abs(eta)
	if eta < 0.4:
		return 1.5
	elif eta < 0.8:
		return 1.4
	elif eta < 1.2:
		return 1.21
	elif eta < 1.7:
		return 2.6
	elif eta < 2.3:
		return 2.1
	return 1;

def etotaufakerateSF(eta):
	eta = abs(eta)
	if eta < 1.460:
		return 1.02
	elif eta > 1.558:
		return 1.11
	return 1

