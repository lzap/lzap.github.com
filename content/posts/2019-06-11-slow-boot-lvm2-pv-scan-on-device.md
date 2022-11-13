---
type: "post"
aliases:
- /2019/06/slow-boot-lvm2-pv-scan-on-device.html
date: "2019-06-11T00:00:00Z"
tags:
- linux
- fedora
title: 'Slow boot: LVM2 PV scan on device'
---

My workstation was sometimes slow to boot and got stuck at:

    Start job is running for LVM PV Scan on device 0:1 ...
    Start job is running for activation of DM RAID sets ...

It took me lot of time experimenting with settings, before you do that I
suggest to do one simple workaround. The timeout for this systemd unit is
actually set to infinite value, so it can easily get your PC or laptop stuck
for hours as there is no way of interrupting this. It's not very practical, I
think it's much better to limit the timeout so if you hit the issue again the
system either boots with some volumes uninitialized or fails to boot and drops
into rescue prompt where you can take actions or do a soft reboot. To set a
timeout do this:

    # mkdir -p /etc/systemd/system/lvm2-pvscan@.service.d/
    # cat /etc/systemd/system/lvm2-pvscan@.service.d/interval.conf
    [Unit]
    StartLimitInterval=30

Now, to my problem. These LVM scan jobs were taking dozens of minutes and I am
not patient person so it always ended up in hard reboot. Today, I decided to
take a look. So after quick search, it looks like LVM scan can get stuck when
searching block devices which are not part of the LVM configuration. What's
weird in my case is that lvscan is quick after the system is booted:

    # time vgscan
      Reading volume groups from cache.
      Found volume group "vg_home" using metadata type lvm2
      Found volume group "vg_virt" using metadata type lvm2
    real    0m0,051s
    user    0m0,016s
    sys     0m0,010s

It must be something else, I suspect that it's the CDROM device which is not
yet fully initialized. This was happening *randomly*, most of the times it
booted quicky but when it did not it was pain in the ass. Let's have a look, I
have the following block devices as part of my LVM:

    # pvdisplay | grep PV.Name
      PV Name               /dev/sda1
      PV Name               /dev/nvme0n1p5
      PV Name               /dev/sda3

However it looks like LVM scan need to sniff more of them:

    # cat /etc/lvm/cache/.cache

    # This file is automatically maintained by lvm.
    persistent_filter_cache {
            valid_devices=[
                    "/dev/disk/by-path/pci-0000:02:00.1-ata-1-part3",
                    "/dev/disk/by-id/wwn-0x5000c500a2e9c4ca-part1",
                    "/dev/block/259:5",
                    "/dev/disk/by-id/nvme-eui.0025385471b19e14-part5",
                    "/dev/disk/by-id/wwn-0x5000c500a2e9c4ca-part3",
                    "/dev/disk/by-partuuid/fa532780-e770-448d-b004-120f1128b5b8",
                    "/dev/disk/by-path/pci-0000:02:00.1-ata-1-part1",
                    "/dev/disk/by-partuuid/35f3b55b-5259-45e2-aa93-b8eb8b9b0cd0",
                    "/dev/block/8:1",
                    "/dev/nvme0n1p5",
                    "/dev/sda1",
                    "/dev/disk/by-id/nvme-Samsung_SSD_960_EVO_250GB_S3ESNX0J444591D-part5",
                    "/dev/disk/by-id/ata-ST4000DM005-2DP166_ZDH1KYP4-part3",
                    "/dev/disk/by-path/pci-0000:01:00.0-nvme-1-part5",
                    "/dev/disk/by-partuuid/73267321-1c7e-4510-86ab-6cd45bd38518",
                    "/dev/block/8:3",
                    "/dev/sda3",
                    "/dev/disk/by-id/ata-ST4000DM005-2DP166_ZDH1KYP4-part1"
            ]
    }

There is a configuration option called global filter which whitelists (a) or
blacklists (r) devices by regular expressions. It's easy to understand. There
are actually two options: `filter` and `global_filter` and both need to be set
in addition to `use_lvmetad`. The purpose of LVM metadata daemon is to speedup
device scans at cost of slower boot times, it can be safely disabled. As long
as you don't have dozens of LVM physical volumes and you don't modify LVM
configuration every day, it's a good idea to disable it. It's been deprecated
in Red Hat Enterprise Linux 7.6 as well:

    # grep global_filter /etc/lvm/lvm.conf
    filter = [ "a|/dev/sda[13]|", "a|/dev/nvme0n1p5|", "r|.*|" ]
    global_filter = [ "a|/dev/sda[13]|", "a|/dev/nvme0n1p5|", "r|.*|" ]
    use_lvmetad = 0

Let's run VG and PV scan again to confirm it's finding the devices correctly:

    # vgscan
      Reading volume groups from cache.
      Found volume group "vg_home" using metadata type lvm2
      Found volume group "vg_virt" using metadata type lvm2

    # pvscan 
      PV /dev/sda1        VG vg_home         lvm2 [<1024,00 GiB / 0    free]
      PV /dev/nvme0n1p5   VG vg_home         lvm2 [<149,69 GiB / 0    free]
      PV /dev/sda3        VG vg_virt         lvm2 [<1024,00 GiB / <226,00 GiB free]
      Total: 3 [<2,15 TiB] / in use: 3 [<2,15 TiB] / in no VG: 0 [0   ]

Let's now delete the cache, this is safe operation do not worry:

    rm /etc/lvm/cache/.cache

Note some symlinks will be still present if its target is whitelisted. On the
next reboot, it should be fast enough every time. Special care needs to be
done:

* During fedora upgrades (to keep the `lvm.conf` change when doing `rpmconf`)
* When adding new disks/devices to the LVM (it might not see it until the filter is adjusted)

Hopefully this blog helps me to get here when I search "LVM does not see a
block device". Let's see, cheers!
