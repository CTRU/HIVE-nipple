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
$| = 1;

my $bam = shift;
my $out_bam = shift;
if ( ! $out_bam ) {
  $out_bam = $bam;
  $out_bam =~ s/.bam/_fixed.bam/;
}
open( my $in, "$samtools view -h $bam |") || die "Could not open stream: $!\n";
$bam =~ s/.bam/_fixed.bam/;
open( my $out, "| $samtools view -Sb - > $out_bam") || die "Could not open stream: $!\n";

#$out = *STDOUT;

while( <$in> ) {

  chomp;

  if (/^\@/) {
    print $out "$_\n";
    next;
  }
  else {
    my @F = split("\t");
  
    #print STDERR "$_\n";

    #print STDERR "$F[5]  - - \n";    
    my ( $fixed_cigar, $fixed_indel, $mapping_offset );
    do {
    
      my $cigar = $F[ 5 ];
      ( $fixed_indel, $fixed_cigar, $mapping_offset ) = fix_cigar( $cigar );

	if ( $fixed_indel ) {
           $F[ 5 ] = $fixed_cigar;
           $F[ 3 ] += $mapping_offset;
        }


    } while ( $fixed_indel );

    print $out join("\t", @F) . "\n";

  }

}

close( $in  );
close( $out );

# 
# 
# 
# Kim Brugger (07 Apr 2015)
sub fix_cigar {
  my ( $cigar ) = @_;


  my ($fixed_cigar, $new_cigar, $mapping_offset) = (0,"NA",0);

  # Close indel within the read!
  if ( $cigar =~ /(.*?)(\d+)M(\d*)([I|D])(\d+)M(\d*)([I|D])(\d+)M(.*)/ ) {
    my $up_stream     = $1;
    my $pre_match     = $2;
    my $indel1_length = $3;
    my $indel1_type   = $4;
    my $between_match = $5;
    my $indel2_length = $6;
    my $indel2_type   = $7;
    my $post_match    = $8;
    my $down_stream   = $9;
    
    $indel1_length ||= 1;
    $indel2_length ||= 1;

    print join( " -- ",  $up_stream, $pre_match, $indel1_type, $indel1_length, $between_match, 
		         $indel2_type, $indel2_length, $post_match, $down_stream ) ."\n" if (0);

    if ( $indel1_type ne $indel2_type  && 
	 $indel1_length == $indel2_length &&
	 $between_match <= $MAX_INDEL_DISTANCE) {

      my $new_cigar = $up_stream;
      $new_cigar   .= ($pre_match + $between_match + $indel1_length + $post_match) ."M" ;
      $new_cigar   .= $down_stream;
	  
      $fixed_cigar = 1;
      return ($fixed_cigar, $new_cigar, $mapping_offset);
    }

  }
  # 5' indel w/ soft clipping
  if ( $cigar =~ /^(\d*S)(\d+)M(\d*)([I|D])(\d+)M(.*)/ ) {

    my $up_stream    = $1;
    my $pre_match    = $2;
    my $indel_length = $3;
    my $indel_type   = $4;
    my $post_match   = $5;
    my $down_stream  = $6;

    print join( " -- ",  $up_stream, $pre_match, $indel_type, $indel_length,  
		         $post_match, $down_stream ) ."\n" if (0);

    $indel_length ||= 1;
    
    if (  $pre_match <= $MAX_INDEL_DISTANCE ) {
      my $match_length = $pre_match + $post_match;
      $match_length += $indel_length if ( $indel_type eq 'I');
      my $new_cigar = $up_stream . $match_length ."M";
      $new_cigar   .= $down_stream;
      
      $mapping_offset -= $indel_length if ( $indel_type eq "I");
      $mapping_offset += $indel_length if ( $indel_type eq "D");

      $fixed_cigar = 1;
      return ($fixed_cigar, $new_cigar, $mapping_offset);
    }
  }

  # 5' indel wo/ soft clipping
  if ( $cigar =~ /^(\d+)M(\d*)([I|D])(\d+)M(.*)/ ) {

    my $pre_match    = $1;
    my $indel_length = $2;
    my $indel_type   = $3;
    my $post_match   = $4;
    my $down_stream  = $5;

    print join( " -- ",  $pre_match, $indel_type, $indel_length,  
		         $post_match, $down_stream ) ."\n" if (0);

    $indel_length ||= 1;
    
    if (  $pre_match <= $MAX_INDEL_DISTANCE ) {
      my $match_length = $pre_match + $post_match;
      $match_length += $indel_length if ( $indel_type eq 'I');
      my $new_cigar = $match_length ."M";
      $new_cigar   .= $down_stream;
      
      $mapping_offset -= $indel_length if ( $indel_type eq "I");
      $mapping_offset += $indel_length if ( $indel_type eq "D");

      $fixed_cigar = 1;
      return ($fixed_cigar, $new_cigar, $mapping_offset);
    }
  }


  # 3' indel w/ soft clipping
  if ( $cigar =~ /(.*?)(\d+)M(\d*)([I|D])(\d+)M(\d*S)\z/) {
    my $up_stream    = $1;
    my $pre_match    = $2;
    my $indel_length = $3;
    my $indel_type   = $4;
    my $post_match   = $5;
    my $down_stream  = $6;

    print join( " -- ",  $up_stream, $pre_match, $indel_type, $indel_length,  
		         $post_match, $down_stream ) ."\n" if (0);

    $indel_length ||= 1;

    if (  $post_match <= $MAX_INDEL_DISTANCE ) {
      my $match_length = $pre_match + $post_match;
      $match_length += $indel_length if ( $indel_type eq 'I');
      my $new_cigar = $up_stream . $match_length ."M";

      $new_cigar   .= $down_stream;
      
      $fixed_cigar = 1;
      return ($fixed_cigar, $new_cigar, $mapping_offset);
    }
  }

  # 3' indel wo/ soft clipping
  if ( $cigar =~ /(.*?)(\d+)M(\d*)([I|D])(\d+)M\z/) {
    my $up_stream    = $1;
    my $pre_match    = $2;
    my $indel_length = $3;
    my $indel_type   = $4;
    my $post_match   = $5;

    print join( " -- ",  $up_stream, $pre_match, $indel_length, $indel_type, $post_match ) ."\n" if (0);
    
    $indel_length ||= 1;
    
    if (  $post_match <= $MAX_INDEL_DISTANCE ) {
      my $match_length = $pre_match + $post_match;
      $match_length += $indel_length if ( $indel_type eq 'I');
      my $new_cigar = $up_stream . $match_length ."M";

      $fixed_cigar = 1;
      return ($fixed_cigar, $new_cigar, $mapping_offset);
    }
  }

  
  return ($fixed_cigar, $cigar, $mapping_offset);
  
}
