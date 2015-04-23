#!/usr/bin/perl 
use strict;
use warnings;

my @ls = `ls`;

for my $files (@ls) {
	chomp($files);
	if (substr($files, -3, 3) eq ".pl") {
		print uc$files, " ";
	}
}

print "\n"



