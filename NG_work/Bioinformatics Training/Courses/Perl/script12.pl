#!/usr/bin/perl 
use strict;
use warnings;

my $head;
my $sequence;
my %faseqs;

open my $fa, '<', 'lesson13_file5.fasta' or die "Can't open FASTA file!\n";

print $fa,"\n";

my $start = 0;

while (my $line = <$fa>) {
    chomp $line;
    if ($line =~ /^>(.+)$/) {
        $head = $1;
        $start = 0;
        $faseqs{$head} = '-';

    }
    
	elsif ($start == 1) {
        $faseqs{$head} .= $line;
    }
    
	elsif ($line =~ /TATTAT(.+)/) {
        $faseqs{$head} = $1;
        $start = 1;
    }
}
close $fa;
 
print $fa, "\n";

foreach my $name (keys %faseqs) {
    print "$name\t$faseqs{$name}\n";
}
