---
type: "post"
aliases:
- /2019/09/testing-tls-ca-server-and-client-certs.html
date: "2019-09-05T00:00:00Z"
tags:
- linux
- fedora
title: Testing MTLS CA, server and client certs
---

I needed a X509 CA, server and client certificate quite often during my
day-to-day work on Foreman, Smart Proxy and managed nodes. Up until now, I've
been using "puppet cert" command which was pretty useful utility for simple
X509 management, however it has been moved to puppet server package which I
don't want to install on my workstation.

Well, it turns out that in 2019 it's still a challenge to figure out OpenSSL
commands to generate certificates. I've been struggling a bit but with some
help of Tomas Mraz of Red Hat I was finally able to find last missing bits (V3
extensions). So I present you a script which generates *testing* certificates
for mutual TLS without key password:

* A self-signed CA
* A server TLS certificate with Subject Alternative Name
* A client TLS certificate with Subject Alternative Name

All you need to do is to execute a script (below) with two arguments: server
and client common names:

    ./generate_example_certs server.example.com client.example.com password

Here is the script:


```
#!/bin/bash -xe

# server certificate common name (hostname)
SERVER_CN=${1:-server.example.com}

# client certificate common name (hostname, uuid)
CLIENT_CN=${2:-client.example.com}

SUBJECT="/C=US/ST=CA/O=Example.com"
CA_CN="Example CA"
DAYS=9999
PASSWORD=${3:-password}
PASSCA=pass:$PASSWORD
PASSSV=pass:$PASSWORD
PASSCT=pass:$PASSWORD

# test-ca.crt
openssl genrsa -passout $PASSCA -des3 -out test-ca.key 4096
openssl req -passin $PASSCA -new -x509 -days $DAYS \
  -key test-ca.key -out test-ca.crt -subj "$SUBJECT/CN=${CA_CN}"
openssl x509 -purpose -in test-ca.crt
openssl x509 -in test-ca.crt -out test-ca.pem -outform PEM

# server.crt
openssl genrsa -passout $PASSSV -des3 -out $SERVER_CN-server.key 4096
openssl req -passin $PASSSV -new -key $SERVER_CN-server.key -out server.csr \
  -addext "subjectAltName = DNS:${SERVER_CN}" \
  -subj "$SUBJECT/CN=${SERVER_CN}"
openssl x509 -req -passin $PASSCA -extfile /etc/pki/tls/openssl.cnf \
  -extensions usr_cert -days $DAYS -in server.csr \
  -extensions SAN -extfile <(cat /etc/pki/tls/openssl.cnf <(printf "\n[SAN]\nsubjectAltName=DNS:${SERVER_CN}\n")) \
  -CA test-ca.crt -CAkey test-ca.key -set_serial 01 -out $SERVER_CN-server.crt
openssl x509 -purpose -in $SERVER_CN-server.crt
openssl rsa -passin $PASSSV -in $SERVER_CN-server.key -out $SERVER_CN-server.key
openssl x509 -in $SERVER_CN-server.crt -out $SERVER_CN-server.pem -outform PEM

# client.crt
openssl genrsa -passout $PASSCT -des3 -out $CLIENT_CN-client.key 4096
openssl req -passin $PASSCT -new -key $CLIENT_CN-client.key \
  -addext "subjectAltName = DNS:${CLIENT_CN}" \
  -out client.csr -subj "$SUBJECT/CN=${CLIENT_CN}"
openssl x509 -req -passin $PASSCA -days $DAYS \
  -extfile /etc/pki/tls/openssl.cnf -extensions usr_cert \
  -extensions SAN -extfile <(cat /etc/pki/tls/openssl.cnf <(printf "\n[SAN]\nsubjectAltName=DNS:${CLIENT_CN}\n")) \
  -in client.csr -CA test-ca.crt -CAkey test-ca.key -set_serial 02 -out $CLIENT_CN-client.crt
openssl x509 -purpose -in $CLIENT_CN-client.crt
openssl rsa -passin $PASSCT -in $CLIENT_CN-client.key -out $CLIENT_CN-client.key
openssl x509 -in $CLIENT_CN-client.crt -out $CLIENT_CN-client.pem -outform PEM

# print and verify
openssl x509 -in test-ca.crt -text -noout
openssl x509 -in $SERVER_CN-server.crt -text -noout
openssl x509 -in $CLIENT_CN-client.crt -text -noout
openssl verify -CAfile test-ca.crt $SERVER_CN-server.crt
openssl verify -CAfile test-ca.crt $CLIENT_CN-client.crt
```

Have fun! And remember, never generate production certificates this way. This
is meant only for development or testing environments.
