---
type: "post"
aliases:
- /2013/11/how-to-trim-your-ssd-in-fedora-19.html
date: "2013-11-14T00:00:00Z"
tags:
- linux
- fedora
title: How to TRIM your encrypted SSD in Fedora 19
---

Few months ago I installed Fedora 19 on my new laptop with Samsung SSD and
yesterday I found out TRIM is not enabled by default. I was installing using
standard options with LVM/LUKS/ext4 partitions.

There were some problems in Fedora 18 with LUKS not propagating TRIM commands,
but this was fixed in Fedora 19. On my system, TRIM commands propagate
successfully. One just needs to make few changes in the configuration. First
of all, we need to check if TRIM propagates for all partitions to the end
device:

    [lzap@lzapx ~]$ lsblk -D
    NAME                                            DISC-ALN DISC-GRAN DISC-MAX DISC-ZERO
    sda                                                    0      512B       2G         1
    ├─sda1                                                 0      512B       2G         1
    └─sda2                                                 0      512B       2G         1
      ├─fedora_lzapx-root                                  0      512B       2G         1
      ├─fedora_lzapx-swap                                  0      512B       2G         1
      └─fedora_lzapx-home                                  0      512B       2G         1
        └─luks-aaaaaaaa-6657-44f4-8297-bbbbbbbb1111        0      512B       2G         0

The last column shows if TRIM commands do propagate. We can see all is set,
*except* the encrypted home (the last line). To get full TRIM support on
LUKS-encrypted devices, we need to allow TRIM commands. Note that *this can
decrease encryption strengh*. This is the Fedora 19 default crypttab file:

    $ cat /etc/crypttab
    luks-aaaaaaaa-6657-44f4-8297-bbbbbbbb1111 UUID=aaaaaaaa-6657-44f4-8297-a571e02e5492 none

I added `discard` (used to be `allow-discards` in older versions of Fedora - updated) option there:

    $ cat /etc/crypttab
    luks-aaaaaaaa-6657-44f4-8297-bbbbbbbb1111 UUID=aaaaaaaa-6657-44f4-8297-a571e02e5492 none discard

After reboot, LUKS can be checked (for discards flag) with:

    [lzap@lzapx ~]$ sudo cryptsetup status luks-aaaaaaaa-6657-44f4-8297-bbbbbbbb1111
    /dev/mapper/luks-aaaaaaaa-6657-44f4-8297-bbbbbbbb1111 is active and is in use.
      type:    LUKS1
      cipher:  aes-xts-plain64
      keysize: 512 bits
      device:  /dev/mapper/fedora_lzapx-home
      offset:  4096 sectors
      size:    370683904 sectors
      mode:    read/write
      flags:   discards

Note the `lsblk` command will still show zero for the LUKS partition (this is
normal). You should have the whole chain with `1` and `cryptsetup status`
should give you `discards`.

Before we get to the actual configuration, there are two optional steps you
can do.

Optional LVM configuration
--------------------------

If you modify your LVM logical volumes often (e.g. shrinking, deleting), you
want to set issue\_discards to 1 in `/etc/lvm/lvm.conf`. Then you need to do
the next optional step described bellow.

Optional init RAM disk regeneration
-----------------------------------

If you have *root* partition encrypted by LUKS (not my case) or if you have
your *root* partition on LVM *and* you want LVM trimming when shrinking or
deleting (see above optional step), initial RAM disk needs to be regenerated
using the following command:

    dracut -f

You will need to reboot to make this change effective of course.

Now, to enable TRIM and take advantage of it, there are two options:

TRIM when deleting files
------------------------

It is possible to configure ext4 to send TRIM commands while deleting data.
You can do this by adding `discard` option to partitions in `/etc/fstab`. Note
that this slows down deleting a bit. It depends on the SSD drive, but this can
slow down quite significantly on some drives.

Do not put `discard` option to swap devices as this is not required (and
perhaps it will not work either). Swap is SSD friendly by default and
propagates TRIM command.

TRIM via systemd service
------------------------

Preferred option for those who do not want to play around with anything and
want to discard later (when computer is at idle). To enable this option, do
this:

    systemctl enable fstrim.timer
    systemctl start fstrim.timer

This timer was not enabled on my system by default, but I am upgrading my
Fedora twice an year and I can't tell if this is the same for new
installations.

TRIM from cron
--------------

This is my preferred option because it can be scheduled daily, weekly or
during night if you do not turn off your laptop/server:

    cat /etc/cron.weekly/01-fstrim
    #!/bin/sh
    fstrim /
    fstrim /home

    chmod +x /etc/cron.weekly/01-fstrim

Try to run the script now, it should not print any error message. If you
changed LUKS configuration, you might need restart before doing that. If you
delete lots of files often, consider scheduling trimming every day or even
every hour. The more you trim, the faster the process should be.

That's all folks. I would like to thank Lukáš Czerner, Kamil Páral and Chris
Smart for helping me with this.

