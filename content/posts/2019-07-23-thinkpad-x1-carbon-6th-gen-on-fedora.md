---
type: "post"
aliases:
- /2019/07/thinkpad-x1-carbon-6th-gen-on-fedora.html
date: "2019-07-23T00:00:00Z"
tags:
- linux
- fedora
title: ThinkPad X1 Carbon 6th gen on Fedora
---

This is a quick post to have my installation notes on the record.

# Step one: BIOS upgrade and settings

Before I start, it is worth mentioning that it's possible to seamlessly upgrade
BIOS and firmware of this laptop directly from Software app in Fedora, however
I want to upgrade BIOS to the latest possible version before I even attempt to
install the OS. You can very likely skip this step, setup BIOS as recommended,
install Fedora and then upgrade it using a single mouse click if you want.

But if you want to follow my intentionally more complicated approach, just do
this:

    # wget https://lenovo.com/blah/blah/n23ur11w.iso
    # geteltorito -o bios.img n23ur11w.iso
    # sudo dd bs=4M if=bios.img of=/dev/sdx

Make sure to have your laptop connected to AC, who knows how much power is in
the battery. The upgrade process was quick, next up we have BIOS settings. I
like to review them one by one but these are notable changes from the standard
configuration:

* Config > Power > Sleep State = Linux
* Config > Network > Wake on LAN = Disabled
* Config > Network > Wake on LAN from Dock = Disabled
* Config > Thunderbolt (TM) 3 > Thunderbolt BIOS Assist Mode = Enabled
* Config > Thunderbolt (TM) 3 > Wake by Thunderbolt (TM) 3 = Disabled
* Config > Thunderbolt (TM) 3 > Security Level = No Security
* Config > Intel AMT = Disabled
* Security > Computrace > Current Setting = Disabled
* Security > I/O Port Access > Fingerprint Reader = Disabled
* Security > I/O Port Access > Wireless WAN = Disabled
* Security > I/O Port Access > Memory Card Slot = Disabled

Few notes. Since this is my very first Thunderbolt 3 laptop and I have zero
experience with security of this thing, I turned it off effectively downgrading
this to pre 3.0 version. Once I get familiar with how this thing works, I will
probably enable it back. I turned off AMT and Computrace features of course, I
don't want to be managed or tracked remotely. However I kept TPM module on and
TXT feature off. Also Intel SGX technology was disabled by default so I kept it
that way. Make sure to remove all fingerprint data even tho the fingerprint
will not likely work under Linux.

In the Security > I/O Port Access it is possible to disable Fingerprint Reader
which usually don't work reliably, WAN and SD card reader to save some extra
watts if you don't plan to use it. Some people even disable LAN but I want to
keep the opportunity to use the adapter when needed.

Now, this is important. Although you will see on various resources to disable
Secure Boot, if you are installing Fedora or RHEL don't do that since
bootloaders are digitally signed and the rest goes through shim "man in the
middle". There is no need to disable this, unless you want to compile your own
kernel and/or kernel modules. If you are planning to use TLP's discharge
feature, note that it will only work with `acpi_call` kernel module and only
then you want to turn off Secure Boot. I can live without discharge feature
myself.

Also the Sleep State is absolutely essential to set to "Linux" if you want to
have this working.

# Step two: Download and install Fedora 30

I used Media Writer available on my existing Fedora to download and write
Fedora 30 image onto a USB stick. It was quick and nice experience. I installed
without LVM because I unlikely be extending or repartitioning this drive and of
course with LUKS2 encryption.

Remember to set computer name (hostname) during the installation. I forgot,
then you can do it via `hostnamectl` or via Settings - Sharing - Name. You are
welcome!

I am bit surprised how often and quick the internal fan kicks in, it's not as
quiet as Macbook Pro 2015 however this is much more powerful machine. Edit:
This happens only when on AC, the laptop running on battery is quiet when idle
or browsing. What a relief!

Anyway, the installation took about two minutes - amount of time I needed to
write those three paragraphs. Storage is indeed quite fast on this laptop.

# Step three: Profit

Once Fedora showed up, I started the Software app and scheduled immediate
update. This was actually my first time to see Fedora update reboot method in
this nice graphical design - so cute. After successful update, I launched
Software once again to update Corporate ME for the Intel's sneaky embedded
software that was offered.

I have decided to install
[TLP](https://linrunner.de/en/tlp/docs/tlp-linux-advanced-power-management.html),
an advanced power management for laptops. It is a set of scripts which fine
tune the system for longer battery life, it works together with systemd and
udev to hook into events like system was unplugged from AC or suspended. It's
not a daemon!

    # sudo dnf install tlp
    # sudo systemctl enable tlp tlp-sleep
    # sudo systemctl start tlp tlp-sleep

I am sticking with the default configuration (`/etc/default/tlp`), it is worth
reviewing the pretty long file and perhaps setting up battery charging
thresholds. Many articles will instruct you to install kernel modules in order
to be able to set these thresholds but as of Kernel 5.1 this is no longer
necessary because there is a new upstream kernel module (`natacpi`) which
provides most of the features:

    # sudo tlp-stat -b
    ...
    +++ Battery Features
    natacpi = active (data, thresholds)
    ...

It can read battery data and set thresholds, unfortunately one nice feature
does not work yet and that is full discharge and recalibration (discharge and
charge to full) when connected to AC. It's a very useful command to do once per
week to keep the battery in a good shape. This will hopefully work without any
additional kernel module in future Fedoras, the command is:

    # sudo tlp recalibrate

Gnome battery applet shows me around 9-15 hours of capacity after enabling tlp
and light use which looks good. I need more battery cycles for better
statistical data so I can hardly comment on battery life but so far so good.
Also it's worth nothing that fan is completely silent when running on battery
and browsing web or working in terminals. Good news for me.

The keyboard is great, initially I struggled with the more modern ThinkPad
keyboards but this is very close to what I always liked. Function keys have a
slight space between groups, enter is big enough, Fn key on the right spot and
the overall feeling is great - keys are big (for such a small one) and
responsive.

Mixed feelings are for the touchpad, it works fine however haptic feedback is a
very nice thing and X1 only has normal "click". I enabled "touch click" or
whatever this is called, this I use for casual evening browsing. For work of
course, there's the beloved trackpoint. Works great, a bit stiff but it's new.

Speakers are quite bad, as bad as in my $200 Chromebook. That's probably why
Lenovo are reworking them in the upcoming 7th generation. But other than that,
they only provide smaller battery and slight chip refresh so it was not worth
the wait for me. I use headphones anyway.

That's all folks for today, I will probably revisit this article after few
weeks and put more of my own experience with this laptop. Take care!
