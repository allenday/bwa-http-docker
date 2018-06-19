#!/bin/bash

openssl genrsa -des3 -passout pass:x -out /etc/apache2/ssl/pass.key 2048
openssl rsa -passin pass:x -in /etc/apache2/ssl/pass.key -out /etc/apache2/ssl/server.key
cat /tmp/ssl-info.txt | openssl req -new -key /etc/apache2/ssl/server.key -out /etc/apache2/ssl/server.csr
openssl x509 -req -days 365 -in /etc/apache2/ssl/server.csr -signkey /etc/apache2/ssl/server.key -out /etc/apache2/ssl/server.crt

if [[ -z $BWA_FILES ]]; then
  echo "\$BWA_FILES not set"
else

  if [[   $BWA_FILES =~ ^gs://    ]]; then
    echo "using gsutil to retrieve BWA_FILES='$BWA_FILES'"
    gsutil -m cp $BWA_FILES /data/ && touch /data/ok
  elif [[ $BWA_FILES =~ ^http://  ||  $BWA_FILES =~ ^https:// ]]; then
    echo "using wget to retrieve BWA_FILES='$BWA_FILES'"
    wget --directory-prefix=/data/ $BWA_FILES && touch /data/ok
  else
    echo "unsupported scheme for BWA_FILES='$BWA_FILES'"
  fi

  #if [[ $BWA_FILES =~ .tar.gz$ ]]; then
  #  echo "untar/gunzip BWA_FILES='$BWA_FILES'"
  #  tar -C /data/ -xvzf $BWA_FILES
  #fi

fi

/usr/sbin/apache2ctl -D FOREGROUND
