---
type: "post"
aliases:
- /2021/03/letsencrypt-a-fedora-server.html
date: "2021-03-31T00:00:00Z"
tags:
- linux
- fedora
title: Letsencrypt a Fedora server
---

I was looking for a simple letsencrypt tutorial for my home server running
Fedora but it looks like the official (and quite capable) certbot is not
availble in Fedora repos. So I have decided to go a more simple route of using
acme-tiny shell script which is present and does the same, at least if you are
running Apache httpd.

First off, install Apache httpd, SSL support and acme script itself:

    # dnf install httpd mod_ssl acme-tiny

Let's assume that the Apache server is already serving some files and is
available on the desired domain via HTTP (not HTTPS yet):

    # systemctl enable --now httpd
    # curl -s http://home.zapletalovi.com | grep -o "Test Page"
    Test Page

We are almost there, trust me. Generate a new certificate request. OpenSSL tool
will ask several questions like name, organization and this stuff. Make sure
that the Common Name (CN) is correct.

    # cd /etc/pki/tls
    # ln -s /var/lib/acme/csr .
    # openssl req -new -nodes -keyout private/home.zapletalovi.com.key -out csr/home.zapletalovi.com.csr
    # chmod 0400 private/home.zapletalovi.com.key

The next step is the actual communication with the authority, putting the
challenge hash into `/var/www/challenges` directory which is exported by Apache
httpd and downloading the signed request:

    # systemctl start acme-tiny

See system journal for any errors. If you encounter one, just start the script
manually but make sure to use acme user account not root:

    # su acme -s /bin/bash
    # /usr/libexec/acme-tiny/sign

And that's really all! You should have your certificate signed by letsencrypt
now. Configure the desired software to use the new certificate and the key from
the following paths:

    # find /var/lib/acme /etc/pki/tls/private
    /var/lib/acme
    /var/lib/acme/certs
    /var/lib/acme/certs/home.zapletalovi.com.crt
    /var/lib/acme/csr
    /var/lib/acme/csr/home.zapletalovi.com.csr
    /var/lib/acme/private
    /var/lib/acme/private/account.key
    /etc/pki/tls/private/home.zapletalovi.com.key

For example I want to actually configure the Apache httpd itself:

    # grep zapletalovi /etc/httpd/conf.d/ssl.conf
    SSLCertificateFile /var/lib/acme/certs/home.zapletalovi.com.crt
    SSLCertificateKeyFile /etc/pki/tls/private/home.zapletalovi.com.key

If you are like me and running under SELinux enforcing, make sure that the
newly generated certificates have the proper label:

    # semanage fcontext -a -f a -t cert_t '/var/lib/acme/certs(/.*)?'
    # restorecon -rv /var/lib/acme/certs

The final and the most important step - enable systemd timer which will
automatically extend the certificate for you:

    # systemctl enable --now acme-tiny.timer

That was easy.
