---
title: "Fedora 40 on Intel NUC 13th gen"
date: 2024-04-27T22:52:03+02:00
type: "post"
tags:
- linux
- fedora
- hardware
---

My main machine for all upstream work was Intel NUC 8th gen running i3-8109U
CPU, 32 GB RAM and NVME, SSD and two USB HDDs. Originally, I only used this
little machine as a file server and backup server but shortly after I added
bunch of other services which ended up with this mess of NVMe/SSD/HDD.

Last week when I was testing bootable container installations of Anaconda in a
libvirt VM and decided to configure a new raw partition storage pool and (ehm)
I made a small typo. As you guessed, I completely destroyed one of my volumes
(file server data). Recovery from backups was painful as I do not have much
experience with `btrfs` snapshots, I just wanted to try this file system out as
I heard about it. But I did it, family photos and videos were saved, ton of
"scratch" data was lost, probably nothing of a value.

I have decided to buy a new machine and separate home services like files or
backups from my work. The only thing I hate about Intel NUCs is noise under
load which can be easily solved by purchasing one of third-party passive cases.
I use Akasa massive heat-sink/case for my 8th gen NUC and it works flawlessly:
zero noise, temperatures essentially halved. So it was an easy decision to go
for Intel NUC again.

I landed on Intel NUC 13 with i5-1340P with 12 cores (4 p-cores, 8 e-cores),
this is actually the last NUC made by Intel as they sold the business to ASUS
which already introduced a bit modernized NUC based on the same CPU but with
faster DDR5 memory, but reviewers said it was much noisier and higher priced.
Even a system with DDR4 (at 3200 MT/s) is a major upgrade from my i3,
specifically in the storage area - PCIe 4 is much faster than PCIe 3. Also 64
GB RAM is twice as big as before.

My NMVe pick was shooting in the dark, I wanted the biggest possible SSD (4 TB)
but reasonably priced to avoid any raw device typos. The plan is to only have
one SSD with LVM so I will never do that again when working with VMs and
logical volumes. So I ultimately decided on fairly new product: Lexar NM790,
quite unknown brand but I have witnessed both Samsung and Intel SSD to die so
why not to try something else. There were some compatibility concerns both for
hardware and Linux kernel, but I could always swap it with my 2TB SSD in PS5 if
it did not work.

And it almost ended up a failure. Luckily, I ordered the tall NUC version which
has a bay for additional 2.5 HDD/SSD. I have not realized how massive is the
heat-sink on the Lexar NVMe, it whould have not fit into a slim NUC model for
sure but the tall model allowed a small hack: I did unscrew the HDD bay in
order to fit the NVMe with the heat-sink. I was not planning to add an internal
HDD anyway, just a USB HDD for backups.

I was planning to purchase Akasa passive heat-sink/case for the new NUC too,
but I have to admit this system is quiet when idle (in balanced fan mode) and
the fan is only audible after minutes of heavy work. I plan to put it into a
separate room where noise is not a concern, so I am going to keep the original
case after all. Eventually I might swap it with the Akasa passive case if the
fan breaks or gets too dirty.

The power consumption is excellent and it is the reason why I use Intel NUC in
the first place. Both 8th gen i3 and this new 13th gen i5 draw around 5W when
idle. I disabled internal SATA, audio, thunderbolt (the system has two of them
version 4), WLAN and bluetooth but I could not identify an improvement in power
draw. Also, power consumption of the Lexar SSD is pretty decent - no measurable
diff when idle, 1-2W under I/O load.

The new system is a fresh Fedora 40 installation, this time a simple and good
old ext4 on LVM. For backups, I plan to use LVM snapshots with `e2image` raw
image dumps into qcow2 with one month history. Here is an example backup script
I ended up using:

```
#!/bin/bash -e
test "$(id -u)" != '0'

DEST=/mnt/backup/img
TS="$(date +%Y%m%d-%H%M)"
SIZE=5G
LOG=$DEST/last.log
date > $LOG

# non-LVM partitions
tar cf $DEST/esp-$TS.tar.zstd --zstd /boot/efi &>>$LOG
e2image -afQ /dev/nvme0n1p2 $DEST/boot-$TS.qcow2 &>>$LOG
zstd --rm -q $DEST/boot-$TS.qcow2 &>>$LOG

# LVM partitions
VG=ssd
for LV in root; do
        SNAP=/dev/${VG}/${LV}_s${TS}
        test -e "$SNAP"
        lvcreate -L${SIZE} -s -n ${LV}_s${TS} /dev/${VG}/${LV} &>>$LOG
        e2image -afQ "$SNAP" $DEST/$LV-$TS.qcow2 &>>$LOG
        zstd --rm -q $DEST/$LV-$TS.qcow2 &>>$LOG
        lvremove -f "$SNAP" &>>$LOG
done

# cleanup and sleep
find $DEST -type f -mtime +30 -delete &>>$LOG
sync
sdparm -C stop -r /dev/sda &>>$LOG

date >> $LOG
```

My linux development will be all virtual from now on, I will use libvirt
through cockpit on a [routed
network](https://lukas.zapletalovi.com/posts/2022/easy-vm-access-with-routed-libvirt-mode/)
and podman for other workloads to keep the host Fedora system clean.

I promise, this time, I will keep it clean for at least a decade...
