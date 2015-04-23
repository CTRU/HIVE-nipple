dna = "aaaccctttgggatc"
print dna
# Make a cg variable
gc = 0 


# Loop over dna string and add 1 to the cg variable for every 
# entry that = g or c
# !!!!! remeber when using OR function to define again that the 
# variable you want to see if is "c/g" is one defined in loop 
#(in this e.g. base)
for base in dna:
	if base == "c" or base == "g":
		gc += 1.0
		
	if base not in "atcg":
		raise Exception("Unknown base: %s" % base)
	
		
		
print gc
gcent = (gc/len(dna))*100.0	
print "GC content %s" % gcent 
