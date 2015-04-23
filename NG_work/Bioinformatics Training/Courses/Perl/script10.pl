#!/usr/bin/perl 
use strict;
use warnings;

my $dna = "catgcatgcatgcgcgcgcgGCAG";

if ($dna =~ /CG/) {
    print "CG Dinucleotide present\n";
}


if ($dna =~ /^[ATCGatcg]+$/) { 
	print "Sequence only contains bases\n";
}	

elsif ($dna !~ /^[ATCGatcg]+$/) {
	die "Contains unknown base\n";
	}

if ($dna =~ /[GA]C[ACTG]G/) {
    print "Meth site found\n";
}
elsif ($dna !~ /[GA]C[ACTG]G/) {
    print "No meth site\n";
}












































