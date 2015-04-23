#!/usr/bin/python
print "Hello world!"

#------- IMPORTING MODULES -------

import pprint
import sys
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

# Reads in all reads, including the unaligned ones
for line in infile.fetch(until_eof=True):

    alignment_length = line.query_alignment_end - line.query_alignment_start + 1
    alignment_score  = line.mapping_quality

    if ( alignment_length < MIN_ALIGN_LENGTH or alignment_score < MIN_ALIGNMENT_SCORE ):
        line.is_qcfail = 1

    # QC fail if mate is unmapped or mapped to a different reference..... 
    #   tried "if line.next_reference_id != line.reference_id" see documentation here instead of "mate = infile.mate(line)".....
    #	    but as before documentation is ambiguous at best and gave very low reads in hash at end (talking highest reads = 15!!)
   	
    mate = ''

    if line.mate_is_unmapped == True: 
   		line.is_qcfail = 1
   		continue

    #else:
      #mate = infile.mate(line)
    
    if line.next_reference_id != line.reference_id:
		  line.is_qcfail = 1
   
    # counting how many reads are mapped to each reference id in bamfile. 

    if line.is_qcfail == 1:
      continue 

    else:
      if line.is_qcfail == 0:
        if line.reference_id not in subtype_scores.keys():
          subtype_scores[line.reference_id] = 1
        else:
          if line.reference_id in subtype_scores.keys():
            subtype_scores[line.reference_id] += 1

# printing the hash and getting the ID of the best ref. 

print subtype_scores

sys.exit()

best_ref = max(subtype_scores, key=subtype_scores.get)    

# thought I would seperate this out as it makes it easier for me to write all reads which have the "best" ref id to the new bamfile even if they are QC fail

for line in infile.fetch(until_eof=true):
	if line.reference_id != best_ref:
		continue 

	else:
		if line.reference_id == best_ref:
			outfile.write( line )



infile.close( )
outfile.close( )
