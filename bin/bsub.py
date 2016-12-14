#!/usr/bin/env python
import os, re
import commands
import math, time
import sys

print 
print 'START'
print 
########   YOU ONLY NEED TO FILL THE AREA BELOW   #########
########   customization  area #########
NumberOfJobs= 1 # number of jobs to be submitted
interval = 1 # number files to be processed in a single job, take care to split your file so that you run on all files.
OutputFileNames = "outputFile" # base of the output file name, they will be saved in res directory
ScriptName = "analysis_file.py" # script to be used with cmsRun
FileList = "List.txt" # list with all the file directories
queue = "1nh" # give bsub queue -- 8nm (8 minutes), 1nh (1 hour), 8nh, 1nd (1day), 2nd, 1nw (1 week), 2nw 
########   customization end   #########

path = os.getcwd()
print
print 'do not worry about folder creation:'
os.system("rm -r tmp")
os.system("mkdir tmp")
os.system("mkdir res")
print

##### loop for creating and sending jobs #####
for x in range(1, int(NumberOfJobs)+1):
    ##### creates directory and file list for job #######
    os.system("mkdir tmp/"+str(x))
    os.chdir("tmp/"+str(x))
    os.system("sed '"+str(1+interval*(x-1))+","+str(interval*x)+"!d' ../../"+FileList+" > list.txt ")

    ##### creates jobs #######
    with open('job.sh', 'w') as fout:
        fout.write("#!/bin/sh\n")
        fout.write("echo\n")
        fout.write("echo\n")
        fout.write("echo 'START---------------'\n")
        fout.write("echo 'WORKDIR ' ${PWD}\n")
        fout.write("source /afs/cern.ch/cms/cmsset_default.sh\n")
        fout.write("cd "+str(path)+"\n")
        fout.write("cmsenv\n")
#        fout.write("cmsRun "+ScriptName+" outputFile='res/"+OutputFileNames+"_"+str(x)+".root' inputFiles_clear inputFiles_load='tmp/"+str(x)+"/list.txt'\n")
        fout.write("python "+ScriptName)
        fout.write("echo 'STOP---------------'\n")
        fout.write("echo\n")
        fout.write("echo\n")
    os.system("chmod 755 job.sh")

    ###### sends bjobs ######
    os.system("bsub -q "+queue+" -o logs job.sh")
    print "job nr " + str(x) + " submitted"

    os.chdir("../..")

print "your jobs:"
os.system("bjobs")
print 'END'
