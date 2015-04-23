#print "hello world!"

import sys
import re
import os

infile = sys.argv[1]
filename = ''

for i in os.listdir(infile):
    if not i.endswith("_depth.csv"):
        continue
    #print i
    isolate = re.sub(r'(.*)_depth.csv', r'\1', i)
    #print isolate

    openinfile = open(i, 'rU')

    for line in openinfile:
        line = line.replace("\t", ",")
        print isolate, ",", line
