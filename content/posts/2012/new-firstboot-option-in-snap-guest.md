---
type: "post"
aliases:
- /2012/07/new-firstboot-option-in-snap-guest.html
date: "2012-07-26T00:00:00Z"
name: test
tags:
- linux
- snapguest
title: New firstboot option in snap guest
---

[Snap-guest][1] is a simple script for creating copy-on-write QEMU/KVM guests. I
have added new option "-1 \[command\]" that will execute a script during first
boot. It uses rc.local file, so it should be compatible with most
distributions. I test on RHEL and Fedoras.

Primary reason is I maintain some auto-install scripts in git, so I usually do
something like:


    ./snap-guest -b fedora-17-base -t test-vm -s 4098 -1 "git clone xyz && \
        cd xyz && bash -x script.sh"

Command is executed using screen utility (must be installed) in the /root
directory and output of STDOUT and STDERR is captured in the
/root/firstboot.log file. Also two aliases are dropped to root account: tt
tails the logfile and ttr resumes screen.

To recapitulate snap-guest usage:

    usage: ./snap-guest options

    Simple script for creating copy-on-write QEMU/KVM guests. For the base image
    install Fedora or RHEL (compatible), install acpid and ntpd or similar, do not
    make any swap partition (use -s option), make sure the hostname is the same
    as the vm name and it has "base" in it. Example: rhel-6-base.

    OPTIONS:
      -h             Show this message
      -l             List avaiable images (with "base" in the name)
      -a             List all images
      -b [image]     Base image name (template) - required
      -t [image]     Target image name (and hostname) - required
      -n [network]   Network settings (default: "network=default")
      -m [MB]        Memory (default: 800 MiB)
      -c [CPUs]      Number of CPUs (default: 1)
      -p [path]      Images path (default: /var/lib/libvirt/images/)
      -d [domain]    Domain suffix like "mycompany.com" (default: none)
      -f             Force creating new guest (no questions)
      -w             Add IP address to /etc/hosts (works only with NAT)
      -s             Swap size (in MB) that is appeded as /dev/sdb to fstab
      -1 [command]   Command to execute during first boot in /root dir
                     (logfile available in /root/firstboot.log)

    EXAMPLE:

      ./snap-guest -l
      ./snap-guest -p /mnt/data/images -l
      ./snap-guest -b fedora-17-base -t test-vm -s 4098
      ./snap-guest -b fedora-17-base -t test-vm2 -n bridge=br0 -d example.com
      ./snap-guest -b rhel-6-base -t test-vm -m 2048 -c 4 -p /mnt/data/images

Enjoy.

[1]: http://github.com/lzap/snap-guest

