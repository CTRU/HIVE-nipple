#!/usr/bin/python
import sys
import getopt
import pprint
pp = pprint.PrettyPrinter(indent=4)

sys.path.append("/software/lib/python2.7/site-packages/pysam-0.7.1-py2.7-linux-x86_64.egg/")

import re

import pysam


bamfile = sys.argv[1]
samfile = pysam.Samfile( bamfile, "rb" )
#samfile = pysam.Samfile( "../miseq/A280050.bam", "rb" )

#samfile = pysam.Samfile( "/data/CP/CP0007/C060004.bam", "rb" )

fasta_ref = None
reference = ""

gene_list = []




if ( re.match(r'C06', bamfile)):
    gene_list = [['Pol', 2253, 2546, 5],
                 ['RT', 2550, 4227, 0, 320],
                 ['Int',4233, 5100, 1]]


    fasta_ref = pysam.Fastafile("/refs/HIV/K03455.fasta");
    reference = "K03455";

elif ( re.match(r'C11', bamfile)):
    gene_list = [['TK', 1, 1128]]
    fasta_ref = pysam.Fastafile("/refs/HSV/TK.fasta");
    reference = "TK";
elif ( re.match(r'C19', bamfile)):
    gene_list = [['Kinase', 140484, 142405], 
                 ['Pol', 80631,76906]]
    fasta_ref = pysam.Fastafile('/refs/CMV/CMV_AD169.fasta')
    reference = "CMV_AD169"




MIN_PERCENTAGE = 1

def codon2AA(codon):

    codon = codon.upper()

    codon2AA = { 'TTT': 'F', 'TTC': 'F',
                 'TTA': 'L', 'TTG': 'L',
                 'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
                 'TAT': 'Y', 'TAC': 'Y', 
                 'TAA': '*', 'TAG': '*', 'TGA': '*',
                 'TGT': 'C', 'TGC': 'C',
                 'TGG': 'W',
                 'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
                 'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
                 'CAT': 'H', 'CAC': 'H',
                 'CAA': 'Q', 'CAG': 'Q',
                 'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
                 'ATT': 'I', 'ATC': 'I', 'ATA': 'I',
                 'ATG': 'M',
                 'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
                 'AAT': 'N', 'AAC': 'N',
                 'AAA': 'K', 'AAG': 'K',
                 'AGT': 'S', 'AGC': 'S',
                 'AGA': 'R', 'AGG': 'R',
                 'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
                 'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
                 'GAT': 'D', 'GAC': 'D',
                 'GAA': 'E', 'GAG': 'E',
                 'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G' }
                 
    if (len(codon) > 3):
        return "i"

    if (len(codon) < 3):
        return "d"


    if ( codon not in codon2AA ):
#        print "Cannot tranlate " + codon + " codon to an AA";
        return "X"

    return codon2AA[ codon ] 



def revDNA( string ):
    rev_bases = { 'A': 'T', 
                  'a': 'T', 
                  'C': 'G',
                  'c': 'G',
                  'G': 'C',
                  'g': 'C',
                  'T': 'A',
                  'T': 'A',
                  '-': '-'}

#    print "STRING FOR REVDNA:: " + string
    rev_str = len(string)*[None]
    for i in range(0, len(string)):
        rev_str[ len(string) - i - 1] =  rev_bases[ string[ i ]]

    return "".join( rev_str )



def codon_count2AA_count( codon_counts, minus_strand ):
    AA_counts = dict();

    
    total_AAs = 0

    for codon in (codon_counts.keys()):

        AA = codon2AA( codon )

        if ( minus_strand):
#            print "normal codon: " + codon
            rev_codon = revDNA( codon )
#            print "reverse codon: " + rev_codon
            AA = codon2AA( rev_codon )


        if ( AA == "X"):
            continue

        if ( AA not in AA_counts) :
            AA_counts[ AA ] = 0;

        AA_counts[ AA ] += codon_counts[ codon ];
        total_AAs += codon_counts[ codon ]


#    pp.pprint( AA_counts )

    AA_percents = dict()

    for AA in (AA_counts.keys()):
        AA_percent = float(100)*float(AA_counts[ AA ])/float( total_AAs )
        if ( AA_percent >= MIN_PERCENTAGE ):
            AA_percents[ AA ] = "%.2f" % ( AA_percent )

#    pp.pprint( AA_percents )

    return AA_percents

#############################
def update_counts(codon_counts, codon):

    if (codon not in codon_counts):
        codon_counts[ codon ] = 0

    codon_counts[ codon ] += 1

    return codon_counts;


Stamford_format = dict();



for gene in gene_list:
    (gene_name, ORF_start, ORF_end, ) = (gene[0], gene[1], gene[2]);
    
    max_depth = 0

    try:  
        gene[3]
    except IndexError:
        first_codon_to_report = 0
    else:
        first_codon_to_report = gene[3]

    try:  
        gene[4]
    except IndexError:
        last_codon_to_report = 0
    else:
        last_codon_to_report = gene[4]


#    print "\t".join([ str(ORF_start),  str(ORF_end)])

    minus_strand = 0

    if ( ORF_start > ORF_end):
        minus_strand = 1
        (ORF_start,  ORF_end) = (ORF_end,  ORF_start )#


    Stamford_format[gene_name] = [];
    variants = []


    iter = samfile.pileup(reference, ORF_start -1 , ORF_end - 1, max_depth=80000)

    skip_bases = 0
    exit_counter = 50

    READING_FRAME_OFFSET = 0

    INDEL_SKIPPING = 0

    for x in iter:
 
        if ( x.pos < ORF_start ):
            continue

        if ( x.pos > ORF_end ):
            break



        # Check that we are in frame...
        if ( (ORF_start - 1  - x.pos )%3):
            continue
#        print "(%d - %d - 1 )/3 == %d" % (ORF_start, x.pos, (ORF_start - 1 -x.pos )%3)

        if ( INDEL_SKIPPING ):
#            print "skipping an indel base: " + str( INDEL_SKIPPING )
            INDEL_SKIPPING += 1
            continue


        indel_counter = dict()

        for read in x.pileups:
            
            if ( read.indel not in indel_counter) :
                indel_counter[ read.indel ] = 0;
                
                indel_counter[ read.indel ] += 1;
                
                
        major_mutation = sorted(indel_counter, key=indel_counter.get, reverse=True);
        
        if ( major_mutation[0] < 0 ):
            INDEL_SKIPPING = major_mutation[0]

        READING_FRAME_OFFSET += major_mutation[0]

#        if ( skip_bases ):
#            skip_bases -= 1
#            continue
   
        skip_bases = 2
    
        passed_bases = 0

        codon_counts = dict()

        for read in x.pileups:

            if (read.alignment.is_unmapped or read.alignment.is_duplicate or read.is_del):
                continue

            if ( read.qpos + read.indel + 3 > read.alignment.alen):
#                print "\t".join([str(read.qpos), str(read.alignment.alen)])
                continue

 
            if ( read.indel > 0):
                insertion = read.alignment.seq[ read.qpos:read.qpos+ read.indel + 3 ]
                codon_counts = update_counts(codon_counts, insertion)
             

            elif ( read.indel < 0):
                deletion = ''
                deletion = read.alignment.seq[ read.qpos] + "-" * abs(read.indel)

                codon_counts = update_counts(codon_counts, deletion)
            
            
            else:
                alt_base = read.alignment.seq[ read.qpos:read.qpos + 3];
                if (len( alt_base) != 3):
                    continue
                codon_counts = update_counts(codon_counts, alt_base)

        if ( 0 and x.pos == 2381) :
            pp.pprint( codon_counts ) 
            print "--->>>" + "\t".join([str(    READING_FRAME_OFFSET), str ( INDEL_SKIPPING)])

        

        good_AA_counts = codon_count2AA_count( codon_counts, minus_strand )

        reference_codon = fasta_ref.fetch(str(samfile.getrname(x.tid)), x.pos + READING_FRAME_OFFSET, x.pos+3 + READING_FRAME_OFFSET)
        reference_AA    = codon2AA( reference_codon)

        if ( minus_strand):
            rev_reference_codon = revDNA( reference_codon )
            reference_AA = codon2AA( rev_reference_codon )


        codon_number    = (1+ (x.pos + 1 - ORF_start)/3)

        if ( minus_strand ):
            transcript_length = (ORF_end - ORF_start + 1)/3
            codon_number    = (transcript_length - (x.pos + 1 - ORF_start)/3)


        if ( first_codon_to_report > 0 and first_codon_to_report > codon_number):
#            print "!!!!!!!" + str(first_codon_to_report) + "\t" + str(codon_number)
            continue

        if ( last_codon_to_report and last_codon_to_report < codon_number):
            continue


        if (max_depth < x.n):
            max_depth = x.n 
#            print "New max depth " + "\t".join([ str(x.pos), str(max_depth) ])

        if ( len(good_AA_counts.keys()) >= 2 ):

            frequencies = []
            for AA in (sorted(good_AA_counts.keys())):
                if ( reference_AA == AA):
                    continue;

                frequencies.append( AA+":"+good_AA_counts[ AA ]+"%")

                Stamford_format[gene_name].append("%s%d%s" % (reference_AA, codon_number, AA))
        
            variants.append(str(x.pos+1) + "\t" + reference_AA +"%d\t" % codon_number + "\t".join( frequencies ))


        else:

            # Only codon is the ref codon, so lets skip on to the next one...
            if (reference_AA in good_AA_counts):
                continue

            frequencies = []
            for AA in (sorted(good_AA_counts.keys())):
                frequencies.append( AA+":"+good_AA_counts[ AA ]+"%")
        
                Stamford_format[gene_name].append("%s%d%s" % (reference_AA, codon_number, AA))

            variants.append(str(x.pos+1) + "\t" + reference_AA +"%d\t" % codon_number + "\t".join( frequencies ))


        if (0):
            exit_counter -= 1
            if ( not exit_counter):
                exit()
            

    if (minus_strand):
        variants.reverse()

#    print gene_name + "MAX_DEPTH :: " + str(max_depth)
    if ( max_depth > 100):
        print gene_name
        print "\n".join( variants )
        print 
    else:
        del Stamford_format[ gene_name ]


print 
print    

for gene in (sorted(Stamford_format.keys())):
    print gene
    print ", ".join(Stamford_format[ gene ]);

