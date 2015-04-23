#!/usr/bin/python

#print "hello world"

#----------------------------------------------------------------------------------------

import re
import os
import sys

#----------------------------------------------------------------------------------------

nReads = ""
nMapped = ""
nDuplicate = ""
AvgIns = ""

nMapn = 0
nDup = 0

#----------------------------------------------------------------------------------------

print "Sample\tReads (n)\tReads Mapped (%)\tDuplicate Reads (%)\tAverage Insert Size"

#----------------------------------------------------------------------------------------

indir = sys.argv[1]


for file in os.listdir(indir):
	if not file.endswith(".bam.flagstat"):
		continue

	samplename = re.sub(r'(.*).bam.*', r"\1", file)

	infile = open(indir + file, "rU")

	for i, line in enumerate(infile):
		if i == 0:
			nline = line.split(" ")
			nReads = nline[0]

		if i == 2:
			line = line.strip("\n")
			nline = re.sub(r'(.*)\((.*):.*', r'\2', line)
			nMapped = nline

			nline = line.split(" ")
			nMapn = int(nline[0])

		if i == 1:
			nline = line.split(" ")
			nDup = nline[0].strip(" ")
			#NEEEDS FIXING TO MAKE %
			nDuplicate = int(nDup)/float(nReads)*100
	
	isizefile = open(indir + samplename + ".bam.isize" , "rU")
	
	for i, line in enumerate(isizefile):
		if i == 7:
			nline = line.split("\t")
			AvgIns = nline[0] 
	
	print "%s \t %s \t %s \t %.2f%% \t %s" % (samplename, nReads, nMapped, nDuplicate, AvgIns)