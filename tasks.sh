#!/usr/bin/env bash

dependencies(){
  echo "[+] installing/upgrading dependency packages"

  pip install --upgrade \
    pyyaml \
    google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib
}

case $1 in
  dep*)
    dependencies
    ;;
  **)
    echo "unknown option: ${1}"
    exit 123
    ;;
esac
