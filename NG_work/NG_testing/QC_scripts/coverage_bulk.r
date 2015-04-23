args <- commandArgs(trailingOnly = TRUE)
print(args)


png("tyt.png", width=1048,height=440)

plot(0,0, xlim=c(0,10000), ylim=c(0,10000), col='darkgreen', xlab='Genome position (bp) ', ylab='count', type='l')


for ( file in args) {

    print( file )

    depth <- read.delim( file, header=F)
    depth_high <- depth[ depth$V3 > 100,]


    lines(depth_high$V2, depth_high$V3, col='darkgreen', xlab='Genome position (bp) ', ylab='count', type='l')
}

title(main = paste("Depth plot for sample ", "T"))
dev.off()
