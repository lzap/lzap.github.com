---
type: "post"
aliases:
- /2020/01/configuring-hdd-to-spin-down-in-linux-via-smart.html
date: "2020-01-08T00:00:00Z"
tags:
- linux
- fedora
title: Configuring HDD to spin down in Linux via SMART
---

I had a chat with Standa Graf from Red Hat about the `idle3ctl` WD disks
utility, looks like some WD disks do actually follow the SMART/APM parameter
and the spindown timeout can be changed using the standardized utility. Standa
showed me a nifty trick to do this automatically and he claims it works for all
his internal and external (USB) drives. I am gonna share the trick here:

    cat >/etc/udev/rules.d/69-hdparm.rules <<EOF
    ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="1", RUN+="/usr/sbin/smartctl --set apm,128 --set lookahead,on --set wcache,on --set standby,241  /dev/%k"
    EOF

Unfortunately, my WD model (RED 2TB) does not accept the APM parameter and I
need to stick with the `idle3ctl` utility:

    # /usr/sbin/smartctl --set apm,128 --set lookahead,on --set wcache,on --set standby,242 /dev/sdc
    smartctl 7.0 2019-03-31 r4903 [x86_64-linux-5.3.15-300.fc31.x86_64] (local build)
    Copyright (C) 2002-18, Bruce Allen, Christian Franke, www.smartmontools.org

    === START OF ENABLE/DISABLE COMMANDS SECTION ===
    APM enable failed: scsi error badly formed scsi parameters
    Read look-ahead enabled
    Write cache enabled
    Standby timer set to 242 (01:00:00, a vendor-specific minimum applies)

Thought it's useful. Thanks Standa!
