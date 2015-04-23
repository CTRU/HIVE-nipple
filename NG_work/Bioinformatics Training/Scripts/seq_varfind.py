#!/users/Nick/anaconda/bin/python

import re
from Bio.Alphabet import generic_dna, generic_protein
from Bio import SeqIO
import sys
import pprint
import csv

pp = pprint.PrettyPrinter(width=1)

file = str(sys.argv[1])


def compare_seqs( seq1, seq2 ):

  diff_positions = []


  for i in range(0, len( seq1 )):
    if ( seq1[ i ] != seq2[ i ]):
      difference = "%s-%s [%d]" %( seq1[i], seq2[i], (i + 1))
      diff_positions.append( difference )


  return ",".join( diff_positions )

# -----------------------------------------------------------------------------------------------

reference_sequence = ""
reference_name     = ""
diff_found = []
for record in SeqIO.parse(open(file, 'rU'), 'fasta', generic_protein):
    record_id = re.sub(r'\d+_(\d+_\d\#\d+)_\d+', r'\1', record.id)

    difference_count = []
    same_count = 0

    if ( not reference_sequence ):
      reference_sequence = record.seq
      reference_name     = record_id
    #print ",".join([reference_name, record_id, compare_seqs(reference_sequence, record.seq)])
    diff_found.append(compare_seqs(reference_sequence, record.seq))
#      else :
#      difference_count.append("Same_as_reference") !!!! TRYING TO APPEND TO LIST TO COUNT SAME SEQS !!!!!

print diff_found # prints the list generated!
# ---------------------------------------------------------------------------------------------

mutdic = {}

for mutation in diff_found :
  if mutation in mutdic :
    mutdic[mutation] += 1

  else :
    mutdic[mutation] = 1

# ---------------------------------------------------------------------------------------------

outfile = csv.writer(open(file + "_mutation_count.csv", "w"))
for key, value in mutdic.items():
  outfile.writerow([key,value])

exit()
