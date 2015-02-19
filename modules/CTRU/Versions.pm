package CTRU::Versions;
# 
# Module for providing versions for programs used in the pipelines
# 
# 
# Kim Brugger (24 Oct 2013), contact: kim.brugger@easih.ac.uk

use strict;
use warnings;
use Data::Dumper;



# 
# 
# 
# Kim Brugger (24 Oct 2013)
sub samtools {
  my ( $program ) = @_;

  open( my $pipe, "$program 2>&1 | head -n 3 |") || die "Could not open samtools pipe: $!\n";
  <$pipe>;
  <$pipe>;
  my $version = <$pipe>;
  chomp( $version);
  $version =~ s/Version: //;
  
  return( $version);
}


# 
# 
# 
# Kim Brugger (08 Nov 2010)
sub picard {
  my ( $program ) = @_;

  my $version = `$program -v`;
  chomp($version);
  return $version;
}



# 
# 
# 
# Kim Brugger (12 Feb 2013)
sub smalt {
  my ( $program ) = @_;
  
  my $version = `$program version | grep Version`;
  $version =~ s/Version: //;
  chomp( $version );
  return $version;
}



# 
# 
# 
# Kim Brugger (24 Oct 2013)
sub bwa {
  my ( $program ) = @_;
  
  my $version = `$program  2>&1 | head -n 3 | tail -n1`;
  $version =~ s/Version: //;
  chomp( $version );
  return $version;
}



  

# 
# 
# 
# Kim Brugger (24 Oct 2013)
sub gatk {
  my ( $program ) = @_;
  my $version = `$program --version`;
  chomp($version);
  $version =~ s/.*\(GATK\) //;
  $version =~ s/, Compiled.*//;
  return $version;
}



1;



