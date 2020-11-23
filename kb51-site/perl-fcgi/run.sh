#!/bin/sh
docker run  --rm -v $(pwd)/share:/share -p 8999:8999 --name site-kb site-kb/perl-fcgi 
