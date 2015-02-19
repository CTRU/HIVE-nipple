package CTRU::Git;
# 
# Some simple git interaction scripts.
# 
# If this file is included and it is not in the master branch a warning will come.
# 
# Kim Brugger (13 May 2011), contact: kim.brugger@easih.ac.uk

use strict;
use warnings;


# 
# Find the git version of the program using the EASIH::Git package otherwise the package
# given as argument 
#
# Kim Brugger (20 Sep 2010)
sub version {
  my ( $module ) = @_;

  my $file = $0;

  if ( $module ) {
    my $mfile = $module;
    $mfile =~ s/::/\//;
    $mfile =~ s/\;//;
    $mfile .= ".pm";
    $file = $INC{ $mfile };
    
    return "Cannot find version for '$module' it is not loaded\n" if ( ! $file );

  }

  my $sha1   = "Unknown";
  my $TAG = "";

  if ($file && $file =~ /(.*)\//) {
    $sha1 = `cd $1; git describe --always 2> /dev/null`;
  }
  else {
    $sha1 = `git describe --always 2> /dev/null`;
  }

  chomp( $sha1     );

  return "$sha1";
}


1;



