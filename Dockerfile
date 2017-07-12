FROM google/cloud-sdk
MAINTAINER Allen Day "allenday@allenday.com"

EXPOSE 80

ENV IMAGE_PACKAGES="apache2 bwa gzip tar wget"

RUN apt-get -y update
RUN apt-get -y --no-install-recommends install $IMAGE_PACKAGES
RUN a2enmod cgi

RUN mkdir -p /data

RUN rm -rf /var/lib/apt/lists/*

COPY hello.cgi /usr/lib/cgi-bin/hello.cgi
RUN chmod +x /usr/lib/cgi-bin/hello.cgi

COPY bwa.cgi /usr/lib/cgi-bin/bwa.cgi
RUN chmod +x /usr/lib/cgi-bin/bwa.cgi

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT bash /entrypoint.sh $BWA_FILES
