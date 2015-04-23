#!/usr/bin/python
print "Hello world!"

#------- IMPORTING MODULES -------

import pprint
import sys
sys.path.append("/data/HIV/subtyping/pysam-0.8.1/build/lib.linux-x86_64-2.7/")
import pysam

#------- SETTING GLOBALS -------

MIN_ALIGN_LENGTH    = 70
MIN_ALIGNMENT_SCORE = 20

subtype_scores = {}


#------- DATA I/O SETUP -------

inbam = sys.argv[1]
outbam = inbam;
outbam = outbam.replace('.bam', '_no_lowQ.bam');
print "Writing to: " + outbam

#pysam.index(inbam)
infile  = pysam.AlignmentFile(inbam, "rb" )
outfile = pysam.AlignmentFile(outbam, "wb", template=infile)

exit_counter = 60000

# Reads in all reads, including the unaligned ones
for line in infile.fetch(until_eof=True):

    alignment_length = line.query_alignment_end - line.query_alignment_start + 1
    alignment_score  = line.mapping_quality

    if ( alignment_length < MIN_ALIGN_LENGTH or alignment_score < MIN_ALIGNMENT_SCORE ):
        line.is_qcfail = 1

    # QC fail if mate is unmapped or mapped to a different reference..... 
    #   tried "if line.next_reference_id != line.reference_id" see documentation here instead of "mate = infile.mate(line)".....
    #	    but as before documentation is ambiguous at best and gave very low reads in hash at end (talking highest reads = 15!!)

#    print "\t".join([str(line.reference_id), str(line.next_reference_id)])

   	
    if ( not line.mate_is_unmapped and  line.next_reference_id != line.reference_id):
        line.is_qcfail = 1


    outfile.write( line )
   
    # counting how many reads are mapped to each reference id in bamfile. 

    if line.is_qcfail == 1:
      continue 

    else:
        if line.reference_id not in subtype_scores.keys():
          subtype_scores[line.reference_id] = 1
        else:
          subtype_scores[line.reference_id] += 1


    if ( exit_counter == 0):
        break
    exit_counter -= 1


# printing the hash and getting the ID of the best ref. 

#print subtype_scores
# Print nicely, ref-name & count sorted by counts.
for tid in subtype_scores:
    print "\t".join([infile.getrname( tid ), str( subtype_scores[ tid ])])



infile.close( )
outfile.close( )
