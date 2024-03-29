---
type: "post"
aliases:
- /2022/11/lightweight-mastodon-instance-gotosocial.html
date: "2022-11-06T00:00:00Z"
tags:
- linux
- fedora
title: 'Lightweight Mastodon instance: gotosocial'
---

If you need a lightweight Mastodon instance, I have a tip for you:
[GoToSocial](https://docs.gotosocial.org/en/latest/) is an ActivityPub backend
written in Go, no dependencies needed, lightweight (well, 50MB binary) and can
store data in either SQLite3 or Postgres.

The setup is well documented, you can download pre-built binary, create an
empty directory, configure database connection and just run it. It has a
built-in support for Let's Encrypt, however, if you already have a domain with
existing web server and Let's Encrypt certificate, you can turn this feature off.

This was my case as I am running my domain on Apache2 httpd with
[acme-tiny](/2021/03/letsencrypt-a-fedora-server.html). On top of that, I also
wanted my instance running at `social.zapletalovi.com` available via redirect
from `zapletalovi.com` so my Mastodon account has a shorter name of
`@lukas@zapletalovi.com`. I thought I'd share the httpd configuration in case
you need to do the same:

        # cat /etc/httpd/conf.d/social.conf
        <VirtualHost *:80>
          ServerName social.zapletalovi.com

          RewriteEngine On
          RewriteCond %{HTTP:Upgrade} websocket [NC]
          RewriteCond %{HTTP:Connection} upgrade [NC]
          RewriteRule ^/?(.*) "ws://localhost:8080/$1" [P,L]

          ProxyPreserveHost On
          ProxyPassMatch ^/.well-known !
          ProxyPass / http://localhost:8080/
          ProxyPassReverse / http://localhost:8080/

          Alias /.well-known/acme-challenge/ "/var/www/challenges/"
        </VirtualHost>

The first section is HTTP config of the main site, the rewrite and proxy rules
are from the project configuration. I had to add ProxyPassMatch with Alias for
challenges from acme-tiny.

        <VirtualHost *:443>
          ServerName social.zapletalovi.com

          RewriteEngine On
          RewriteCond %{HTTP:Upgrade} websocket [NC]
          RewriteCond %{HTTP:Connection} upgrade [NC]
          RewriteRule ^/?(.*) "ws://localhost:8080/$1" [P,L]

          SSLEngine On
          SSLCertificateFile /var/lib/acme/certs/social.zapletalovi.com.crt
          SSLCertificateKeyFile /etc/pki/tls/private/social.zapletalovi.com.key

          ProxyPreserveHost On
          ProxyPass / http://localhost:8080/
          ProxyPassReverse / http://localhost:8080/

          RequestHeader set "X-Forwarded-Proto" expr=https
        </VirtualHost>

This is the HTTPS configuration as mentioned in the project documentation. Note
there are no acme-challenge aliases necessary as they are valid only for HTTP.
Do not forget to add SSL certificate and key. Note httpd will fail to start if
those files do not exist and are not valid SSL certs, that can be only done
after acme-tiny generates it.

        <VirtualHost *:80>
          ServerName zapletalovi.com
          Redirect 301 /.well-known/webfinger https://social.zapletalovi.com/.well-known/webfinger
          Redirect 301 /.well-known/nodeinfo https://social.zapletalovi.com/.well-known/nodeinfo
        </VirtualHost>

This HTTP section allows Mastodon instances to perform redirection.

        <VirtualHost *:443>
          ServerName zapletalovi.com
          Redirect 301 /.well-known/webfinger https://social.zapletalovi.com/.well-known/webfinger
          Redirect 301 /.well-known/nodeinfo https://social.zapletalovi.com/.well-known/nodeinfo

          SSLEngine On
          SSLCertificateFile /var/lib/acme/certs/zapletalovi.com.crt
          SSLCertificateKeyFile /etc/pki/tls/private/zapletalovi.com.key
        </VirtualHost>

And finaly the same but for HTTPS.

So there you have it, I really like gotosocial. If you want to try it, keep in
mind that it is only a backend, there is no user-facing UI except the profile
page and user settings page. Service operations can be done via CLI, API and a
small admin UI which I have't even tried. To access your feed, you can use any
UI or mobile app. There are two recommended, from which I have chosen
[Pinafore](https://pinafore.social), a static JavaScript web application which
is very fast, intuitive and works on mobile too.

Oh, it's alpha version. You have been warned!

Follow me at [@lukas@zapletalovi.com](https://social.zapletalovi.com/@lukas). Cheers.
