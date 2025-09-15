---
type: "post"
aliases:
- /2022/11/http-uefi-boot-with-tianocore-libvirt.html
date: "2022-11-05T00:00:00Z"
tags:
- linux
- fedora
title: HTTP UEFI Boot with TianoCore libvirt
---

One of the new features in EFI 2.x is "HTTP Boot" also known as "UEFI HTTP
Boot" or "UEFI Boot". Let's explore how you can use it in your environment, I
will show everything on a Fedora server running KVM/QEMU with Open Virtual
Machine Firmware (OVFM) TianoCore implementation.

First, we will need a Linux environment, that is in my case Fedora 35 Server
Edition with libvirt installed. To serve HTTP files, I will use Apache2 httpd
and iPXE as the bootloader, but this should also work with Grub2:

        # dnf -y install @virtualization httpd ipxe-bootimgs-x86
        # systemctl enable --now libvirtd httpd

Next up, we need to setup DHCP to answer to HTTPBoot and iPXE clients with two
different HTTP addresses. To do that, use the `virsh` command which will start
the editor loaded with bunch of XML:

        # virsh net-edit default

Edit the XML and add `xmlns` attribute to the `network` tag and then the whole
`dnsmasq:options` section:

    <network xmlns:dnsmasq='http://libvirt.org/schemas/network/dnsmasq/1.0'>
      <name>default</name>
      <uuid>9f3e4377-3d33-42df-b34c-7880295d24ee</uuid>
      <forward mode='nat'/>
      <bridge name='virbr0' zone='trusted' stp='on' delay='0'/>
      <mac address='52:54:00:7a:00:01'/>
      <ip address='192.168.122.1' netmask='255.255.255.0'>
        <dhcp>
          <range start='192.168.122.2' end='192.168.122.254'/>
        </dhcp>
      </ip>
      <dnsmasq:options>
        <dnsmasq:option value='dhcp-vendorclass=set:efi-http,HTTPClient:Arch:00016'/>
        <dnsmasq:option value='dhcp-option-force=tag:efi-http,60,HTTPClient'/>
        <dnsmasq:option value='dhcp-match=set:ipxe,175'/>
        <dnsmasq:option value='dhcp-boot=tag:efi-http,&quot;http://192.168.122.1/boot/ipxe-x86_64.efi&quot;'/>
        <dnsmasq:option value='dhcp-boot=tag:ipxe,&quot;http://192.168.122.1/boot/menu.ipxe&quot;'/>
      </dnsmasq:options>
    </network>

It might look a bit cryptic, but what it really does is configuring the DHCP
service (dnsmasq) that is launched by libvirt daemon automatically to answer
with two different HTTP URLs depending on "who asks". If it's HTTPClient (UEFI
firmware), then `ipxe-x86_64.efi` file will be returned. If it's iPXE (the
bootloader), then `menu.ipxe` which is a configuration (script). For all other
requests, just network information (IP, router, DNS) will be returned.

I also suggest to set the `zone` of the bridge interface to `trusted` so all
connections are enabled. Or alternatively, you need to set up firewall to allow
DHCP and HTTP services for the zone you have your libvirt bridge in.

Save and exit, now very important: every time you change this configuration you
need to restart the network. Make sure to power off all VMs on that network
(all connections will be lost anyway):

    # virsh net-destroy default; virsh net-start default

Now, let's prepare boot files and configuration by creating a directory:

    # mkdir -p /var/www/html/boot/f36
    # cp /usr/share/ipxe/ipxe-x86_64.efi /var/www/html/boot
    # cd /var/www/html/boot/f36
    # curl https://download.fedoraproject.org/pub/fedora/linux/releases/36/Server/x86_64/os/images/pxeboot/vmlinuz
    # curl https://download.fedoraproject.org/pub/fedora/linux/releases/36/Server/x86_64/os/images/pxeboot/initrd.img
    # cd -

Create a menu which is a iPXE script. This bootloader has very rich scripting
capabilities, for my testing I will simply start up Anaconda:

    # cat menu.ipxe
    #!ipxe
    echo "Booting Fedora 36 Anaconda..."
    kernel http://192.168.122.1/boot/f36/vmlinuz initrd=initrd.img inst.repo=https://download.fedoraproject.org/pub/fedora/linux/releases/36/Server/x86_64/os/ ip=dhcp
    initrd http://192.168.122.1/boot/f36/initrd.img
    boot

If you want to automate installation, feel free to add `inst.ks` option with a
path to a kickstart file. The whole directory should look something like:

    # find /var/www/html/boot/
    /var/www/html/boot/
    /var/www/html/boot/ipxe-x86_64.efi
    /var/www/html/boot/f36
    /var/www/html/boot/f36/vmlinuz
    /var/www/html/boot/f36/initrd.img
    /var/www/html/boot/menu.ipxe

If you have SELinux in enforcing mode like I do, double check contexts of these files.

Let's create a new VM, I use Cockpit Virtual Machines plugin, creating new VM
is super easy. Make sure not to launch the VM immediately, but click on "Create
and Edit" and before starting it up for the first time, change the firmware
from BIOS to UEFI. If you create a VM with BIOS firmware, you cannot easily
change it back, at least not via Cockpit so pay special attention.

Now, very important: When you create a new EFI VM, the firmware will be
configured in SecureBoot by default. In this mode, only HTTPS protocol is
allowed. All HTTP requests will end up with "Access denied" cryptic error. You
have two options, turn off SecureBoot if you want to use HTTP, or enroll server
CA certificate into the firmware and change the libvirt network configuration
to HTTPS. In this case, make sure the server uses the correct hostname which
matches the X509 CN and DNS resolves it correctly.

For my testing, I will simply turn off SecureBoot as it's good enough:

* Power on the EFI VM.
* Focus the console by clicking it quickly.
* Keep pressing Escape key over and over again.
* A firmware screen should come up.
* Navigate to Device Manager - Secure Boot Configuration.
* Uncheck Attempt Secure Boot. Save your changes via Reset option.

To enroll X509 CA, you will need to create a floppy, copy the file and insert
it into the firmware. For more info:
https://github.com/tianocore/tianocore.github.io/wiki/HTTP-Boot

It is also possible to hardcode the HTTP URL of the bootloader directly into
the firmware, this will work both with HTTP with SecureBoot disabled, or with
HTTPS if you enroll the X509 CA certificate. But this is out of scope of this
post.

Also note that the default boot order in the firmware is: UEFI PXE IPv4, UEFI
PXE IPv6 and only then HTTP Boot IPv4 is attempted. If you do not want to wait,
change the boot order so UEFI HTTP Boot is the first. That's all, start your VM
and it should boot up.  This is the full sequence:

* A EFI VM starts up and TianoCore firmware loads up.
* A DHCP request is made with HTTPClient identifier
* Dnsmasq configured via libvirt answers with `http://192.168.122.1/boot/ipxe-x86_64.efi` address.
* Bootloader is downloaded via HTTP and started up.
* A new DHCP request is made, this time with iPXE identifier.
* Dnsmasq configured via libvirt answers with `http://192.168.122.1/boot/menu.ipxe` address.
* The bootloader downloads and interprets the script.
* Linux kernel and initram disk are downloaded and loaded.
* Linux boots up, initializes network, another DHCP request is made.
* Anaconda installer starts up, kickstart is loaded and the installation can start up.

If you need to debug DHCP server, add the following entries to the libvirt XML
file:

        <dnsmasq:option value='log-queries'/>
        <dnsmasq:option value='log-dhcp'/>
        <dnsmasq:option value='log-debug'/>

To debug Apache2, just tail `/var/log/httpd/access_log`. That is all for today!

