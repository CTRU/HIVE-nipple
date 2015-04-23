args <- commandArgs(trailingOnly = TRUE)
#print(args)

out_file = args[1]
out_file = sub("(.*).bam.depth", "\\1.png", out_file)
print(out_file)
png(out_file, width=1048,height=440)


depth <- read.delim( args[1], header=F)
#print(depth)

depth_high <- depth[ depth$V3 > 100,]
#print(depth_high)

sample_name <- args[1]
sample_name <- sub(".*/(.*?).bam.*", "\\1", sample_name)
#print(sample_name)

 


plot(depth_high$V2, depth_high$V3, xlim=c(0,10000), ylim=c(0,10000), col='darkgreen', xlab='Genome position (bp) ', ylab='count', type='l')
	
title(main = paste("Depth plot for sample ", sample_name))



dev.off()	


