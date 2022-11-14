---
type: "post"
aliases:
- /2015/10/foreman-and-pxe-less-environments.html
date: "2015-10-07T00:00:00Z"
tags:
- linux
- foreman
title: Foreman and PXE less environments
---

Foreman (and Satellite 6) has many options when it comes to provisioning in
PXE-less (or DHCP-less) environments.

Option 1: *Bootdisk plugin - iPXE*

Foreman Bootdisk plugin enables Foreman users to download *Host based* or
*Generic host* images. These are small ISO images pre-loaded with SYSLINUX which
chainloads [iPXE](http://ipxe.org). This kind of firmware is able to load
kernels via http, but hardware driver in iPXE *must* exist for this to work.
Unfortunately, there are many issues with various hardware and even
virtualization technologies (VMWare, Microsoft).

The *host image* embeds network credentials (IP, gateway, netmask, DNS)
therefore DHCP is not requred but the host is bound to the host it was
generated for. On the other hand, Generic image initializes network via DHCP
and can be used with any host. Recent version of Foreman will add Subnet
image, which is a Generic image but proxies the http calls via Smart Proxy
(Templates plugin must be enabled).

Option 2: *Bootdisk plugin - SYSLINUX*

There is a special kind of image: Full host image. This one is host-based (not
generic) image that requires DHCP. It contains SYSLINUX loader, configuration
rendered from PXELinux template kind associated with the host and embedded
Linux kernel and init RAM disk of the associated OS installer. The image is
slightly bigger, but it works on most platforms as the initial network
configuration is done by the OS installer (e.g. Anaconda from RHEL).

Although this image type requires DHCP, there is a trick to get it working
with static configuration. Create the following PXELinux kind template and
associate it with the OS/Host, then download the image:

    <%
      mac = @host.primary_interface.mac
      bootif = '00-' + mac.gsub(':', '-') if mac
      ip = @host.primary_interface.ip
      mask = @host.primary_interface.subnet.mask
      gw = @host.primary_interface.subnet.gateway
      dns = @host.primary_interface.subnet.dns_primary
    -%>
    DEFAULT linux
    LABEL linux
    KERNEL <%= @kernel %>
    <% if (@host.operatingsystem.name == 'Fedora' and @host.operatingsystem.major.to_i > 16) or
        (@host.operatingsystem.name != 'Fedora' and @host.operatingsystem.major.to_i >= 7) -%>
    APPEND initrd=<%= @initrd %> ks=<%= foreman_url('provision') + "&static=yes" %> inst.ks.sendmac <%= "ip=#{ip}::#{gw}:#{mask}:::none nameserver=#{dns} ksdevice=bootif BOOTIF=#{bootif}" %>
    <% else -%>
    APPEND initrd=<%= @initrd %> ks=<%= foreman_url('provision') + "&static=yes" %> kssendmac <%= "ip=#{ip} netmask=#{mask} gateway=#{gw} dns=#{dns} ksdevice=#{mac} BOOTIF=#{bootif}" %>
    <% end -%>

For Foreman 1.6 or older (or Satellite 6.0-6.1) use this one:

    <%
      mac = @host.mac
      bootif = '00-' + mac.gsub(':', '-') if mac
      ip = @host.ip
      mask = @host.subnet.mask
      gw = @host.subnet.gateway
      dns = @host.subnet.dns_primary
    -%>
    DEFAULT linux
    LABEL linux
    KERNEL <%= @kernel %>
    <% if (@host.operatingsystem.name == 'Fedora' and @host.operatingsystem.major.to_i > 16) or
        (@host.operatingsystem.name != 'Fedora' and @host.operatingsystem.major.to_i >= 7) -%>
    APPEND initrd=<%= @initrd %> ks=<%= foreman_url('provision') + "&static=yes" %> inst.ks.sendmac <%= "ip=#{ip}::#{gw}:#{mask}:::none nameserver=#{dns} ksdevice=bootif BOOTIF=#{bootif}" %>
    <% else -%>
    APPEND initrd=<%= @initrd %> ks=<%= foreman_url('provision') + "&static=yes" %> kssendmac <%= "ip=#{ip} netmask=#{mask} gateway=#{gw} dns=#{dns} ksdevice=#{mac} BOOTIF=#{bootif}" %>
    <% end -%>

The template passes network credentials from Foreman Host via SYSLINUX
configuration file into Anaconda. This is an example for Red Hat or Fedora
systems. Keep in mind that provisioning token is embedded in the image, so
Host record *must* be present (the image is *not* generic).

For more info visit [Foreman
Bootdisk](https://github.com/theforeman/foreman_bootdisk)

Option 3: *Discovery ISO*

In Foreman 1.10, Discovery image (version 3.0.1+) together with Foreman
Discovery plugin 4.1.1+ can be used to discover systems via CD/DVD-ROM or USB
stick. In this workflow, discovered hosts are either manually or automatically
(via Discovery Rules) provisioned and kernel is replaced with installer using
kexec technology.

It works in both DHCP or DHCP-less environments as the ISO image can be
"remastered" with a script providing network credentials via SYSLINUX
configuration similarly as in Full host image.

For more info visit [Foreman Discovery
documentation](http://theforeman.org/plugins/foreman_discovery/4.0/index.html)

Documentation for this feature is currently being finished. The draft is
[available here](https://github.com/theforeman/theforeman.org/pull/421/files).
