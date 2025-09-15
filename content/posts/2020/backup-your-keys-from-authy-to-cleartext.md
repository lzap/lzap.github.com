---
type: "post"
aliases:
- /2020/10/backup-your-keys-from-authy-to-cleartext.html
date: "2020-10-19T00:00:00Z"
tags:
- linux
- fedora
title: Backup your keys from Authy to cleartext
---

I've been using [Authy](https://www.authy.com) for my 2FA and I am happy with
it, it's on my iPhone, iPad, Apple Watch and also Fedora desktop. But the
desktop app is quite slow, it's Chrome web app wrapped as a Snap Linux
application in the end. When I want my token, I want it NOW, instantly in my
clipboard. So I started seeking a cli utility. There is no official app from
Authy, so I have decided to export my keys in clear text.

There are some tutorials on how to do this in browser console, however I am not
particularly strong in JavaScript and it did not work out for me. But I've
stumbled upon [authy-export](https://github.com/alexzorin/authy) command line
app which was written in Go. When you run it for the first time, it registers
as another Authy application asking for your phone number and confirmation in
the Authy app. Then it prints all tokens in the QR code URL format in exchange
for your "backup password". It works flawlessly:

    $ authy-export
    Please provide your Authy TOTP backup password: ************
    Here are your authenticator tokens:

    otpauth://totp/Twitter:@lzap?digits=6&secret=ABC334XZL5K21J7
    ...

The token then can be used to show tokens. There are multiple command-line
applications but if you want raw experience, then oathtool is in every major
Linux distribution:

    $ oathtool --totp -b ABC334XZL5K21J7
    123456

If you want something more convinient I suggest
[gauth](https://github.com/pcarrier/gauth) which after configuration looks like
this:

    $ gauth
               prev   curr   next
    AWS        315306 135387 483601
    Airbnb     563728 339206 904549
    Google     453564 477615 356846
    Github     911264 548790 784099
    [=======                      ]

I created a short Ruby script which converts auth-export output to gauth
configuration file:

    #!/usr/bin/env ruby
    require 'uri'
    require 'cgi'
    require 'open3'
    require 'base64'

    STDIN.each_line do |line|
      begin
        uri = URI.parse(line)
        name = uri.path[1..-1].gsub(':', ' ')
        params = CGI.parse(uri.query)
        puts "#{name}:#{params['secret'][0]}"
      rescue RuntimeError
        # pass
      end
    end

To use just redirect output to input:

    $ authy-export | ./authy2gauth > ~/.config/gauth.csv

With all of this, one can easily synchronize Authy tokens into gauth
configuration and use both tools. I highly suggest to also make `gauth.csv`
part of your daily backup.

A sidenote: to display the QR code on the console do something like:

    $ echo -n "ootpauth://totp/Twitter:@lzap?digits=6&secret=ABC334XZL5K21J7" | qrencode -t UTF8

Finally, "ABC334XZL5K21J7" is NOT my secret. Do not bother. Have fun! :-)

