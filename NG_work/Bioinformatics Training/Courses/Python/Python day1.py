# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/participant/.spyder2/.temp.py
"""
# ---------------------------------------------------------------
# Name + Age exer
print "Name exer"
name = "Nick" 
age = 24

print """
My name is %s I am %s years old.
In ten years I will be %s years old
""" % ( name, age, age + 10 )
#---------------------------------------------------------------
# Genetic code exer 
print "Genetic code exer"
s = "TCT"
l = "CTT"
y = "TAT"
c = "TGT"

dna = s+y+l+y+c

print "Possible DNA sequence =", dna

# --------------------------------------------------------------

# Data structures 1 
print "List excer"

s = "TCT"
l = "CTT"
y = "TAT"
c = "TGT"

# Creating list of codon sequences
seqls = [s, l, y, c]
print seqls

# Spaces between each codon
jseqls = " ".join(seqls)
print jseqls

# Print last codon sequence in list 
print seqls[-1]

# Create Start/Stop codon variables
sta = "ATG" 
sto = "TGA"

# Delete first sequence, replace with start codon and append stop
# codon to list. 
print seqls
del seqls[0]
seqls.insert(0,sta)
seqls.append(sto)

print " ".join(seqls)

# ----------------------------------------------------------------

# String modifications

# Define variables
Name = "Nick S Gleadall"

# Create list from var splitting by spaces
Nlist = Name.split(" ")
print Nlist

# Print surname
print Nlist[2]

# Check surname for FIRST INSTANCE OF letter l
pos = Nlist[2].find("l")
print pos

# Print name and age using modifiers 
print "My name is %s it is %.1f letters long" %(Name, len(Nlist[0])) 

# ----------------------------------------------------------------

# Sets the seq and lists it out letter by letter
seq = "MPISEPTFFEIF"
aa = list(seq)

print aa

# Puts the AA list into a set, deletes duplicates
uniaa = set(aa)
print uniaa

# ----------------------------------------------------------------

seq = "GTT GCA CCA CAA CCG"
codons = seq.split(" ")
print codons

###
#Valine = "GTT"
#Alanine = "GCA"
#Proline = "CCA"
#Glutamine = "CAA"
#Arganine = "CCG"
###

dseq = ({"GTT": "Valine", "GCA": "Alanine",
"CCA": "Proline", "CAA": "Glutamine", "CCG": "Arganine"})
print dseq

"GTT" in dseq

# Answer - Multiple codon combinations for same amino acids, hash has to have 
# unique values 

# ------------------------------------------------------------------

# Advanced excer 

# Start with and empty dict
aad = {}

seq = "MKALIVLGLVLLSVTVQGKVFERCELARTLKRLGMDGYRGISLANWMCLAKWESGYNTRATNYNAGDRSTDYGIFQINSRYWCNDGKTPGAVNACHLSCSALLQDNIADAVACAKRVVRDPQGIRAWVAWRNRCQNRDVRQYVQGCGV"

# This functions iterates over the sequence, assisngs value of the residue to "aa"
# if aa is allready inside the dict it adds 1 count
# if not it adds the residue id to the dict and counts 1

for aa in seq : 
	if aa in aad : 
		aad[aa] += 1
		
	else : 
		aad[aa] = 1
		
# Prints the generated dictionary		
print aad
	

# ---------------------------------------------------------------------------

mage = 24
tage = 15

if tage > mage:
	print "They are older"
elif tage < mage:
	print "They are younger"
	
# ---------------------------------------------------------------------------

dna = "TTA"

sto1 = "TAG"
sto2 = "TTA"
sto3 = "TGA"



if sto1 in dna :
	print "Has TAG stop codon"

if sto2 in dna :
	print "Has TTA stop codon"
	
if sto3 in dna :
	print "Has TGA stop codon"

#-----------------------------------------------------------------------------

dna = "aaaccctttgggatc"

seq = list(dna)

pos = 2

while pos <= 12:
	print seq[pos]
	pos += 3

# --------------------------------------------------------------

#USEFUL 

# Finding the GC content of a sequence 

# Define DNA sequence (here as string)
dna = "aaaccctttgggatc"
print dna
# Make a cg variable
gc = 0 

# Loop over dna string and add 1 to the cg variable for every 
# entry that = g or c
# !!!!! remeber when using OR function to define again that the 
# variable you want to see if is "c/g" is loop (in this e.g. base)
for base in dna:
	if base == "c" or base == "g":
		gc += 1
		
print "GC content =", (gc/(len(dna)))*100
