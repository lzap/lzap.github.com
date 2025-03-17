---
title: "Generate testing MTLS certificates more easily"
date: 2024-11-20T15:48:23+01:00
type: "post"
tags:
- linux
- fedora
- rhel
---

I found a much better tool to generate testing X509 TLS certificates than [my own script](/posts/2019/testing-tls-ca-server-and-client-certs/) which by the way is not correct. Here is how to generate a MTLS pair for typical web testing:

```
#!/bin/bash -e

wget -nc https://raw.githubusercontent.com/redhat-qe-security/certgen/refs/heads/master/certgen/lib.sh
source lib.sh

x509KeyGen ca
x509KeyGen server
x509KeyGen client
x509SelfSign --notAfter "13 years" -t ca ca
x509CertSign --notAfter "13 years" --CA ca -t webserver server
x509CertSign --notAfter "13 years" --CA ca -t webclient client

openssl x509 -in ca/cert.pem -text -noout
openssl x509 -in server/cert.pem -text -noout
openssl x509 -in client/cert.pem -text -noout
openssl verify -CAfile ca/cert.pem server/cert.pem
openssl verify -CAfile ca/cert.pem client/cert.pem
```

Quick test, a server:

```
openssl s_server -accept 4433 -www \
    -CAfile ./ca/cert.pem \
    -cert ./server/cert.pem \
    -key ./server/key.pem
```

And a client:

```
openssl s_client -connect localhost:4433 \
    -CAfile ./ca/cert.pem \
    -cert ./client/cert.pem \
    -key ./client/key.pem
```

A python server:

```python
import http.server
import ssl

cert_dir = "."
cacert = cert_dir + "ca/cert.pem"
servercert = cert_dir + "server/cert.pem"
serverkey = cert_dir + "server/key.pem"
clientcert = cert_dir + "client/cert.pem"
clientkey = cert_dir + "client/key.pem"
httpd = http.server.HTTPServer(('127.0.0.1', 4433), http.server.SimpleHTTPRequestHandler)
ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=cacert)
ctx.load_cert_chain(certfile=servercert, keyfile=serverkey)
ctx.verify_mode = ssl.CERT_REQUIRED
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
httpd.serve_forever()
```

