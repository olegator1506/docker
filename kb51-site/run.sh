#!/bin/sh
html_path=/net/users/artem/work/site-kb51
db_path=/home/artem/work/docker/kb51-site/mysql/db
nginx_conf_path=/home/artem/work/docker/kb51-site/nginx/conf
net_name=site-kb51
case $1 in
    build)
	docker build -t kb51-site/mysql mysql
	docker build -t kb51-site/perl-fcgi perl-fcgi
	;;
    start)
## MySQL
	docker run \
	    --name mysql \
	    -e MYSQL_ROOT_PASSWORD=dct_[thyz \
	    -e MYSQL_DATABASE=site_kb51 \
	    -e MYSQL_USER=www \
	    -e MYSQL_PASSWORD=ghtk.,jltq \
	    -dp 3306:3306  \
	    -v ${db_path}:/var/lib/mysql \
	    --rm \
	    --net ${net_name} \
	    kb51-site/mysql
## Perl fastCGI
	docker run \
	    -dp 8999:8999 \
	    -v ${html_path}:/html \
	    --name perl-fcgi \
	    --rm \
	    --net ${net_name} \
	    kb51-site/perl-fcgi
## NGINX
    docker run \
        -p 80:80 \
        -v ${html_path}:/usr/share/nginx/html \
        -v ${nginx_conf_path}:/etc/nginx \
       --rm \
        -d \
        --name nginx \
	--net ${net_name} \
        nginx
	;;
    stop)
	docker kill nginx
    	docker kill perl-fcgi
	docker kill mysql
	;;
esac
