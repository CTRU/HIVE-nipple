#!/usr/bin/perl 
# 
# Map/realign/indels/snps integrated pipeline
# 
# 
# Kim Brugger (27 Jul 2010), contact: kim.brugger@easih.ac.uk

# BEGIN {
#   use vars qw/$path/; 
#   $path = $0;
#   if ($path =~ /.*\//) {
#     $path =~ s/(.*\/).*/$1/;
#   }
#   else {
#     $path = "./";
#   }
#   print "$path\n";
#   push @INC, $path;
# }

use strict;
use warnings;
use Data::Dumper;

use Getopt::Std;

use lib '/software/packages/ctru-pipeline/modules';
use lib '/software/packages/ctru-clinical/modules';

use CTRU::Git;
use CTRU::Pipeline;
use CTRU::Versions;
use CTRU::Pipeline::Misc;

my $VERSION = "1.51";

my $opts = 'Q:';
my %opts;
getopts($opts, \%opts);

my $username = scalar getpwuid $<;

my $samtools        = '/software/bin/samtools';#EASIH::Pipeline::Misc::find_program('samtools');
my $picard          = '/software/bin/picard';
my $smalt           = '/software/bin/smalt-0.7.6';
my $cutadapt      = '/software/packages/cutadapt-1.1/bin/cutadapt';

use File::Basename;
my $pipeline_dir = dirname($0);
my $script_dir  = "$pipeline_dir/../scripts";

#print "Script root: $script_dir\n";

usage() if ( $opts{h} || ! $opts{Q});

my $CP_run = "unknown";

my @consensus_regions = ();
# if using standard naming, this is a lot easier.
if ( $opts{Q} ) {

  $opts{Q} =~ s/(.*?)\..*/$1/;
  

  if ($opts{'Q'} =~ /^C06/ ) {
    $opts{ 'R' } = '/refs/HIV/K03455.fasta';
    $opts{ 'r' } = '/refs/HIV/K03455_s1k6';
    @consensus_regions = ('2253 4227', '4232 5099');

  }
  elsif ($opts{'Q'} =~ /^C11/ ) {
    $opts{ 'R' } = '/refs/HSV/TK.fasta';
    $opts{ 'r' } = '/refs/HSV/TK_s1k6';
    @consensus_regions = ('1 1128');
  }
  elsif ($opts{'Q'} =~ /^C19/ ) {
    $opts{ 'R' } = '/refs/CMV/CMV_AD169.fasta';
    $opts{ 'r' } = '/refs/CMV/CMV_AD169_s1k6';
    @consensus_regions = ('80631 76906', '141740 142418');
  }
  else {
    $opts{ 'R' } = '/refs/HIV/K03455.fasta';
    $opts{ 'r' } = '/refs/HIV/K03455_s1k6';
    @consensus_regions = ('2253 4227', '4232 5099');
  }


  $opts{'1'} = glob("$opts{Q}*.1.fq.gz");
  $opts{'2'} = glob("$opts{Q}*.2.fq.gz");

  if ( ! $opts{'1'} ) {
    $opts{'1'} = glob("$opts{Q}*.1.fq");
    $opts{'2'} = glob("$opts{Q}*.2.fq");
  }


  $opts{'L'} = "$opts{Q}.log";
  $opts{'E'} = "$opts{Q}.error.log";
  $opts{'o'} = "$opts{Q}";
  $opts{'l'} = 1;
  $opts{'m'} = 1;

  CTRU::Pipeline::set_project_name("P".$opts{'Q'});

  my $path = `pwd`;
  if ( $path =~ /(CP\d+.*)\// ) {
    $CP_run = $1;
  }
  elsif ( $opts{Q} =~ /(CP\d+.*)\//) {
    $CP_run = $1;
  }

}  


my $first            = $opts{'1'}     || usage();
my $second           = $opts{'2'}     || usage();
my $platform = 'ILLUMINA';
my $reference        = $opts{'R'}     || usage();
my $smalt_reference  = $opts{'r'}     || usage();

my $log              = $opts{'L'};
my $error_log        = $opts{'E'};


open (*STDOUT, ">> $log")       || die "Could not open '$log': $!\n" if ( $log );
open (*STDERR, ">> $error_log") || die "Could not open '$error_log': $!\n" if ( $log );

my $out = $opts{o} || $first;
$out =~ s/.1.fq//;
$out =~ s/.gz//;

my $bam_file = "$out.bam";

my $host_cpus      = nr_of_cpus();

use CTRU::ComplexLog;
CTRU::Pipeline::logger('CTRU::ComplexLog');
$CTRU::Pipeline::logger->level('fatal');
$CTRU::Pipeline::logger->level('debug');


my $run_id = "---";


open (*STDOUT, ">> $log") || die "Could not open '$log': $!\n" if ( $log );


#validate_input();

#CTRU::Pipeline::backend('Local');
#CTRU::Pipeline::max_jobs( $host_cpus );
#CTRU::Pipeline::max_retry(0);

CTRU::Pipeline::backend('SGE');

CTRU::Pipeline::add_start_step('trim_reads');
CTRU::Pipeline::add_merge_step('trim_reads','smalt');
CTRU::Pipeline::add_step('smalt', 'bam_sort');
CTRU::Pipeline::add_step('bam_sort', 'mark_dups');
CTRU::Pipeline::add_step('mark_dups', 'fix_indels');
CTRU::Pipeline::add_step('fix_indels', 'bam_reheader');
CTRU::Pipeline::add_step('bam_reheader', 'bam_index');

CTRU::Pipeline::add_step('bam_index', 'isize');
CTRU::Pipeline::add_merge_step('isize', 'mapping_stats');
CTRU::Pipeline::add_step('bam_index', 'flagstats');
CTRU::Pipeline::add_merge_step('flagstats', 'mapping_stats');
CTRU::Pipeline::add_merge_step('mapping_stats', 'finish');

CTRU::Pipeline::add_step('bam_index', 'QC');
CTRU::Pipeline::add_step('QC', 'finish');


CTRU::Pipeline::add_step('bam_index', 'bam_consensus');
CTRU::Pipeline::add_step('bam_index', 'bam_codons');
CTRU::Pipeline::add_merge_step('bam_consensus', 'finish');
CTRU::Pipeline::add_merge_step('bam_codons', 'finish');


#CTRU::Pipeline::print_flow();
#exit;


CTRU::ComplexLog->info( {'ctru-pipeline' => CTRU::Pipeline::version(), 
			 'ctru-clinical' => "$VERSION-".CTRU::Git::version(), 
			 "smalt"         => CTRU::Versions::smalt( $smalt ),
			 'samtools'      => CTRU::Versions::samtools( $samtools ),
			 'picard'        => CTRU::Versions::picard( $picard ),
			 'type'          => 'versions'});


&CTRU::Pipeline::run();

&CTRU::Pipeline::store_state();




# 
# 
# 
# Kim Brugger (12 Feb 2013)
sub trim_reads {
  
  
  my $tmp_fa1  = CTRU::Pipeline::tmp_file(".fq.gz");
  my $cmd = "$cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT $first | gzip -c > $tmp_fa1 ";
  CTRU::Pipeline::submit_job( $cmd, $tmp_fa1 ); 

  my $tmp_fa2  = CTRU::Pipeline::tmp_file(".fq.gz");
  $cmd = "$cutadapt -b TGTAGAACCATGTCGTCAGTGT -b AGACCAAGTCTCTGCTACCGT $second | gzip -c > $tmp_fa2 ";
  CTRU::Pipeline::submit_job( $cmd, $tmp_fa2 ); 

}


# 
# 
# 
# Kim Brugger (05 Oct 2012)
sub smalt {
  my ( $input ) = @_;

  print Dumper( $input );

  my ( $trimmed_first, $trimmed_second ) = @$input;

  my $tmp_bam  = CTRU::Pipeline::tmp_file(".bam");
  my $cmd = "$smalt map -n 14 -f sam $smalt_reference $trimmed_first $trimmed_second | egrep -v \\\# | $samtools view -t $reference.fai -Sb - > $tmp_bam";

#  print STDERR "$cmd\n";

  CTRU::Pipeline::submit_job($cmd, "$tmp_bam", "t=16", "$trimmed_first $trimmed_second");

}


sub bam_index {
  my ($input) = @_;

  my $cmd = "$samtools index $input";
  CTRU::Pipeline::submit_job($cmd, $input);
}


sub bam_reheader {

  my $picard_version   = CTRU::Versions::picard( $picard );
  my $samtools_version = CTRU::Versions::samtools( $samtools );
  my $smalt_version    = CTRU::Versions::smalt( $smalt ),;

  my $tmp_new  = CTRU::Pipeline::tmp_file(".sam.header");
  print "$tmp_new\n";
  open( my $out, "> $tmp_new") || die "Could not open '$tmp_new':$!\n";
  open( my $in, "$samtools view -H $bam_file| ") || die "Could not open '$bam_file': $!\n";
  my $done_GATK_indel_line = 0;
  while(<$in>) {
    if (1 || !/GATK/) {
      print $out $_;
    }
  }
  close ($in);

  print $out join("\t", '@PG', "ID:picard", "VN:$picard_version") . "\n";
  print $out join("\t", '@PG', "ID:samtools", "VN:$samtools_version") . "\n";
#  print $out join("\t", '@PG', "ID:smalt", "VN:$smalt_version") ."\n";

  print $out join("\t", '@PG', "ID:ctru-pipeline", "VN:" . &CTRU::Pipeline::version()) . "\n";
  print $out join("\t", '@PG', "ID:ctru-clinical", "VN:$VERSION-" . &CTRU::Git::version()) . "\n";


  close($out);

  my $tmp_bam  = CTRU::Pipeline::tmp_file(".bam");

  my $cmd1 = "$samtools reheader $tmp_new $bam_file > $tmp_bam; mv -f $tmp_bam $bam_file";

  CTRU::Pipeline::submit_system_job($cmd1, $bam_file);
  
}


# 
# 
# 
# Kim Brugger (25 Jun 2012)
sub bam_sort {
  my ($input) = @_;

  my $readgroup = $out;
  $readgroup =~ s/\.gz//;
  $readgroup =~ s/\.[1|2].fq//;
  
  my $sample = $readgroup;
  $sample =~ s/\..*//;
  $sample =~ s/_\d*//;

  my $tmp_bam  = CTRU::Pipeline::tmp_file(".bam");
  my $cmd = "$picard -T AddOrReplaceReadGroups.jar I=$input O=$tmp_bam SORT_ORDER=coordinate CN=CTRU PL=$platform LB=$readgroup PU=$run_id  SM=$out VALIDATION_STRINGENCY=SILENT CREATE_INDEX=false";  

  print "$cmd\n";

  CTRU::Pipeline::submit_job($cmd, $tmp_bam);
}



# 
# 
# 
# Kim Brugger (12 Feb 2013)
sub fix_indels {
  my ($input) = @_;
  
  my $tmp_bam  = CTRU::Pipeline::tmp_file(".bam");
  my $cmd = "$script_dir/bam_fix_indels.pl $input $tmp_bam; mv -f $tmp_bam $input";

  CTRU::Pipeline::submit_job($cmd, $input);
}


# 
# 
# 
# Kim Brugger (12 Feb 2013)
sub bam_consensus {
  my ($input) = @_;


  if ( @consensus_regions ) {

    my $out_file = $input;
    $out_file =~ s/.bam/_consensus.fasta/;
    my $cmd = "";
  
    foreach my $consensus_region (@consensus_regions) {
      
      $cmd    .= "$script_dir/Bam_consensus.py $input $consensus_region  >> $out_file;";
    }


    CTRU::Pipeline::submit_job($cmd, $input) ;
  }
  else {
    CTRU::Pipeline::submit_system_job("sleep 1") ;
  }
}


# 
# 
# 
# Kim Brugger (12 Feb 2013)
sub bam_codons {
  my ($input) = @_;
  
  my $out_file = $input;
  $out_file =~ s/.bam/_codons.xls/;
  my $cmd = "$script_dir/codon_usage.py $input > $out_file";

  CTRU::Pipeline::submit_job($cmd, $input);
}




# 
# 
# 
# Kim Brugger (12 Feb 2013)
sub finish {
  my ($input) = @_;

  CTRU::Pipeline::submit_system_job("sleep 1");
  
}



# 
# 
# 
# Kim Brugger (25 Jun 2012)
sub mark_dups {
  my ($input) = @_;

  my $username = scalar getpwuid $<;
  my $metrix_file = CTRU::Pipeline::tmp_file(".mtx");
  my $cmd = "$picard -T MarkDuplicates  I=$input O=$bam_file  M= $metrix_file VALIDATION_STRINGENCY=SILENT TMP_DIR=/tmp/ MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=true ASSUME_SORTED=Boolean ";
  print STDERR "$cmd\n";
  CTRU::Pipeline::submit_job($cmd, $bam_file);
}





# 
# Ensure that the reference and it auxiliary files are all present.
# 
# Kim Brugger (02 Aug 2010)
sub validate_input {
  
  my @errors;
  my @info;

  
  push @errors, "$first does not exist"  if ( ! -e $first );
  
  push @errors, "$second does not exist"  if ( ! $second );

  # Things related to the reference sequence being used.
  
  push @errors, "GATK expects references to end with 'fasta'." 
      if ( $reference !~ /fasta\z/);

  my ($dir, $basename, $postfix) = (".","","");
  if ( $reference =~ /\//) {
    ($dir, $basename, $postfix) = $reference =~ /^(.*)\/(.*?)\.(.*)/;
  }
  else {
    ($basename, $postfix) = $reference =~ /^(.*?)\.(.*)/;
  }
  
  push @errors, "GATK expects and references dict file (made with Picard), please see the GATK wiki $dir/$basename.dict\n" 
      if ( ! -e "$dir/$basename.dict");
  
  # Check that the bam_file ends with bam, or add it
  if ( $bam_file !~ /bam\z/) {
    push @info, "Added bam postfix so '$bam_file' becomes '$bam_file.bam'";
    $bam_file .= ".bam";
  }


  push @errors, "Platform must be either ILLUMINA or PGM not '$platform'" if ( $platform ne "ILLUMINA" && $platform ne 'PGM');


  # print the messages and die if critical ones.
  die join("\n", @errors) . "\n"   if ( @errors );
  print  join("\n", @info) . "\n"   if ( @info );
}



# 
# 
# 
# Kim Brugger (09 Nov 2012)
sub flagstats {
  
  my $cmd = "$samtools flagstat $bam_file > $bam_file.flagstat";
  CTRU::Pipeline::submit_job($cmd, "$bam_file.flagstat");
}


# 
# 
# 
# Kim Brugger (02 Oct 2013)
sub isize {

  my $cmd = "$picard -T CollectInsertSizeMetrics.jar I= $bam_file O= $bam_file.isize H= $bam_file.isize.pdf VALIDATION_STRINGENCY=SILENT \n";
  CTRU::Pipeline::submit_job($cmd, "$bam_file.isize");
}



# 
# 
# 
# Kim Brugger (02 Oct 2013)
sub QC {

  my $cmd = "$script_dir/VIRUS_sample_QC.py $bam_file";
  CTRU::Pipeline::submit_job($cmd);
}



# 
# 
# 
# Kim Brugger (02 Oct 2013)
sub mapping_stats {

  my $flagstat_file = "$bam_file.flagstat";
  my $isize_file    = "$bam_file.isize";

  print "flagstat_file $isize_file \n";

  my $flag_hash = flagstat_entry( $flagstat_file );
  if ( -e $isize_file ) {
      my $isize_hash = isize_stats($isize_file);
      
      # delete gunk I dont want
      delete $$isize_hash{ library };
      delete $$isize_hash{ read_group };
      
      # merge the two hashes
      map { $$flag_hash{ $_ } = $$isize_hash{ $_ } } keys %$isize_hash;
  }

  $$flag_hash{ 'plate'  }  = $CP_run;
  $$flag_hash{ 'sample' }  = $out;
  $$flag_hash{ 'type'   }  = "mapping_stats";


  print Dumper( $flag_hash );

  # Hijacking to logging system to put some mapping stats to the rabbitmq
  CTRU::ComplexLog->info( $flag_hash );
  CTRU::Pipeline::submit_system_job("sleep 1");
}


# 
# 
# 
# Kim Brugger (27 Sep 2013)
sub flagstat_entry {
  my ($file ) = @_;
  my %res;
  open (my $in, $file) || die "Could not open '$file': $!\n";
  while(<$in>) {
    if ( /(\d+) .*total/) {
      $res{total_reads} = $1;
    }
    elsif ( /(\d+) .*dups/) {
      $res{dup_reads} = $1;
    }
    elsif ( /(\d+) .*mapped \((.*?)%/) {
      $res{mapped_reads} = $1;
      $res{mapped_perc} = $2;
    }
    elsif ( /(\d+) .*properly paired/) {
      $res{properly_paired} = $1;
    }
    elsif ( /(\d+) .*singletons/) {
      $res{singletons} = $1;
    }
  }
  close( $in );

  $res{ type } = 'mapping_stats';

  return \%res;
}


# 
# 
# 
# Kim Brugger (30 Sep 2013)
sub isize_stats {
  my ($file) = @_;

  my %res;

  my @rows;

  open( my $in, $file) || die "Could not open '$file': $!\n";
  while(<$in>) {
    chomp;
    if ( /^MEDIAN_INSERT_SIZE/) {
      @rows = split("\t");
      $_ = <$in>;
      chomp;
      my @fields = split("\t");

      for( my $i=0;$i< @rows;$i++) {
	$res{ lc($rows[ $i ])} = $fields[ $i ];
      }
      last;
    }
  }
  close( $in );
    
  return \%res;
  
}




# 
# 
# 
# Kim Brugger (13 Jan 2011)
sub nr_of_cpus {

  my $cpus = `cat /proc/cpuinfo | egrep ^proc | wc -l`;
  chomp $cpus;
  return $cpus;
}






# 
# 
# 
# Kim Brugger (22 Apr 2010)
sub usage {

  my $script = $0;
  $script =~ s/.*\///;
  print "USAGE: $script -Q [base sample name]\n";

  print "\n";

  print "Samtools: " . CTRU::Versions::samtools( $samtools ) ."\n";
  print "Picard: " . CTRU::Versions::picard( $picard ) ."\n";
  print "Smalt: " . CTRU::Versions::smalt( $smalt ) ."\n";

  print "ctru-pipeline: " . &CTRU::Pipeline::version() . "\n";

  print "ctru-clinical: $VERSION-" . &CTRU::Git::version() . "\n";

  print "@ARGV \n";

  exit;

}
