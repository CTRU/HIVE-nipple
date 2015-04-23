#!/usr/bin/perl 
use strict;
use warnings;

my @numbers = @ARGV;
print @numbers,"\n";

my @sortednumbers = sort {$a <=> $b} @numbers;

foreach my $number (@sortednumbers) {
	print "$number\n";
}




