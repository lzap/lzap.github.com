---
type: "post"
aliases:
- /2019/09/testing-tls-ca-server-and-client-certs.html
date: "2019-09-05T00:00:00Z"
tags:
- linux
- fedora
title: Testing TLS CA, server and client certs
---

I need a X509 CA, server and client certificate quite often during my
day-to-day work on Foreman, Smart Proxy and managed nodes. Up until now, I've
been using "puppet cert" command which was pretty useful utility for simple
X509 management, however it has been moved to puppet server package which I
don't want to install on my workstation.

Well, it turns out that in 2019 it's still a challenge to figure out OpenSSL
commands to generate certificates. I've been struggling a bit but with some
help of Tomas Mraz of Red Hat I was finally able to find last missing bits (V3
extensions). So I present you a script which generates *testing* certificates:

* A self-signed CA
* A server TLS certificate
* A client TLS certificate

All you need to do is to set SERVER_CN and CLIENT_CN variables and that's it:

    ./generate_example_certs server.example.com client.example.com

Here is the script:

    #!/bin/bash -e

    # server certificate common name (hostname)
    SERVER_CN=${1:-box.home.lan}

    # client certificate common name (hostname, uuid)
    CLIENT_CN=${2:-client1}

    SUBJECT="/C=US/ST=CA/O=Example.com"
    CA_CN="Example CA"
    DAYS=9999
    PASSCA=pass:password_ca
    PASSSV=pass:password_server
    PASSCT=pass:password_client

    # ca.crt
    openssl genrsa -passout $PASSCA -des3 -out ca.key 4096
    openssl req -passin $PASSCA -new -x509 -days $DAYS \
      -key ca.key -out ca.crt -subj "$SUBJECT/CN=${CA_CN}"
    openssl x509 -purpose -in ca.crt
    openssl x509 -in ca.crt -out ca.pem -outform PEM

    # server.crt
    openssl genrsa -passout $PASSSV -des3 -out server.key 4096
    openssl req -passin $PASSSV -new -key server.key -out server.csr \
      -subj "$SUBJECT/CN=${SERVER_CN}"
    openssl x509 -req -passin $PASSCA -extfile /etc/pki/tls/openssl.cnf \
      -extensions usr_cert -days $DAYS -in server.csr \
      -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt
    openssl x509 -purpose -in server.crt
    openssl rsa -passin $PASSSV -in server.key -out server.key
    openssl x509 -in server.crt -out server.pem -outform PEM

    # client.crt
    openssl genrsa -passout $PASSCT -des3 -out client.key 4096
    openssl req -passin $PASSCT -new -key client.key \
      -out client.csr -subj "$SUBJECT/CN=${CLIENT_CN}"
    openssl x509 -req -passin $PASSCA -days $DAYS \
      -extfile /etc/pki/tls/openssl.cnf -extensions usr_cert \
      -in client.csr -CA ca.crt -CAkey ca.key -set_serial 02 -out client.crt
    openssl x509 -purpose -in client.crt
    openssl rsa -passin $PASSCT -in client.key -out client.key
    openssl x509 -in client.crt -out client.pem -outform PEM

    # print and verify
    openssl x509 -in ca.crt -text -noout
    openssl x509 -in server.crt -text -noout
    openssl x509 -in client.crt -text -noout
    openssl verify -CAfile ca.crt server.crt
    openssl verify -CAfile ca.crt client.crt

Have fun! And remember, never generate production certificates this way. This
is meant only for development or testing environments.
