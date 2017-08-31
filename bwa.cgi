#!/usr/bin/perl
use strict;
use CGI qw();
use File::Temp qw();

$CGI::POST_MAX = 50 * 1024 * 1024; #50MB

my $fastq_fh = CGI::param('fastq');
my $database = CGI::param('database');

if ( ! $fastq_fh || ! $database ) {
  print CGI::header(-status=>400);
  exit(0);
}

my $bytes = 0;
my $head = "";
my (undef, $tempfile) = File::Temp::tempfile();
open( F, ">$tempfile.fq" );
while ( my $line = <$fastq_fh> ) {
  $head ||= $line;
  $bytes += length($line);
  print F $line;
}
close( F );

print STDERR "fastq_bytes=$bytes\nhead=$head";

system( "bwa mem /data/$database $tempfile.fq > $tempfile.sam" );
open( B, "$tempfile.sam" );
print CGI::header('text/plain');
while ( my $line = <B> ) {
  print $line;
  if ( $line !~ m/^[@#]/ ) {
    print STDERR "hit=$line";
  }
}

unlink "$tempfile.fq";
unlink "$tempfile.sam";
