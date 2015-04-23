#print "hello world!"

#By Kim Brugger and Nick Gleadall
#Please e-mail nick.gleadall@googlemail.com if needed! 

#------------------------------------------------------------------
#Defining the function
#------------------------------------------------------------------

def best_pos( sequence, primer):

    primer.upper()
    sequence.upper()


    best_score = 0
    position = []

    for i in range(0, len(sequence) - len(primer)): # -1 here to avoid going over length of i
        local_score = 0
        for j in range(0, len(primer)):
            if sequence[i + j] == primer[j]: #Anchors I and then loops J over I
                local_score += 1 # Append local score

        #print best_score
        if (local_score > best_score):
            position = []
            position.append( str(i) )
            best_score = local_score
        elif ( local_score == best_score): #Appends best local score to global best score.
            pass
            position.append(str(i))

#    print "score:" + str(best_score) + ",".join(str(position))
    return (best_score, position)

#------------------------------------------------------------------
#Looping through inputs
#------------------------------------------------------------------
import sys
import re
import pprint




def readin_fasta(file):

    infile = open(file, 'rU')

    res = []

    seq_name = ""
    seq      = ""

    for line in infile:

        line = line.strip("\n")


        if (  re.match(r'\>', line)):
            line = re.sub(r'\>', "", line)
            if ( seq_name ):
                res.append( [seq_name, seq] )
                #res[ seq_name ] = seq

            seq = ""
            seq_name = line
        else:
            seq += line

    if ( seq_name ):
        res.append( [seq_name, seq] )

#    pprint.pprint( res )

    return res
# ----------- Reversing Primers -------------

def seq_reverse(sequence):

    rev_sequence = []

    dna_dict = {'A' : 'T', 'T' : 'A', 'C' : 'G', 'G' : 'C'}

    for base in sequence:
        if base in dna_dict.keys():
            rev_sequence.append(dna_dict[base])
        else:
            rev_sequence.append(base)

    "".join(rev_sequence)

    trev_sequence = rev_sequence[::-1]


    return "".join(trev_sequence)

# ----------- MAIN LOOP --------------


references = readin_fasta(sys.argv[ 1 ])
primers    = readin_fasta(sys.argv[ 2 ])

scores = dict()

reference_names = dict()

for primer in primers:
    [primer_name, primer_seq] = primer
    scores[ primer_name ] = dict()
    primer_seq_rev = seq_reverse( primer_seq )

    for reference in references:
        [ref_name, ref_seq] = reference

        reference_names[ ref_name ] = 1

        (score, pos) = best_pos(ref_seq, primer_seq)
        (score_rev, pos_rev) = best_pos(ref_seq, primer_seq_rev)

        if ( score_rev > score):
            scores[ primer_name ][ ref_name ] = [len(primer_seq), score_rev, pos_rev, "r"]
        else:
            scores[ primer_name ][ ref_name ] = [len(primer_seq), score, pos, "f"]



print "\t".join([""]+ sorted(reference_names.keys()))


for primer_name in sorted(scores):
    line = []

    for reference in sorted( reference_names.keys()):

        (primer_len, score, pos, strand) = scores[ primer_name ][ reference ]
        line.append( "%d/%d:%d/%d %s [%s]" % (score,primer_len, score, primer_len, strand, ",".join(pos)))

    print "\t".join([ primer_name ] + line)
