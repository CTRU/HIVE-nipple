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

VERBOSE = 'DEBUG'


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
        sample_name_unclipped = sample_name + "_unclipped"


#------------------------------------------------------------
# Commands to be executed

# Make analysis directory

make_analysis_directory = "mkdir " + analysis_dir

# remove the sequencing adaptors
<<<<<<< HEAD
remove_adapters_1 = "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT " + fastq_dir + sample_name +".1.fq.gz > " + analysis_dir + sample_name + "_ra.1.fq; cd " + analysis_dir + "; gzip " + sample_name + "_ra.1.fq; cd .."
remove_adapters_2 = "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT " + fastq_dir + sample_name +".2.fq.gz > " + analysis_dir + sample_name + "_ra.2.fq; cd " + analysis_dir + "; gzip " + sample_name + "_ra.2.fq; cd .."
=======
remove_adapters_1 = "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT " + fastq_dir + sample_name +".1.fq.gz > " + analysis_dir + sample_name + "_rm.1.fq"
remove_adapters_2 = "/software/packages/cutadapt-1.1/bin/cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT " + fastq_dir + sample_name +".2.fq.gz > " + analysis_dir + sample_name + "_rm.2.fq"
>>>>>>> 2c62b93d6daaaa14c8bbb1e23f19b1a3dda9d6c9

# Align the reads to the reference (run smalt-0.7.6 to see all options)
smalt = "/software/bin/smalt_0.7.6 map -f samsoft /refs/HIV/K03455_s1k6 " + analysis_dir + sample_name + "_ra.1.fq.gz " + analysis_dir + sample_name + "_ra.2.fq.gz > " + analysis_dir + sample_name + ".sam"

# Make the samfile into a bam file using samtools
sam_to_bam = "/software/bin/samtools view -Sb " + analysis_dir + sample_name + ".sam -o " + analysis_dir + sample_name + ".bam"

# Sort the bamfile with samtools
sort_bam_1 = "/software/bin/samtools sort " + analysis_dir + sample_name + ".bam " + analysis_dir + sample_name + "_sorted"

# Mark/remove duplicate reads
deduplicate_bamfile = "/software/bin/picard -T MarkDuplicates I= " + analysis_dir + sample_name + "_sorted.bam O= " + analysis_dir + sample_name + "_rmdups.bam AS=true M=" + analysis_dir + sample_name + "_rmdup.csv"

# Index the bam file so it can be viewed in IGV later on
index = "/software/bin/samtools index " + analysis_dir + sample_name + "_rmdups.bam"

# HIV alignment fix
alignment_fixing_HIV = "/software/packages/HIV-pipeline/scripts/bam_fix_indels.pl " + analysis_dir + sample_name + "_rmdups.bam " + analysis_dir + sample_name + "_fixed.bam"

# Index the new bam file so it can be viewed in IGV later on
index_fix = "/software/bin/samtools index " + analysis_dir + sample_name + "_fixed.bam"

# Run unclip bamfile
unclip_bamfile = "/software/bin/scripts/bam_unclip_bases.pl " + analysis_dir + sample_name + ".bam"

#------------------------------------------------------------
#------------------------------------------------------------
<<<<<<< HEAD
# Sort the unclipped bamfile with samtools
sort_bam_2 = "/software/bin/samtools sort " + analysis_dir + sample_name_unclipped + ".bam " + analysis_dir + sample_name_unclipped + "_sorted"

# Mark/remove duplicate reads
deduplicate_bamfile_2 = "/software/bin/picard -T MarkDuplicates I= " + analysis_dir + sample_name_unclipped + "_sorted.bam O= " + analysis_dir + sample_name_unclipped + "_rmdups.bam AS=true M=" + analysis_dir + sample_name_unclipped + "_rmdup.csv"

# Index the bam file so it can be viewed in IGV later on
index_2 = "/software/bin/samtools index " + analysis_dir + sample_name_unclipped + "_rmdups.bam"
=======
# Main pipeline
>>>>>>> 2c62b93d6daaaa14c8bbb1e23f19b1a3dda9d6c9

# HIV alignment fix
alignment_fixing_HIV_2 = "/software/packages/HIV-pipeline/scripts/bam_fix_indels.pl " + analysis_dir + sample_name_unclipped + "_rmdups.bam " + analysis_dir + sample_name_unclipped + "_fixed.bam"

# Index the new bam file so it can be viewed in IGV later on
index_fix_2 = "/software/bin/samtools index " + analysis_dir + sample_name_unclipped + "_fixed.bam"

<<<<<<< HEAD
# Run unclip bamfile
unclip_bamfile_2 = "/software/bin/scripts/bam_unclip_bases.pl " + analysis_dir + sample_name_unclipped + ".bam"

=======
system_call("Removing adapters from fastq 1" , remove_adapters_1)
system_call("Removing adapters from fastq 2" , remove_adapters_2)



>>>>>>> 2c62b93d6daaaa14c8bbb1e23f19b1a3dda9d6c9


#------------------------------------------------------------
# Make directory
#system_call("DIRECTORY", make_analysis_directory)

# Process raw fastq files
#system_call("DE-ADAPT2", remove_adapters_2)
#system_call("DE-ADAPT1", remove_adapters_1)

# Align to reference
#system_call("SMALT ALIGNMENT", smalt)
system_call("samfile > bamfile", sam_to_bam)
# Regular pipeline
system_call("sort_bam_1", sort_bam_1)   
system_call("deduplicate_bamfile", deduplicate_bamfile)
system_call("index", index)
system_call("HIV_fix", alignment_fixing_HIV)
system_call("Index fixed", index_fix)

# Unclip bamfile and proceed with rest of analysis 
system_call("unclip", unclip_bamfile)
# Rest of pipeline
system_call("sort_bam_2", sort_bam_2)   
system_call("deduplicate_bamfile2", deduplicate_bamfile_2)
system_call("index2", index_2)
system_call("HIV_fix2", alignment_fixing_HIV_2)
system_call("Index fixed2", index_fix_2)
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
