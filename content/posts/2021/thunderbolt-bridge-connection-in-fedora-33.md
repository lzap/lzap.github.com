---
type: "post"
aliases:
- /2021/02/thunderbolt-bridge-connection-in-fedora-33.html
date: "2021-02-27T00:00:00Z"
tags:
- linux
- fedora
title: Thunderbolt bridge connection in Fedora 33
---

My home network is extremely slow, because I have CAT5e cables everywhere. I
was wondering if I can use Thunderbolt ports which I have both on the new Mac
M1 and Intel NUC with Fedora. So without my breath, since some Thunderbolt
docks are known to brick the new Macs, I connected the two guys. And it worked
automatically!

Fedora's (33) kernel automatically recognized thunderbolt0 device and
NetworkManager created a new connection named "Wired connection 1". There must
be some autonegotiation in the spec, because the two devices created 169.254/16
network and picked some IP addresses. I was not expecting that, I mean maybe if
this was Linux to Linux but with MacOS involved I thought this is not gonna
work. Let's see how fast is my 100Mbps connection:

    mac$ nc -v -l 2222 > /dev/null

    linux$ dd if=/dev/zero bs=1024K count=512 | nc -v 192.168.1.55 2222
    Ncat: Version 7.80 ( https://nmap.org/ncat )
    Ncat: Connected to 192.168.1.5:2222.
    512+0 záznamů přečteno
    512+0 záznamů zapsáno
    536870912 bajtů (537 MB, 512 MiB) zkopírováno, 45,8012 s, 11,7 MB/s
    Ncat: 536870912 bytes sent, 0 bytes received in 45.86 seconds.

That's expected on a 100Mbps ethernet. On a gigabit network, which I considered
to upgrade to, we should see something like 117 MB/s for my ideal case (just a
switch). But let's see how Thunderbolt works for me:

    linux$ dd if=/dev/zero bs=1024K count=512 | nc -v 169.254.145.73 2222
    Ncat: Version 7.80 ( https://nmap.org/ncat )
    Ncat: Connected to 169.254.145.73:2222.
    512+0 záznamů přečteno
    512+0 záznamů zapsáno
    536870912 bajtů (537 MB, 512 MiB) zkopírováno, 0,788541 s, 681 MB/s
    Ncat: 536870912 bytes sent, 0 bytes received in 0.79 seconds.

Holy Moly! It's not 1.1 Gbps but almost 900 MB/s that's insane. This is a USB-C
cable which is the best thing I currently have (this came with my LG screen). I
am dropping a proper Thunderbolt3 into a basket to see how faster this can be.
I mean in theory, I don't have that fast SSD in my Intel NUC server.

Allright, so that's looks like should be my preferred connection between my
desktop and Linux. Let's rename the connection first:

    nmcli con modify "Drátové připojení 1" connection.id thunderbolt0

Oh gosh, I need to switch back to English from Czech language. Next up, set static IP address.

    nmcli con modify thunderbolt0 ipv4.method static ipv4.address 192.168.13.4/24
    nmcli con down thunderbolt0
    nmcli con up thunderbolt0

And after quick update in a MacOS network dialog and `/etc/hosts` change, the
connection between my new desktop and my working Linux machine is 10Gbps.
