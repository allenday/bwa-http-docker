#!/bin/bash

if [[ -z $BWA_FILES ]]; then
  echo "\$BWA_FILES not set"
else

  if [[   $BWA_FILES =~ ^gs://    ]]; then
    echo "using gsutil to retrieve BWA_FILES='$BWA_FILES'"
    gsutil -m cp $BWA_FILES /data/
  elif [[ $BWA_FILES =~ ^http://  ||  $BWA_FILES =~ ^https:// ]]; then
    echo "using wget to retrieve BWA_FILES='$BWA_FILES'"
    wget --directory-prefix=/data/ $BWA_FILES
  else
    echo "unsupported scheme for BWA_FILES='$BWA_FILES'"
  fi

  if [[ $BWA_FILES =~ .tar.gz$ ]]; then
    echo "untar/gunzip BWA_FILES='$BWA_FILES'"
    tar -C /data/ -xvzf $BWA_FILES
  fi

fi

/usr/sbin/apache2ctl -D FOREGROUND
