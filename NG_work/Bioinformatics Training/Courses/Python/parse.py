import sys
print "hello world"
try:
	v1 = float(sys.argv[1])
	v2 = float(sys.argv[2])
except ValueError:
	print "Cannot convert to number, not used numeric value"
except IndexError:
	print "Supply 2 numbers"
else:	

	total = v1

	print total 


