#!/bin/bash 

cert_config="${1:-$( dirname ${0} )/self_cert.conf}" 
if [[ -r ${cert_config} ]]
then

  # Generate ca + server keys
  # ec by default otherwise RSA
  algorithm="${2:-ed25519}" 
  if [[ "${algorithm}" == "ed25519" ]]
  then 
    openssl genpkey -algorithm ${algorithm} -out ca-key.pem
    # openssl pkey -in ca-key-priv.pem -pubout >ca-key.pub
    openssl genpkey -algorithm ${algorithm} -out server-key.pem
    # openssl pkey -in server-key-priv.pem -pubout >server-key.pub
  else
    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out ca-key.pem 
    openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out server-key.pem
  fi

  # Generate CA cert
  openssl req -new -x509 -batch -nodes -config "${cert_config}" -days 666 -key ca-key.pem -out ca-cert.pem

  # Generate server cert req
  openssl req -new -nodes -config "${cert_config}" -key server-key.pem -out server-req.pem

  # Use CA cert to sign server req and generate server cert
  openssl x509 -req -in server-req.pem -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem

else

  echo -ne "\nCan't find conf file: ${cert_config}!\n\n" >&2
  exit 1

fi
