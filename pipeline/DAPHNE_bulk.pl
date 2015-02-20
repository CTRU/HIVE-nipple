#!/usr/bin/perl 
# 
# pipeline for few genes analysis, mainly for clinical use.
# 
# 
# Kim Brugger (17 Jan 2012), contact: kim.brugger@easih.ac.uk

use strict;
use warnings;
use Data::Dumper;

my $VERSION = '0.1';

BEGIN {
  use vars qw/$path/; 
  $path = $0;
  if ($path =~ /.*\//) {
    $path =~ s/(.*\/).*/$1/;
  }
  else {
    $path = "./";
  }
#  push @INC, $path;
}

use Getopt::Std;

use lib '/software/packages/easih-toolbox/modules';
use EASIH::Parallel;

use File::Basename;
my $pipeline_dir = dirname($0);
my $script_dir  = "$pipeline_dir/../scripts";


my @samples = glob("*.1.fq.gz");

#print Dumper( \@samples );

EASIH::Parallel::max_nodes( int( @samples ));
my $HIV_samples = 0;

my $exit_count = 5;
foreach my $sample ( @samples )  {

  EASIH::Parallel::command_push("/software/packages/ctru-clinical/pipeline/DAPHNE.pl -Q $sample" );
  $HIV_samples++;
}

EASIH::Parallel::run_parallel( 60, 1 );




EASIH::Parallel::command_push("python /software/packages/ctru-clinical_dev/scripts/HIV_XS_QC.py *_codons.xls") 
   if ( $HIV_samples );
EASIH::Parallel::run_parallel( 60, 1 );

my $cwd = `pwd`;
chomp( $cwd );

$cwd =~ s/(CP\d+.*)/$1/;


EASIH::Parallel::command_push("zip $1_PHE.zip *QC.pdf *fasta *xls crosssample_QC.xls");
EASIH::Parallel::run_parallel( 60, 1 );

print "All done!\n";
