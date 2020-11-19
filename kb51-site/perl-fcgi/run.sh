#!/bin/sh
docker run -it --rm -v $(pwd)/share:/share  --name site-kb site-kb/perl-fcgi bash
