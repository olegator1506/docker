#!/bin/sh
#docker run -it -v $(pwd)/share:/var/www/ -p 8000:8000 --name auth-center iss/auth-center bash
docker run --rm -it -p 8999:8999 -v /home/artem/work:/application --name php-fpm artem/php7.4-fpm-v2 