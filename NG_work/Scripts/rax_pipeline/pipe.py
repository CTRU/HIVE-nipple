# Generic process pipelining script using system calls
# 21st April 2015
# Nicholas S. Gleadall - ng384@cam.ac.uk

# print "Hello World!"

#------------------------------------------------------------
# Importing Modules

import sys
import subprocess

LEVELS = {'DEBUG' = 10,
	      'INFO' = 9}

VERBOSE = LEVEL[ 'DEBUG' ]


#------------------------------------------------------------
# Make system call fucntion

def system_call( step_name, cmd ):

	if ( VERBOSE > LEVELS['DEBUG']}):
		print cmd

	if ( VERBOSE > LEVELS['INFO']}):
		print "Am now doing :: " + step_name


		
    print locals().keys()

    try:
        subprocess.check_call(cmd, shell=True)

    except subprocess.CalledProcessError as scall:
        print "Script failed at %s stage - exit code was %s, ouput = %s" % (cmd, scall.returncode, scall.output)
        exit()

#------------------------------------------------------------
# Define arguments for script, firstly location of file containg fasta's and...
#   secondly analysis output name definition

in_dir = "."

if sys.argv[1:]:
    in_dir = sys.argv[1]

out_name = "YOU_FORGOT_TO_NAME_THIS_OUTPUT"

if sys.argv[2:]:
    out_name = sys.argv[2]

#------------------------------------------------------------
# Commands to be executed

# Sets up directories for alignment and tree files
directory_setup = "mkdir "+in_dir+"alignment/ "+in_dir+"rax_tree/"

# Concatenates all fastas into one file.catted.fasta for alignment purposes
cat_sequences = "cat "+in_dir+"*.fasta > "+in_dir+"/alignment/"+out_name+".catted.fasta"

# Running clustal omega on catted sequences
clustal_omega = "clustalo -i "+in_dir+"/alignment/*.catted.fasta -o "+in_dir+"/alignment/"+out_name+".aln.fa -v"

# Running raxML on alignment output, note has to change directory for raxml
raxML = "cd "+in_dir+"rax_tree/; raxmlHPC -b 1 -# 100 -s ../alignment/"+out_name+".aln.fa -n "+out_name+" -m GTRGAMMA -p 12"


#------------------------------------------------------------
# Pipeline ordering - this is the actual pipeline
system_call("directory_setup", directory_setup)

system_call("cat_sequences", cat_sequences)

system_call("clustal_omega", clustal_omega)

system_call("raxML", raxML)

#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
#------------------------------------------------------------
