---
type: "post"
aliases:
- /2014/05/virt-builder-quick-provision-script.html
date: "2014-05-15T00:00:00Z"
tags:
- linux
- fedora
title: Virt builder quick provision script
---

Until now, I was using [snap-guest](https://github.com/lzap/snap-guest) tool
together with Foreman to spawn my development/test virtual machines. I have
been carefully monitoring
(virt-builder)[http://libguestfs.org/virt-builder.1.html] tool in recent
Fedoras and it looks like the version from Fedora 20 is finally usable for my
scenarios (thanks Rich for fixing some annoying bugs for me).

Therefore I am happy to announce new tool called
[fvb](https://github.com/lzap/bin-public/blob/master/fvb) which stands for
Foreman-virt-builder. This little script is based around two little commands
virt-builder/virt-install and it has grown to something bigger over last
couple of months. The usage is simple:

    fvb --install-deps

The above command should install all required dependencies on Red Hat systems.
Note Fedora 20+ is *required* to get this working since this needs some latest
and greatest features from virt-builder.

    fvb -n my-nightly-foreman -f
    fvb -n rc-foreman -- "FOREMAN_REPO=rc" "MYVAR=value"
    fvb -n stable-foreman -- "FOREMAN_REPO=releases/1.4"
    fvb -n bz981123 -- "KOJI_BUILD=http://mykoji.blah/taskinfo?taskID=97281"
    fvb -n my-own-script --script fb-xyz.bats -- BATS_REPOOWNER=lzap BATS_BRANCH=test

You may notice download of `centos-6.xz` file into `~/.cache/virt-builder`.
This will only happen once, or when new CentOS minor release is uploaded. The
template image is handled by virt-builder project itself.

The script works the following way:

* Generates MAC address from hypervisor hostname and guest hostname (hash) so
  it does not change when you provision again.
* Removes existing guest from libvirt (if `--force` is given).
* Generates random IP address.
* Allocates DHCP and DNS entry with the MAC and IP in libvirt network
  ("default") overwriting existing entries. This is compatible with virsh
  Foreman provider (and also works the similar way).
* Installs your public SSH key on the image.
* Creates a new VM image based on CentOS6 using virt-builder.
* Configures a firstboot script:
  * install git
  * install bats framework
  * install foreman-bats scripts
  * run script provided by `--script` option (by default
  fb-install-foreman.bats)
* Spawns the new image with virt-install (with nested kvm enabled if
  possible).
* Refreshes dnsmasq configuration.
* Waits until DHCP daemon (dnsmasq) returns the IP address.
* Calls fortune command.

Dnsmasq configuration (optional)
--------------------------------

By default dnsmasq is installed on Fedora and Red Hat systems, but the daemon
is turned off and it is only used by libvirt. What I usually do is I have it
configured as a caching DNS daemon on my laptop. It not only speeds up DNS
queries (web browsing is _much_ faster on all connections), but it also allows
me to redirect DNS queries for different domains to different DNS servers. For
example:

    # grep -v ^# /etc/dnsmasq.conf | sort -u
    bind-interfaces
    cache-size=500
    conf-dir=/etc/dnsmasq.d
    listen-address=127.0.0.1
    resolv-file=/etc/resolv.dnsmasq

    # cat /etc/resolv.conf
    nameserver 127.0.0.1
    domain redhat.com

    # cat /etc/resolv.dnsmasq
    nameserver 8.8.8.8
    nameserver 8.8.4.4

    # cat /etc/dnsmasq.d/local.lan
    addn-hosts=/var/lib/libvirt/dnsmasq/default.addnhosts

In the configuration above, you can see that dnsmasq is configured to read
nameservers from a separate file (`/etc/resolv.dnsmasq`) where it has Google
DNS public servers and to respond on localhost and to act like a simple DNS
caching daemon. The system is configured to take advantage of that.

The last bit is configuration for local.lan domain (default `--domain` for fvb
script). Libvirt keeps host names in this file and since this is in dnsmasq
format, we can read it directly.

What does it mean? Well, if you configure everything according to this, once
you spawn a VM called "test", the box named "test.local.lan" will be
immediately available, so you can do this:

    ssh root@test.local.lan

Or even visit this:

    http://test.local.lan

That's kinda cool, isn't it?

Notes to redhatters
-------------------

If you are not a redhatter, skip to the next section. If you want this setup,
make sure you have something like this:

    # cat /etc/dnsmasq.d/redhat.com
    server=/redhat.com/9.8.7.1
    server=/redhat.com/9.8.7.2
    server=/www.redhat.com/8.8.8.8
    server=/vpn-concentrator-1.redhat.com/8.8.8.8
    server=/vpn-concentrator-2.redhat.com/8.8.8.8

This configuration adds separate handling for redhat.com domain which goes to
internal servers (these are dummy values). Also note that I want to use public
DNS for vpn concentrators and web site (so I am able to connect initially and
also the site works when not connected).

This way you can enjoy advantage of fvb script, fast public DNS lookups and
fast internal lookups.

What next?
----------

The fvb script is just a little prototype. It [lives
here](https://github.com/lzap/bin-public/blob/master/fvb) and I might move it
into a separate repository eventually.

The script can be used for anything, you can provide different distribution
(use `virt-builder -l` to list all the base images available to you) and
provide any command with `--script` that should be executed. For example to
deploy Katello Foreman plugin (which we sometimes call "foretello"), do:

    fvb -n knightly --script 'git clone https://github.com/Katello/katello-deploy.git && cd katello-deploy && ./setup.rb centos6'

The script accepts any shell variables and values after the `--` option, so
you are able to pass anything to your own scripts when needed.

Please send me patches and comments. If you like it, I can rename the project
and generalize it a bit so it is useful for others as well.

Nested virtualization
---------------------

I have one extra trick for you. If you do

    echo “options kvm-intel nested=1″ | sudo tee /etc/modprobe.d/kvm-intel.conf

on the *host* machine and restart, you should be able to use KVM inside KVM.
The fvb script spawns machines with required nesting options turned on, so you
can configure Foreman/Katello for provisioning there.

Help
----

    usage: fvb options -- VARIABLE1=value1 ...

    Script for building images with Foreman preinstalled using virt-builder and
    bats suite on local libvirt host. The script also modifies dnsmasq
    configuration and sends SIGHUP to refresh so the hostname is instantly
    available. The root password is "redhat" but you should have your public
    ssh key installed by default.

    OPTIONS:
      --help | -h
            Show this message

      --name | -n
            Image name, default: nightly

      --distro | -d
            Distribution base image for virt-builder, default: centos-6

      --force | -f
            Overwrite target image and VM if they exist

      --no-sudo
            Do not use sudo for building and running VM - you will need to
            set --image-dir accordingly too when running under regular user.

      --image-dir [path]
            Target images path
            Default: /var/lib/libvirt/images

      --domain [domain]
            Domain suffix like "mycompany.com", default: local.lan

      --subnet [subnet]
            Subnet to be used for writing DHCP/DNS configuration
            Default: 192.168.122 (note there is no suffix or period)

      --pub-key [key]
            Install this public ssh key
            Default: /home/you/.ssh/id_rsa.pub

      --script [name]
            BATS script to execute during first boot (can be any shell command)
            Default: fb-install-foreman.bats

      --install-deps
            Install required dependencies

Next time!

