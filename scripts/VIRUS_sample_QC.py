#!/usr/bin/python
import sys
import os
import re
import getopt
import pprint
pp = pprint.PrettyPrinter(indent=4)

import tempfile

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.pyplot import *


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
width, height = A4 #keep for later

sys.path.append("/software/lib/python2.7/site-packages/pysam-0.7.1-py2.7-linux-x86_64.egg/")

import pysam

bamfile = sys.argv[1]
samfile = pysam.Samfile( bamfile, "rb" )
sample_name = re.sub(r'^.*\/(.*?)[\.|_].*', r'\1', bamfile)
sample_name = re.sub(r'(.*?)[\.|_].*', r'\1', bamfile)
#print sample_name

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
                 ['Pol', 76906, 80631]]
    fasta_ref = pysam.Fastafile('/refs/CMV/CMV_AD169.fasta')
    reference = "CMV_AD169"


def add_header(c, sample_id ):
    c.drawString(40 , height - 40, "Sample: %s" % sample_id)

    


c = canvas.Canvas("%s_QC.pdf" % sample_name, pagesize=A4)
add_header(c, sample_name )


image_offset = 320


for gene in gene_list:
    (gene_name, ORF_start, ORF_end, ) = (gene[0], gene[1], gene[2]);
    
    try:  
        gene[3]
    except IndexError:
        first_codon_to_report = 1
    else:
        first_codon_to_report = gene[3]

    try:  
        gene[4]
    except IndexError:
        last_codon_to_report = ORF_end/3
    else:
        last_codon_to_report = gene[4]

    
    iter = samfile.pileup(reference, ORF_start -1 , ORF_end - 1, max_depth=80000)

    skip_bases = 0
    exit_counter = 50

#    depths = dict()
    positions      = []
    forward_depths = []
    reverse_depths = []
    total_depths   = []

    max_depth = 0

    for x in iter:
 

        if ( x.pos < ORF_start - 1):
            continue

        if ( x.pos > ORF_end ):
            break

        if ( ((x.pos - ORF_start) /3) < first_codon_to_report):
            continue

        if ( ((x.pos - ORF_start) /3) > last_codon_to_report):
            continue
        
        plus_strand_reads  = 0
        plus_strand_qual   = 0
        minus_strand_reads = 0
        minus_strand_qual  = 0

        if (max_depth < x.n):
            max_depth = x.n 


        for read in x.pileups:
            


            if (read.alignment.is_unmapped or read.alignment.is_duplicate or read.is_del):
                continue

            if ( read.alignment.is_reverse ):
                minus_strand_reads += 1
            else :
                plus_strand_reads += 1

        positions.append((x.pos-ORF_start)/3)
        forward_depths.append( plus_strand_reads )
        reverse_depths.append( minus_strand_reads )
        total_depths.append( plus_strand_reads + minus_strand_reads )

    if ( max_depth < 100):
        continue


    fig, ax = plt.subplots()
#    fig.set_size_inches(6,5)
    ax.set_xlim(1, (ORF_end - ORF_start) / 3)
    ax.axhline(y=1000, linewidth=2, color='c')
#    ax.axvline(x=first_codon_to_report, linewidth=2, color='c')
#    ax.axvline(x=last_codon_to_report, linewidth=2, color='c')


    ax.set_title("%s coverage" % gene_name, fontsize = 30)
    ax.set_xlabel('Codon position', fontsize = 20)
    ax.set_ylabel('depth', fontsize = 20)


    fwd = ax.plot(positions, forward_depths)
    rev = ax.plot(positions, reverse_depths)
    all = ax.plot(positions, total_depths)

    ax.legend((fwd[0], rev[0], all[0]), ("Forward", "Reverse", "Total"))
    
    image_name = "%s.png" % gene_name
    (fd, filename) = tempfile.mkstemp()
    os.remove(filename)    
    image_name = "%s.png" % filename
    
    savefig( image_name )

    c.drawInlineImage(image_name, 60, height - image_offset, width=300, height=200) 
    c.drawString(350 , height - image_offset + 160, "Forward min. depth: %d" % min( forward_depths ))
    c.drawString(350 , height - image_offset + 140, "Forward mean depth: %.2f" % (sum( forward_depths )/len( positions )))
    c.drawString(350 , height - image_offset + 120, "Reverse min. depth: %d" % min( reverse_depths ))
    c.drawString(350 , height - image_offset + 100, "Reverse mean depth: %.2f" % (float(sum( reverse_depths )/len( positions ))))
    c.drawString(350 , height - image_offset +  80, "Total min. depth: %d" % min( total_depths ))
    c.drawString(350 , height - image_offset +  60, "Total mean depth: %.2f" % (float(sum( total_depths ))/len( positions )))

#    c.drawString(350 , height - image_offset +  20, "Total mean depth: %d %d" % (min( total_depths ),len( positions )))

    
    image_offset += 200

    os.remove(image_name)    



#hello(c)
c.showPage()
c.save()
