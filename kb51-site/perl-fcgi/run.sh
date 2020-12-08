#!/bin/sh
docker run  -it --rm -v /data/web/html/main:/usr/share/nginx/html:ro -p 8998:8999  --net site-kb --name perl-fcgi site-kb/perl-fcgi
