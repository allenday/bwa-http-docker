#!/usr/bin/perl
use strict;
use CGI qw();
use File::Temp qw();

$CGI::POST_MAX = 50 * 1024 * 1024; #50MB

my $input_fh = CGI::param('fasta');

if ( ! $input_fh ) {
  print CGI::header(-status=>400);
  exit(0);
}

my $bytes = 0;
my $head = undef;
my (undef, $tempfile) = File::Temp::tempfile();
open( F, ">$tempfile.fa" );

if ( defined(fileno($input_fh)) ) {
  while ( my $line = <$input_fh> ) {
    $head ||= $line;
    $bytes += length($line);
    print F $line;
  }
}
else {
  $bytes += length($input_fh);
  print F $input_fh;
}
close( F );

print STDERR "input_bytes=$bytes\nhead=$head";

system( "kalign kalign -gpo 60 -gpe 10 -tgpe 0 -bonus 0 -q -i $tempfile.fa -o $tempfile.out" );
open( B, "$tempfile.out" );
print CGI::header('text/plain');
while ( my $line = <B> ) {
  print $line;
}

unlink "$tempfile.fa";
unlink "$tempfile.out";
