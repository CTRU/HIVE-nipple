#!/usr/bin/perl 
# 
# 
# 
# 
# Kim Brugger (11 Feb 2013), contact: kim.brugger@easih.ac.uk

use strict;
use warnings;
use Data::Dumper;

my $samtools = '/software/bin//samtools';

my $MAX_INDEL_DISTANCE = 12;

my $bam = shift;
my $out_bam = shift;
if ( ! $out_bam ) {
  $out_bam = $bam;
  $out_bam =~ s/.bam/_fixed.bam/;
}
open( my $in, "$samtools view -h $bam |") || die "Could not open stream: $!\n";
$bam =~ s/.bam/_fixed.bam/;
open( my $out, "| $samtools view -Sb - > $out_bam") || die "Could not open stream: $!\n";
#open( my $out, " > $bam ") || die "Could not open stream: $!\n";

while( <$in> ) {

  chomp;

  if (/^\@/) {
    print $out "$_\n";
    next;
  }
  else {
    my @F = split("\t");

    my $cigar = $F[ 5 ];
    

    my $fixed_indel = 0;
    do {

      $fixed_indel = 0;
      if ( $cigar =~ /(.*?)(\d+)M(\d*)D(\d+)M(\d*)I(\d+)(M.*)/ ) {
	my $up      = $1;
	my $pre     = $2;
	my $insert  = $3;
	my $between = $4;
	my $delete  = $5;
	my $post    = $6;
	my $down    = $7;
	
	$insert ||= 1;
	$delete ||= 1;
	
	if ( $insert == $delete && $between <= $MAX_INDEL_DISTANCE) {
	  my $new_cigar = $up;
	  $new_cigar   .= ($pre + $between + $insert + $post) ;
	  $new_cigar   .= $down;
	  
	  $cigar = $new_cigar;
	  $fixed_indel = 1;
	}
      }

      if ( $cigar =~ /(.*?)(\d+)M(\d*)I(\d+)M(\d*)D(\d+)(M.*)/ ) {
	my $up      = $1;
	my $pre     = $2;
	my $delete  = $3;
	my $between = $4;
	my $insert  = $5;
	my $post    = $6;
	my $down    = $7;
	
	$insert ||= 1;
	$delete ||= 1;
	
	if ( $insert == $delete  && $between <= $MAX_INDEL_DISTANCE ) {
	  my $new_cigar = $up;
	  $new_cigar   .= ($pre + $between + $insert + $post) ;
	  $new_cigar   .= $down;
	  
	  $cigar = $new_cigar;
	  $fixed_indel = 1;
	}
      }
    } while ( $fixed_indel );

    
    $F[ 5 ] = $cigar;
    
    print $out join("\t", @F) . "\n";

  }

}

close( $in  );
close( $out );
