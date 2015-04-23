gene_file = open("genes.txt", "r")
out_file = open("genes_lengths.txt", "w")

print gene_file

for line in gene_file:
	gene, chrom, start, end = line.strip().split("\t")
	length = int(end) - int(start) + 1
	out_file.write("%s, %d\n" % (gene, length))

gene_file.close()
out_file.close()
		


