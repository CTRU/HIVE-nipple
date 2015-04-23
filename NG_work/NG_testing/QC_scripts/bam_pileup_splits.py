#!/usr/bin/python
import sys
import getopt
import pprint
pp = pprint.PrettyPrinter(indent=4)

sys.path.append("/software/lib/python2.7/site-packages/pysam-0.7.5-py2.7-linux-x86_64.egg")

import re

import pysam


bamfile = sys.argv[1]
samfile = pysam.Samfile( bamfile, "rb" )
#samfile = pysam.Samfile( "../miseq/A280050.bam", "rb" )

#samfile = pysam.Samfile( "/data/CP/CP0007/C060004.bam", "rb" )

fasta_ref = pysam.Fastafile("/refs/HIV/K03455.fasta");


MIN_ALLELE_PERC =  25
MIN_COVERAGE    = 300
MIN_FROM_END    =  10


#############################
def First_Char(base):
    """Return only first character of a multi-char base"""
    
    if(base):
        
            bs = re.search("^(.)", base)
            if(bs):
                b = bs.group(1)
    return(b)



#############################
def Find_IUPAC(fb,sb,tb = ''):
    """Return an IUPAC code given a first and second base"""


#    print "\t".join([fb,sb,tb])


    max_length =  max(len(fb), len(sb), len(tb))

    IUPAC_Codes = {'A': 'A',
                   'C': 'C',
                   'G': 'G',
                   'T': 'T',
                   'AT': 'W',
                   'CG': 'S',
                   'AC': 'M',
                   'GT': 'K',
                   'AG': 'R',
                   'CT': 'Y',
                   'CGT': 'B',
                   'AGT': 'D', 
                   'ACT': 'H',
                   'ACG': 'V'
                   }

    IUPAC_consensus = ""

    for i in range(0, max_length):
        bases = [];

#        print str(len(fb)) , " >= " ,str(i)

        if (len(fb) > i and fb[i] != '-'):
            bases.append( fb[i] )

        if (len(sb) > i and sb[i] != '-'):
            bases.append( sb[i] )

        if (len(tb) > i and tb[i] != '-'):
            bases.append( tb[i] )

        fst = ''.join( sorted(set(bases)))

        if ( fst != ""):
            IUPAC_consensus += IUPAC_Codes[ fst ]


#    print IUPAC_consensus

    return(IUPAC_consensus)


#############################
def update_counts(base_counts, base):

    if (base not in base_counts):
        base_counts[ base ] = dict()

        base_counts[ base ][ 'count' ] = 0

    base_counts[ base ][ 'count' ] += 1

    return base_counts;



iter = samfile.pileup(max_depth=80000 )
#iter = samfile.pileup("K03455", 3679, 3680, max_depth=80000)
#iter = samfile.pileup("NC_001802", 1621, 1621 + 10, max_depth=80000)

consensus = []

hyphenlen = 0 ###


print "\t".join(["Position", "total", "A","C","G","T"])


for x in iter:


#    if ( x.pos < 2735 or x.pos >2750 ):
#        continue

#    if ( x.pos < 2746 or x.pos >2746 ):
#        continue


#############################
###Fix indel###
    
    if(hyphenlen):
        hyphenlen -= hyphenlen
        continue

#############################


#    if (x.pos != 3678):
#        continue

    
    passed_bases = 0

    base_counts = dict()
    skipped_reads = 0


#    print 'coverage at base %s = %s' %(x.pos , x.n)

    for read in x.pileups:
        if (read.alignment.is_unmapped or read.alignment.is_duplicate or read.is_del):
            continue


        if ( read.query_position <= MIN_FROM_END ):
#            print "Skipped var as to close to the end...";
            skipped_reads += 1
            continue

        if ( read.alignment.alen - read.query_position + read.indel  <= MIN_FROM_END ):
#            print "Skipped var as to close to the end...";
            skipped_reads += 1
            continue


        if ( read.query_position + read.indel + 3 > read.alignment.alen):
            continue

 
        if ( read.indel > 0):
            insertion = read.alignment.seq[ read.query_position:read.query_position+ read.indel + 1]
            base_counts = update_counts(base_counts, insertion)
             
             

        elif ( read.indel < 0):
            deletion = ''
            deletion = read.alignment.seq[ read.query_position] + "-" * abs(read.indel)
            deletion = deletion.lower()
            deletion = deletion.title()

            base_counts = update_counts(base_counts, deletion)
            
            
        else:
            alt_base = read.alignment.seq[ read.query_position];
            base_counts = update_counts(base_counts, alt_base)


#    pp.pprint( base_counts )



    #continue



    total_bases = 0

    for base in ('A', 'C','G','T'):

        if (base  in base_counts):
            total_bases += base_counts[ base ][ 'count']


    ref_base = fasta_ref.fetch(str(samfile.getrname(x.tid)), x.pos, x.pos+1)


#    print "%d --> %d " % ( total_bases, skipped_reads )

    base_splits = [str(x.pos + 1), ref_base, str(total_bases)]

    for base in ('A', 'C','G','T'):

        if (base not in base_counts):
            base_splits.append('0')
            
        else:
            base_splits.append( "%.2f" % (float(base_counts[ base ][ 'count'])/float(total_bases)*100.0))


    print "\t".join(base_splits)




samfile.close()

