#!/usr/local/bin/perl
use lib qw(.);
require "module.cgi";
use DBI;

kb51_package::read_input();
print "$]";
# my $ConnectRes = kb51_package::db_Connect();
my $ConnectRes = kb51_package::db_Connect_MIS();

if ($ConnectRes eq 'true')
  {

    print "MISW connected\n";
 }
else
  {
    kb51_package::Show_Connect_Result("Error connecting DB", 0, 1);
  }
