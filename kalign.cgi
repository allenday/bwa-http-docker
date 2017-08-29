#!/usr/bin/perl
use strict;
use CGI qw();
use File::Temp qw();

$CGI::POST_MAX = 50 * 1024 * 1024; #50MB

my $fasta_fh = CGI::param('fasta');

if ( ! $fasta_fh ) {
  print CGI::header(-status=>400);
  exit(0);
}

my (undef, $tempfile) = File::Temp::tempfile();
open( F, ">$tempfile.fa" );
while ( my $line = <$fasta_fh> ) {
  print F $line;
}
close( F );

system( "kalign kalign -gpo 60 -gpe 10 -tgpe 0 -bonus 0 -q -i $tempfile.fa -o $tempfile.out" );
open( B, "$tempfile.out" );
print CGI::header('text/plain');
while ( my $line = <B> ) {
  print $line;
}

unlink "$tempfile.fa";
unlink "$tempfile.out";
