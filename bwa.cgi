#!/usr/bin/perl
use strict;
use CGI qw();
use File::Temp qw();

$CGI::POST_MAX = 50 * 1024 * 1024; #50MB

my $input_fh = CGI::param('fastq');
my $database = CGI::param('database');
my $args     = CGI::param('args') || '';

#no args
if ( !$input_fh || !$database ) {
  #load balancer request, ok
  if ( -f "/data/ok" ) {
    print CGI::header(-status=>200);
    print CGI::header('text/plain');
    print "OK\n";
    exit(0);
  }
  #regular request, user error
  else {
    print CGI::header(-status=>400);
    exit(0);
  }
}

my $bytes = 0;
my $head = undef;
my (undef, $tempfile) = File::Temp::tempfile();
open( F, ">$tempfile.fq" );

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

system( "bwa mem $args /data/$database $tempfile.fq > $tempfile.out" ) == 0
        or die "'bwa mem' exited with non zero code";
open( B, "$tempfile.out" );
print CGI::header('text/plain');
while ( my $line = <B> ) {
  print $line;
  if ( $line !~ m/^[@#]/ ) {
    print STDERR "hit=$line";
  }
}

unlink "$tempfile.fq";
unlink "$tempfile.out";
