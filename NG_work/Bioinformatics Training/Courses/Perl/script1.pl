#!/usr/bin/perl
# stricter language and warnings(errors, can use -w at hackline).

use strict; 
use warnings;

print "Hello World!\n";

# -------------------------------------------------------------------------
# Ex.2 - scalars (singles) = use $

# AA s 
my $S = "TCT"; my $L = "TTA"; my $Y = "TAT"; my $C = "TGT";

# Sequence concatenation
my $seq1 = $S . $Y . $L . $Y . $C . "\n";  
 
print $seq1;

# -------------------------------------------------------------------------
# Ex.3 - Arrays (lists) = use @

# Make array using above variables 
my @seq1ls = ($C , $L , $Y , $S  , $Y);

# Printing as array, string and last in array
print @seq1ls , "\n";
print "@seq1ls\n";
print $seq1ls[-1], "\n";

# Adding extra scalar at [n] position in array 
my $Stop = "TAG(stop)"; 
$seq1ls[5] = $Stop;

print "@seq1ls\n";

# ---------------------------------------------------------------------------
# Ex.4 - Hashes (dicts) = use %

# Make hash 
my %AAhash = ('GTT' => 'Valine',
	      'GCA' => 'Alanine',
	      'CCA' => 'Proline',
	      'CAA' => 'Glutamine',
	      'CCG' => 'Proline',
	      'GTG' => 'Valine',
	      );

# Use hash keys to print protein sequence as text string. 
print "$AAhash{GTT}, $AAhash{GCA}, $AAhash{CCA}, $AAhash{CAA}, $AAhash{CCG}, $AAhash{GTT}, $AAhash{GTG} \n";

# --------------------------------------------------------------------------------
# Ex5. Loops 

my @looptest = ('A', 'A', 'A', 'G', 'G', 'G', 'G', 'C', 'C', 'C', 'C', 'T', 'T', 'T', 'T');
print @looptest;

foreach my $base (@looptest) {
	print $base, "\n";
	}

my $basen = 2; 

while ($basen<12) {
		print "$looptest[$basen]\n";
		$basen = $basen + 3;
		}

# -----------------------------------------------------------------------------------
# Ex6. Logical operators

# Make counter
my $gc = 0; 

# Iterate through sequence and add +1 to counter for every G or C 
foreach my $gorc (@looptest) {
		if ($gorc eq 'G' or $gorc eq 'C')
		 	{$gc = $gc + 1;}
}
# % calculation based on length
my $ltlen = @looptest;
my $gcc = ($gc / $ltlen)*100;

print "The GC content of ", @looptest, " is ", $gcc,'%', "\n";
print "The GC content of ", @looptest, " is $gcc%\n";
print "The sequence is $ltlen bases long\n";
#------------------------------------------------------------------------------------
# Ex7. Simplifications 

my $gc2 = 0;

foreach my $gorc2 (@looptest) {
		if ($gorc2 eq 'G' or $gorc2 eq 'C')
		 	{$gc2++;}
}

my $ltlen = @looptest;
my $gcc2 = ($gc2 / $ltlen)*100;
print "The GC content of ", @looptest, " is ", int($gcc2),'%', "\n";
print "The sequence is $ltlen bases long\n";

# -------------------------------------------------------------------------------------
# Ex8. Strings/Functions

# Generating a sequence 
my $ex7seq = "AAAAATTTTTCCCCCGGGGGG";

# Looks at length of sequence and then makes sure that (length of seq / 3) ends in whole number i.e. is divisible by three
# Then the while loop begins, define a counter ($basepos)
# Then create a loop within a loop which is active while the base position counter is less than total sequence length
# The above loop creates a three character substring from the sequence starting at the counter position (0) and prints this with a newline. It then adds the value of 3 to the counter.  

if (length($ex7seq) % 3 == 0) {
    my $basepos = 0;
    while ($basepos < length($ex7seq)) {
        my $codon = substr $ex7seq, $basepos, 3;
        print "$codon\n";
        $basepos += 3;
    }
}
else {
    print "Sequence not divisble by 3\n";
}

# -------------------------------------------------------------------------------------
# Ex9. Array and Hash functions 

my %geneticCode = ('TCT' => 'Serine',
                   'TCC' => 'Serine',
                   'CTA' => 'Leucine', # Hash 
                   'CTG' => 'Leucine',
                   'TGT' => 'Cysteine',
                   'TAG' => 'STOP',
                  );

my $sequence = 'TCCTGTCTACCCCTGAAGTCTTAG'; # Sequence

my $counter8 = 0; 
my $protein = ""; # Defining objects 
my $aminoacid;

while ($counter8 < length($sequence)) { # Run while counter < seqlength
	my $codons = substr $sequence, $counter8, 3; # Substrings from counter pos+3 (gen codons)
	if (exists $geneticCode{$codons}) { # If loop, if codon is in hash run
		$aminoacid = ($geneticCode{$codons}); # Looks up codon value in hash, returns val
		if ($aminoacid eq 'STOP') { # If loop, if val = stop append a * to Protein
			$protein .= '*';
		}
		else { # Else, substring val position 0 to 1, append sub(val) to protein. 
            		$protein .= substr $aminoacid, 0, 1;
        	}}
        else {
        $protein .= '?'; # If does not exist in keys, append a ? to protein. 
    }
    $counter8 += 3; # Move on the counter by three.
}

print "$protein\n"; # Print protein object after loop.
	 
# ------------------------------------------------------------------------------------------
# Ex.10 Subroutines


my @meanarray = (15, 10); # Creates Array

sub mean1 {
	my $a = shift;
	my $b = shift; # Define subroutine
	return ($a+$b)/2;
	}

my $subtest = mean1(@meanarray); # Uses mean1 on array

print "$subtest\n";

#--------------------------------------------------------------------------------------------
# Ex.11 User/Command line inputs
# See script2.pl and script3.pl

#--------------------------------------------------------------------------------------------
# Ex. 12 













