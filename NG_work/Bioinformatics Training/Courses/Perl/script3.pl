#!/usr/bin/perl
use strict;
use warnings;
# Script which takes sequence and prints length/GC content 

my $seq = uc($ARGV[0]); # Assigns argument to $seq as string, forces uppercase, [0] means item 1
my $gc2 = 0; # Establishes counter

foreach my $gorc2 (split '', $seq) { # Start of loop, split each character in $seq
		if ($gorc2 eq 'G' or $gorc2 eq 'C') # If character = G or C +1 to counter
		 	{$gc2++;}
}

my $sqlen = length($seq); # Length of sequence 
my $gcc2 = ($gc2 / $sqlen )*100; # GC content. 

print "The DNA sequence $seq is $sqlen bases long, it's GC content is $gcc2\%\n"; # Printing
print "The DNA sequence ", $seq, " is ", $sqlen, " bases long. It's GC content is ", $gcc2, "%\n";
