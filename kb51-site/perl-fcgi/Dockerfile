FROM perl:5.20
RUN apt update
RUN apt -y install libfcgi-perl unixodbc tdsodbc
RUN cpan JSON/Parse.pm DBI
COPY odbc.ini /etc
COPY fastcgi-wrapper.pl /opt
EXPOSE 8999
WORKDIR /opt
CMD [ "/opt/fastcgi-wrapper.pl" ]

