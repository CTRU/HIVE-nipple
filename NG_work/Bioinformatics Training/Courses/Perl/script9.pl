#!/usr/bin/perl 
use strict;
use warnings;

die "no sequence\n" if @ARGV != 1;

my $dna = uc(shift(@ARGV));
my %basecount;

foreach my $base (split '', $dna) {
	$basecount{$base}++;
}

# Copied from learning materials this copies the hash into an array sorted via ASCII 
my @sortedbc = sort {$basecount{$a} <=> $basecount{$b}} keys(%basecount);

print join ' - ', @sortedbc;

print "\n";

foreach my $count (@sortedbc) {
	print "$count\t$basecount{$count}\n";
}

