#!/usr/bin/python

print "Hello World!"

import re

outfile = open("outfile.fasta", "w")

for line in open("test1.aln", 'rU').readlines():
    line.strip("\n")
    line = re.sub(r'>\d+_(\d+_\d\#\d+)_\d+', r'>\1', line)
    outfile.write(line)

close(outfile)
exit()
