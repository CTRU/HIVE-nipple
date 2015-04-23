import sys

seq = sys.argv[1]

length = len(seq)
print "Sequence is %s bases long" % length

gc = 0
for base in seq:
	if base == "c" or base == "g":
		gc += 1.0
		
	if base not in "atcg":
		raise Exception("Unknown base: %s in sequence" % base)
	
		
	gcent = (gc/(len(seq)))*100	

print 'Its GC content is "%s" percent' % gcent







