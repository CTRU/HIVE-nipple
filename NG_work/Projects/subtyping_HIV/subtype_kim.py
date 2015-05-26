#!/usr/bin/python
print "Hello world!"

import pprint
import sys

sys.path.append("/data/HIV/subtyping/pysam-0.8.1/build/lib.linux-x86_64-2.7/")
import pysam

MIN_ALIGN_LENGTH    = 70
MIN_ALIGNMENT_SCORE = 20

inbam = sys.argv[1]
outbam = inbam;
outbam = outbam.replace('.bam', '_no_lowQ.bam');
print "Writing to: " + outbam
#pysam.index(inbam)
infile  = pysam.AlignmentFile(inbam, "rb" )
outfile = pysam.AlignmentFile(outbam, "wb", template=infile)

# Reads in all reads, including the unaligned ones
for line in infile.fetch(until_eof=True):
    print line.cigar
    exit();
    alignment_length = line.query_alignment_end - line.query_alignment_start + 1
    alignment_score  = line.mapping_quality

    if ( alignment_length < MIN_ALIGN_LENGTH or alignment_score < MIN_ALIGNMENT_SCORE ):
        line.is_qcfail = 1;

    outfile.write( line );

infile.close( )
outfile.close( )
