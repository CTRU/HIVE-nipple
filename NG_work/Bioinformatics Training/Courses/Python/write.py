import sys 

output = open ("out.txt", "w")

map(lambda x: output.write(str(x)+'\n'), range(1, 20, 2))

output.close()
