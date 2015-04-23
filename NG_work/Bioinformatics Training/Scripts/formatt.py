print "Hello World!"

import re
import os
import sys



infile = sys.argv[1]


for i in os.listdir(infile):
    if not i.endswith(".fasta"):
        continue

    new_filename = re.sub(r'(.*)_(.*)_(.*)\.(.*.fasta)', r'\1_\2_\3_\4', i)
    print new_filename

    os.rename(i, new_filename)
