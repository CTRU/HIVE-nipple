#!/usr/bin/perl 
# 
# 
# 
# 
# Kim Brugger (08 Apr 2015), contact: kbr@brugger.dk

use strict;
use warnings;
use Data::Dumper;
my $samtools = '/software/bin//samtools';


my $bam = shift;
my $out_bam = shift;
if ( ! $out_bam ) {
  $out_bam = $bam;
  $out_bam =~ s/.bam/_unclipped.bam/;
}
open( my $in, "$samtools view -h $bam |") || die "Could not open stream: $!\n";
$bam =~ s/.bam/_fixed.bam/;
open( my $out, "| $samtools view -Sb - > $out_bam") || die "Could not open stream: $!\n";

#$out = *STDOUT;

#$out = *STDOUT;

while( <$in> ) {
  chomp;
  if (/^\@/) {
    print $out "$_\n";
    next;
  }
  else {
    my @F = split("\t");
  
    
    my $cigar = $F[ 5 ];

    if ( $cigar =~ /(.*?)(\d+)M(\d*)S\z/) {
      my $up_stream    = $1;
      my $match_length = $2;
      my $soft_length  = $3;
      
      $cigar = $up_stream . ( $match_length + $soft_length) ."M";
      $F[ 5 ] = $cigar;
    }
    
    if ( $cigar =~ /^(\d*)S(\d+)M(.*)/) {
      my $soft_length  = $1;
      my $match_length = $2;
      my $down_stream  = $3;
      
      $cigar = ( $match_length + $soft_length) ."M$down_stream";
      $F[ 5 ] = $cigar;
      $F[ 3 ] -= $soft_length;
    }

    print $out join("\t", @F) . "\n";
  }

}

