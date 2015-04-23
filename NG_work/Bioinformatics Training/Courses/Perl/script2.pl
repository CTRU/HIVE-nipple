#!/usr/bin/perl
use strict;
use warnings; 
# Script which adds two user defined numbers 
# Edited to check for correct numbers

use Scalar:Util ('looks like a number');


#if (!defined $ARGV[0] or !defined $ARGV[1]) { # If number 1 or 2 arent defined kills prog
	#die "Not enough numbers";}
	
#if (defined $ARGV[2]) {
#		die "Too many numbers"; # If too many numbers are defined kills prog
#}

my ($v1, $v2) = @ARGV; # Unpacks @ARGV array to v1 and v2 idividual objects 
print $v1 + $v2, "\n"; # Prints sum of v1 and v2 


