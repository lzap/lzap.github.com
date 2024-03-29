---
type: "post"
aliases:
- /2019/08/capture-and-playback-udp-packets.html
date: "2019-08-13T00:00:00Z"
tags:
- linux
- fedora
title: Capture and playback UDP packets
---

Generating some random statsd communication is easy, it's text-based UDP
protocol and all you need to have is netcat. However things change when statsd
server is integrated with real application flodding it with thousands of
packets of various attributes. For easier debugging, I was able to capture the
traffic with tcpdump:

    tcpdump -i lo udp port 8125 -w /tmp/statsd-from-foreman-devel.pcap

That's easy, however I was looking for a tool to actually replay the traffic
anytime I want and I found tcpreplay. It's easy, to replay at the fastest
possible speed (just once) do:

    tcpreplay -i lo -t -K --loop 1 /tmp/statsd-from-foreman-devel.pcap

Loop 100 times:

    tcpreplay -i lo -t -K --loop 100 /tmp/statsd-from-foreman-devel.pcap

Or keep replaying for one minute at rate of 100 packets per seconds:

    tcpreplay -i lo -K --pps 100 --duration 60 /tmp/statsd-from-foreman-devel.pcap

Here is a [recording](https://lzap.fedorapeople.org/blog/tcpreplay/) of statsd
monitoring from Foreman, about 2600 packets captured during bare-metal hosts
discovery, provisioning and auto-provisioning.

Nice utility indeed. Cheers.
