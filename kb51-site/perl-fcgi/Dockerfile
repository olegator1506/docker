FROM perl:5.26
RUN apt update
RUN apt -y install libfcgi-perl unixodbc unixodbc-dev tdsodbc libdbd-mysql-perl libdbd-odbc-perl mc nano net-tools telnet
RUN cpan JSON:Parse DBI LWP/UserAgent.pm DBD:ODBC 
COPY odbc.ini /etc
COPY fastcgi-wrapper.pl /opt
EXPOSE 8999
WORKDIR /opt
CMD [ "/opt/fastcgi-wrapper.pl" ]

