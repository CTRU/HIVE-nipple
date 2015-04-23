print "Hello world!"

import pysam
import sys

inbam = sys.argv[1]

pysam.index(inbam)
infile = pysam.AlignmentFile(inbam, "rb")

subtype_scores = {}

for line in infile.fetch():
    line = str(line)
    line = line.split("\t")

    if line[4] < 30:
        continue

    refid = line[2]
    quality_score = line[4]

    if refid not in subtype_scores.keys():
        subtype_scores[refid] = 1

    else:
        if refid in subtype_scores.keys():
            subtype_scores[refid] += 1

best_ref = int(max(subtype_scores, key=subtype_scores.get))

best_ref_name = infile.getrname(best_ref)

print best_ref_name
