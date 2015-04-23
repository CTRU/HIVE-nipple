#!/usr/bin/perl 
use strict;
use warnings;

my $dna = uc("CGAGGACTGCAGGGATCTACTGCAGGCCAGCGCGAAGAGACTCATATACTGCAGCGTCG");
print "$dna\n";

$dna =~ s/T/U/g;
print "$dna\n";


