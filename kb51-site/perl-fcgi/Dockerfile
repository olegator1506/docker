FROM perl:5.26
RUN apt update
RUN apt -y install unixodbc unixodbc-dev tdsodbc mc nano net-tools telnet
RUN /usr/local/bin/cpan JSON:Parse DBI LWP/UserAgent.pm DBD:ODBC 
COPY odbc.ini /etc
COPY fastcgi-wrapper.pl /opt
EXPOSE 8999
WORKDIR /opt
CMD [ "/opt/fastcgi-wrapper.pl" ]


