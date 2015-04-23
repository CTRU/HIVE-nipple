# Pipeline for producing clipped and unclipped bamfiles from sample_name's
# 23st April 2015
# Nicholas S. Gleadall - ng384@cam.ac.uk

# print "Hello World!"

#------------------------------------------------------------
# Importing Modules

import sys
import subprocess
import os
import re

#------------------------------------------------------------
# Setting globals

# Software bin loaction
bin = "/software/bin/"

VERBOSE = 'INFO'


#------------------------------------------------------------
# Make system call fucntion

def system_call( step_name, cmd ):

    try:
        subprocess.check_call(cmd, shell=True)

    except subprocess.CalledProcessError as scall:
        if ( VERBOSE == "DEBUG"):
            print "Script failed at %s stage - exit code was %s, ouput = %s" % (step_name, scall.returncode, scall.output) 

        if ( VERBOSE == "INFO"):
            print "Script failed at %s stage - exit code was %s" % (step_name, scall.returncode)
        exit()

#------------------------------------------------------------
# Define fastq's and get sample names. 

# Gets location of fastq
fastq_dir = sys.argv[1]

# Make analysis directory
analysis_dir = fastq_dir +"unclip_analysis/"

# Set globals 
sample_name = ""
sample_name_unclipped = ""

# Get sample names from fasta files
for item in os.listdir(fastq_dir):
    if item.endswith(".1.fq.gz"):
        sample_name = re.sub(r"(.*).1.fq.gz", r"\1", item)




#------------------------------------------------------------
# Commands to be executed

# Make analysis directory

make_analysis_directory = "mkdir " + analysis_dir

# remove the sequencing adaptors
remove_adapters_1 = "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT " + fastq_dir + sample_name +".1.fq.gz"
remove_adapters_2 = "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT " + fastq_dir + sample_name +".2.fq.gz"

# Align the reads to the reference (run smalt-0.7.6 to see all options)
smalt_1 = "/software/bin/smalt-0.7.6 map -f samsoft /refs/HIV/K03455_s1k6 " + sample_name + "_ra.1.fq.gz " + sample_name + "_ra.2.fq.gz > " + sample_name + ".sam"

# Make the samfile into a bam file using samtools
sam_to_bam = "/software/bin/samtools view -Sb " + sample_name + ".sam -o " + sample_name + ".bam"

# Sort the bamfile with samtools
sort_bam_1 = "/software/bin/samtools sort " + sample_name + ".bam " + sample_name + "_sorted"

# Mark/remove duplicate reads
deduplicate_bamfile = "/software/bin/picard -T MarkDuplicates I= " + sample_name + ".bam O= " + sample_name + " _rmdups.bam AS=true M=" + sample_name + "_rmdup.csv"

# Index the bam file so it can be viewed in IGV later on
index = "/software/bin/samtools index " + sample_name + "_rmdups.bam"

# HIV alignment fix
alignment_fixing_HIV = "/software/packages/HIV-pipeline/scripts/bam_fix_indels.pl " + sample_name + "_rmdups.bam " + sample_name + "_fixed.bam"

# Index the new bam file so it can be viewed in IGV later on
index_fix = "/software/bin/samtools index " + sample_name + "HIV_fixed.bam"

#------------------------------------------------------------
# Main pipeline 

system_call("Making directory", make_analysis_directory)


#system_call("Removing adapters from fastq 1" , remove_adapters_1)
system_call("Removing adapters from fastq 2" , remove_adapters_2)

    
   


#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
