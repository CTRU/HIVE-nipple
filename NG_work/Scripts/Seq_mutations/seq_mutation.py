#!/users/Nick/anaconda/bin/python

import re
from Bio.Alphabet import generic_dna, generic_protein
from Bio import SeqIO
import sys
import csv

file = str(sys.argv[1])

def compare_seqs( seq1, seq2 ):

  diff_positions = []

  for i in range(0, len( seq1 )):
    if ( seq1[ i ] != seq2[ i ]):
      difference = "%s-%s [%d]" %( seq1[i], seq2[i], (i + 1))
      diff_positions.append( difference )
    #else:
       #similar += 1

  return ",".join( diff_positions )

reference_sequence = ""
reference_name     = ""

records = []

for record in SeqIO.parse(open(file, 'rU'), 'fasta', generic_protein):
    record_id = re.sub(r'\d+_(\d+_\d\#\d+)_\d+', r'\1', record.id)

    if ( not reference_sequence ):
      reference_sequence = record.seq
      reference_name     = record_id
      #continue
    records.append([reference_name, record_id, compare_seqs(reference_sequence, record.seq)])

print records

outfile = csv.writer(open(file + "_mutations.csv","w"))

outfile.writerows(records)


exit()
