#!/bin/sh
#docker run -it -v $(pwd)/share:/var/www/ -p 8000:8000 --name auth-center iss/auth-center bash
docker run --rm -it -p 8999:9000 \
-v /home/artem/work/web/inet-portal/sites/auth-center:/var/www/html \
-v /home/artem/work/web/php-lib:/usr/local/share/php:ro \
 --name php-fpm php-fpm:latest 
