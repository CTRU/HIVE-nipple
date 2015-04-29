print "hello world" 
#---------------------------------------------------------
# Importing modules

from suds.client import Client
import os
import sys
import re

#---------------------------------------------------------
# Setup Globals

#globals for I/O
infolder = sys.argv[1]

#globals for client
service = "http://db-webservices.stanford.edu:5440/axis/services/StanfordAlgorithm?wsdl"
client = Client(service)

key = "0000-0000-0000-0000"

# globals for functions
sequence = ""
sequences = []
mutation_list = []

#---------------------------------------------------------
# Define Functions

#***************************************************************************
# Method:      processSequence
# Description: Send a sequence to Sierra for processing.
# Arguments:   key - string holding the authorization key
#              $sequence - string holding the sequence.  Suggest cleaning
#                          the string before passing it to this method.
# Returns:     The XML output from the web service. Returned as a string.
#***************************************************************************
def processSequence(sequence):
	
	return client.service.processSequences(key,sequence)

#***************************************************************************
# Method:      processSequences
# Description: Send multiple sequences to Sierra for processing.
# Arguments:   key - string holding the authorization key
#	       (non-argument)reportType  - 0 for Simple Report 1 for Detailed Report
#   	       Sequences - reference to a list containing NA sequences 
#			   which need to be interpreted. Suggest cleaning
#                          the sequences before passing it to this method.
#              
# Returns:     The XML output from the web service. Returned as a string.
#***************************************************************************

def processSequences(sequences):
	
	return client.service.processSequences(key,1,sequences) 

#***************************************************************************
# Method:      processMutationLists
# Description: Send multiple mutation lists to Sierra for processing.
# Arguments:   key - string holding the authorization key
#	       (non-arg)reportType - 0 for Simple Report, 1 for Detailed Report
#	       mutationLists - reference to a list containing mutation lists 
#	                       which need to be interpreted.
#
# Returns:     The XML output from the web service. Returned as a string.
#***************************************************************************
def processMutationLists(mutation_list):
    
    return client.service.processMutationLists(key, 1, mutation_list)
    

#---------------------------------------------------------
# Import sequences and clean them (by removing non letter characters)

for file in os.listdir(infolder):
	if file.endswith(".fasta"):
		sequence_file = open(infolder+file, "rU")
		
		for line in sequence_file.readlines():
			#if line.startswith(">"):
				#title = line

			if line.startswith(">"):
				continue
			line = re.sub(r'[^A-Za-z]', r'', line)
			
			sequences.append(line)

print sequences
print processSequences(sequences)
			

			


		
		
