#print "hello world!"

import sys
import re
import os

infile = sys.argv[1]
filename = ''

for i in os.listdir(infile):
    if not i.endswith(".bam.csv"):
        continue
    #print i
    isolate = re.sub(r'(.*).bam.csv', r'\1', i)
    #print isolate

    openinfile = open(i, 'rU')

    for line in openinfile:
        #print isolate
        newline = re.sub(r"K03455(.*)", r"%s\1" %isolate, line)
        print newline.replace("\t", ",")
