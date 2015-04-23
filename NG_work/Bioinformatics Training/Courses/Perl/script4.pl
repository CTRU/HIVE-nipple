#!/usr/bin/perl 
use strict;
use warnings;
# Script which takes a filename and prints the size of the file. 

if (-e $ARGV[0]) {
	my $size = -s($ARGV[0]); # 
	print $size, "\n";
	}
else {
	die "File does not exist\n"
}


