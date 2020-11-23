FROM perl:5.26
RUN apt update
RUN apt -y install unixodbc unixodbc-dev tdsodbc mc nano net-tools telnet
RUN /usr/local/bin/cpan JSON:Parse DBI LWP/UserAgent.pm DBD:ODBC FCGI
RUN cd /usr/include;/usr/local/bin/h2ph -a syscall.h
COPY odbc.ini /etc
COPY fastcgi-wrapper.pl /opt
EXPOSE 8999
WORKDIR /opt
CMD [ "/opt/fastcgi-wrapper.pl" ]


