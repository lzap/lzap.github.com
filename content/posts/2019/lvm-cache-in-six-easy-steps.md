---
type: "post"
aliases:
- /2019/05/lvm-cache-in-six-easy-steps.html
date: "2019-05-20T00:00:00Z"
tags:
- linux
- fedora
title: LVM cache in six easy steps
---

This article shows how to quickly create LVM cache in six quick step, and how
to remove it properly. Before I start, little bit of warning: I do not
recommend using LVM cache on raw SSD devices. Due to [bug in Fedora
30](https://bugzilla.redhat.com/show_bug.cgi?id=1859149) my cachepool volume
was created with an incorrect cache chunk size which led to problems when I was
trying to remove cache volume from the pool after SSD died. Unfortunately, I
lost all my data since I used more complicated cachepool option.

Here is an advice: use LVM cache only on SSD RAID arrays, SSD chips do die
quickly without warning! Therefore it's a good fit for servers where use of LVM
is very likely. For desktop/laptop use I do recommend to use much more simple
[bcache](https://www.kernel.org/doc/Documentation/bcache.txt) which is availble
in all modern distributions, it is hopefully stable enough and it was designed
from the day one to handle situations when SSD dies.

Before you stop reading, let me tell you that due to an extremely odd [bug in
Fedora 30 GCC9](https://bugzilla.redhat.com/show_bug.cgi?id=1708315) bcache was
corrupting data and I also lost data before I swithed to LVM cache. So nothing
is perfect. A friendly reminder: always backup your data no matter what.

Okay, so you want to use LVM cache. It's pretty simple. Let's assume there is a
(slow) HDD and (fast) NVMe SSD and the first primary partition on the slow
device (`sda1`) should be backed by cache created on the first secondary
partition of the fast device (`nvme0n1p5`). This is actually my workstation
setup, I keep my root filesystem, swap, boot and EFI partition as primary
without any caching or LVM.

    PV_SLOW=/dev/sda1
    PV_FAST=/dev/nvme0n1p5
    VG=vg_home
    LV_SLOW=lv_home
    LV_FAST=lv_home_cache

Here are the six steps. Physical volumes are created, volume group consisting
both volumes, then logical backing volume, then logical cache volume (pool) and
the final logical volume is converted (renamed) and the cache is built:

    pvcreate $PV_SLOW
    pvcreate $PV_FAST
    vgcreate $VG $PV_SLOW $PV_FAST
    lvcreate -l 100%PVS -n $LV_SLOW $VG $PV_SLOW

Now, there are two options. Without cachepool which is more simple and I
recommend this over the other one:

    lvcreate -l 100%PVS -n $LV_FAST $VG $PV_FAST
    lvconvert --type cache --cachevol $LV_FAST $VG/$LV_SLOW

Here is a more complicated cachepool option, only use this if you know what you
are doing:

    lvcreate --type cache-pool -l 100%PVS -n $LV_FAST $VG $PV_FAST
    lvconvert --type cache --cachepool $LV_FAST $VG/$LV_SLOW

Few extra (hidden) logical volumes are created with suffixes `_cdata`, `_cmeta`
and `_corig`. I will not go into details because frankly I don't know much
about it but the important thing to understand is that the volume that shall be
used for mounting and working is named `$LV_SLOW` (`lv_home` in my example). So
to create a filesystem do something like:

    mkfs.ext4 $LV_SLOW

To remove LVM cache and go back to single origin (normal) logical
volume, just do the following:

    lvconvert --uncache $VG/$LV_SLOW

This will actually do the job of flushing the cache (if writeback was
set) and renaming logical volume back. Now you can access your data
using the very same logical volume (`$LV_SLOW`) which is cool.

WARNING: The "uncache" operation will fail if SSD is no longer available (e.g.
after data loss). Do not use `--force` option as this can possibly lead to data
loss.

That's all. Remember, backups, backups, backups...


