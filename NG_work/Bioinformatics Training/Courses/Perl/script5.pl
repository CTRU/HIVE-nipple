#!/usr/bin/perl 
use strict;
use warnings;


die "No filename given\n" if !defined $ARGV[0];
die "File $ARGV[0] is not in this directory or does not exist!\n" if !-e $ARGV[0];

my $filesize = -s($ARGV[0]);
print "$ARGV[0] is $filesize bytes long\n";

