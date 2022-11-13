---
type: "post"
aliases:
- /2020/03/fedora-31-and-amd-radeon-5600-xt.html
date: "2020-03-04T00:00:00Z"
tags:
- linux
- fedora
title: Fedora 31 and AMD Radeon 5600 XT
---

I have upgraded my RX 560 to much more powerful 5600 XT. Thanks to 7nm
technology, this beast draws 7W on idle and both fans are turned off similarly
to my old 560 (4W idle) while it can deliver robust performance up to 160W
after BIOS update (I have the launch model before AMD knew about NVidia price
cuts).

When I booted my Fedora 31 however, I did not get it into X.Org with i3 wm. The
system freezed during boot with:

    kernel: amdgpu 0000:0c:00.0: [gfxhub] page fault (src_id:0 ring:221 vmid:1 pasid:32769, for process Xorg pid 2022 thread Xorg:cs0 pid 2869)
    kernel: amdgpu 0000:0c:00.0:   in page starting at address 0x0000800000010000 from client 27
    kernel: amdgpu 0000:0c:00.0: GCVM_L2_PROTECTION_FAULT_STATUS:0x001009BA
    kernel: amdgpu 0000:0c:00.0:          MORE_FAULTS: 0x0
    kernel: amdgpu 0000:0c:00.0:          WALKER_ERROR: 0x5
    kernel: amdgpu 0000:0c:00.0:          PERMISSION_FAULTS: 0xb
    kernel: amdgpu 0000:0c:00.0:          MAPPING_ERROR: 0x1
    kernel: amdgpu 0000:0c:00.0:          RW: 0x0

Luckily enough, upgrading kernel to latest one with AMD firmware does help.
Worry do not, I am going to show you how to upgrade only kernel, modules and
firmware from Fedora Rawhide (development version of Fedora essentially) while
keeping the rest of the system at the stable versions. Once OS is updated to
newever version, with kernel and modules matching the installed version they
will start updating again.

To do this, configure Fedora Rawhide repository as a disabled one:

    # cat >/etc/yum.repos.d/fedora-rawhide.repo <<EOF
    [rawhide]
    name=Fedora - Rawhide - Developmental packages for the next Fedora release
    failovermethod=priority
    baseurl=http://download.fedoraproject.org/pub/fedora/linux/development/rawhide/$basearch/os/
    metalink=https://mirrors.fedoraproject.org/metalink?repo=rawhide&arch=$basearch
    enabled=0
    metadata_expire=6h
    gpgcheck=0
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$basearch file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
    skip_if_unavailable=False

    [rawhide-debuginfo]
    name=Fedora - Rawhide - Debug
    failovermethod=priority
    metalink=https://mirrors.fedoraproject.org/metalink?repo=rawhide-debug&arch=$basearch
    enabled=0
    gpgcheck=0
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$basearch file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
    skip_if_unavailable=False

    [rawhide-source]
    name=Fedora - Rawhide - Source
    failovermethod=priority
    metalink=https://mirrors.fedoraproject.org/metalink?repo=rawhide-source&arch=$basearch
    enabled=0
    gpgcheck=0
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$basearch file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
    skip_if_unavailable=False
    EOF

To install packages from Rawhide repository, it must be explicitly enabled:

    dnf --enablerepo=rawhide upgrade kernel linux-firmware

This will be probably enough for you, however I noticed that there were several
changes upstream this week in regard to AMD Radeon firmware, so I did one step
and copied over amdgpu firmware files over the update just for case. Chances
are you don't need to do this, in case your system won't boot try it. It is
harmless, once linux-firmware package is updated, these changed files will be
overwritten:

    git clone --depth 1 git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git    
    /usr/bin/cp -f linux-firmware/amdgpu/*bin /usr/lib/firmware/amdgpu/

After reboot, the system is back. My current kernel is
kernel-5.6.0-0.rc4.git0.1.fc33.x86_64 and if it's stable enough I am going to
stick with it until Fedora 33 upgrade. My firmware files are from March 2nd
2020 (commit 0148cfefcbf98898ca65bb26d9d7d638b30e211d) as the current ones in Rawhide
are sligtly older (linux-firmware-20200122-105.fc32.src.rpm).

As a reminder, to exclude some packages from updates, simply add the following
line to DNF configuration:

    cat >/etc/dnf/dnf.conf <<EOF
    exclude=kernel* linux-firmware
    END

Remember to remove the line when upgrading to Fedora 32 at the end of May 2020!
This release is expected to have kernel 5.6.0 final release, or higher. For
sure it will have firmware files updated as well.

Until next time!
