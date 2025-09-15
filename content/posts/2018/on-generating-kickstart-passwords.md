---
type: "post"
aliases:
- /2018/02/on-generating-kickstart-passwords.html
date: "2018-02-27T00:00:00Z"
tags:
- linux
- fedora
title: On generating kickstart passwords
---

Although Fedora or RHEL kickstart accept root password in plain text, it's not
bad idea at all to encrypt them using standard Linux PAM mechanism. There used
to be a utility which is no longer available. So I wrote a small script which
does that. It is in Fedora 27+ now and on its way to EPEL7. Here is how to use
it:


    $ man pwkickstart

    NAME

    pwkickstart - generate kickstart passwords

    SYNOPSIS

      # pwkickstart
      Password:

      # md5
      rootpw --iscrypted $1$SI$D964QyK1.Iz/
      # sha256
      rootpw --iscrypted $5$Ll/Q6$SEYqHGso3maNbtBc1wjyiyr2
      # sha512
      rootpw --iscrypted $6$MN7wS$1QE3FmSBrN71tXV8y.Blif1avdhTYt/

    DESCRIPTION

    Utility pwkickstart generates kickstart passwords from password input and
    prints them to standard output in three different formats: md5, sha256 and
    sha512.

    Previously grub-crypt provided the same, but it is not longer available in
    some Linux distributions.

    The output in section was shortened to fit on screen in the SYNOPOSIS example
    above.

    LICENSE

    MIT License

Or you can grab it from [my github repo](https://github.com/lzap/pwkickstart).

Have fun!

