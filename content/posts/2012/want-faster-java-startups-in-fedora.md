---
type: "post"
aliases:
- /2012/11/want-faster-java-startups-in-fedora.html
date: "2012-11-19T00:00:00Z"
tags:
- linux
- fedora
- java
title: Want faster Java startups in Fedora?
---

IBM contributed thing which is called class sharing. The thing is simple, you
generate class cache which is then used when Java is starting up (and also
shared across JVMs). Startups are faster.

How to use this (pretty old) feature? You re loking for -Xshare option:

    $ java -X 2>&1 | grep share
    -Xshare:off       do not attempt to use shared class data
    -Xshare:auto      use shared class data if possible (default)
    -Xshare:on        require using shared class data, otherwise fail.

To generate the cache do this:

    # java -Xshare:dump

It creates about 25 MB file:
/usr/lib/jvm/java-1.7.0-openjdk-1.7.0.9.x86_64/jre/lib/amd64/server/classes.jsa

Although help screen shows OpenJDK should automatically use shared class cache
when it is present, this does not work on my Fedora 17. So you need to make
sure your app has -Xshare:on in the JVM options. This is a bug perhaps.

How much fast is it? Well, I did not test Eclipse or something like that as I
dont use it, but it is measurable even for Hello World:

    $ time java -Xshare:on -cp . HelloWorldApp
    Hello World!

    real    0m0.051s
    user    0m0.038s
    sys 0m0.012s

    $ time java -Xshare:off -cp . HelloWorldApp
    Hello World!

    real    0m0.076s
    user    0m0.061s
    sys 0m0.012s

In Windows and MacOS systems, the cache is generated automatically after
installation. I have filed a bug for Fedora to do the same:
https://bugzilla.redhat.com/show_bug.cgi?id=878181


