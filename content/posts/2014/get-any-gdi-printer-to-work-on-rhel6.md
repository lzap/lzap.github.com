---
type: "post"
aliases:
- /2014/04/get-any-gdi-printer-to-work-on-rhel6.html
date: "2014-04-02T00:00:00Z"
tags:
- linux
- fedora
title: Get any GDI printer to work on RHEL6
---

I was happy enough to get an old Konica Minolta 163 copy machine and printer.
These devices can deliver black and white printouts at low prices. But this
one is GDI only printer without overpriced network/cpu extension PCL card.
What to do now?

Well, I have one license of Windows XP running in libvirt in the house. Oh, by
the way Microsoft support is ending this month, *what will I do*? :-)
Seriously, how about connecting the machine to my host machine (RHEL6) and
passing the USB device into Windows so I can share the printer and print (via
Google Cloud Print as well). The plan is set.

And it works just like that. Using virt-manager, you can assign the USB
device, install drivers (I'd recommend to install drivers FIRST after my
experience) and start printing. Remember to download GDI drivers and not PCL
for this one otherwise it will not work. But there is a snag.

If you turn off your printer, the connection is lost. When I turn on the
printer back, Windows cannot see it online and the USB device is gone. The
only solution is to detach and reattach the USB device in virt-manager. Okay.
Let's script this, first find the device and vendor USB ID:

    # lsusb | grep Minolta
    Bus 002 Device 004: ID 132b:204c Konica Minolta

Create a libvirt XML definition:

    # cat /var/lib/libvirt/minolta.xml
    <hostdev mode="subsystem" type="usb" managed="yes">
        <source>
            <vendor id="0x132b"/>
            <product id="0x204c"/>
        </source>
    </hostdev>

And reattach with this:

    # virsh detach-device GUEST_NAME /var/lib/libvirt/minolta.xml
    # virsh attach-device GUEST_NAME /var/lib/libvirt/minolta.xml

Once you have this working and you are tired with typing command after you
turn your printer on, then use udev to do this automatically. Warning: This is
tuned for RHEL6/CentOS6 and it may not work on your Ubuntu/Debian depending of
the version of your distribution:

    # cat /etc/udev/rules.d/90-libvirt-usb.rules
    ACTION=="add", \
        SUBSYSTEM=="usb", \
        ENV{ID_VENDOR_ID}=="132b", \
        ENV{ID_MODEL_ID}=="204c", \
        RUN+="/usr/bin/virsh attach-device GUEST_NAME /var/lib/libvirt/minolta.xml"
    ACTION=="remove", \
        SUBSYSTEM=="usb", \
        ENV{ID_VENDOR_ID}=="132b", \
        ENV{ID_MODEL_ID}=="204c", \
        RUN+="/usr/bin/virsh detach-device GUEST_NAME /var/lib/libvirt/minolta.xml"
    ACTION=="add", \
        SUBSYSTEM=="usb", \
        ENV{ID_VENDOR_ID}=="132b", \
        ENV{ID_MODEL_ID}=="204c", \
        RUN+="/bin/logger Attaching USB device to KVM guest"
    ACTION=="remove", \
        SUBSYSTEM=="usb", \
        ENV{ID_VENDOR_ID}=="132b", \
        ENV{ID_MODEL_ID}=="204c", \
        RUN+="/bin/logger Detaching USB device to KVM guest"

After you create this file, do not forget to reload udev rules with

    udevadm control --reload-rules

The two last add and remove commands in the file above are only for monitoring
purposes. I want some clear messages in my syslog:

    kernel: usb 2-1: USB disconnect, device number 3
    logger: Detaching USB device to KVM guest
    kernel: usb 2-1: new full speed USB device number 4 using uhci_hcd
    kernel: usb 2-1: New USB device found, idVendor=132b, idProduct=204c
    kernel: usb 2-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
    kernel: usb 2-1: Product: KONICA MINOLTA 163
    kernel: usb 2-1: Manufacturer: KONICA MINOLTA
    kernel: usb 2-1: SerialNumber: 02145339
    kernel: usb 2-1: configuration #1 chosen from 1 choice
    logger: Attaching USB device to KVM guest

Of course you can see more detailed udev output using

    udevadm monitor --property --kernel --udev

One additional remark - for this particular printer, I had troubles with USB
2.0, so I disabled it completely leaving USB 1.1. Transfer bandwidth does not
matter much for GDI printing I guess. Maybe it was wrong cable (I tried two
USB cables), anyway it works just fine.

Also, I turned off CUPS on my host system and disabled usblp driver (it was
acquiring the device via udev which was useless - I don't use LP on the host):

    service cups stop
    chkconfig cups off

    # cat /etc/modprobe.d/blacklist.conf
    blacklist ehci_hcd
    blacklist usblp

That's all. You can use this approach to get any winprinter working on Linux
(RHEL6) via libvirt (kvm/qemu). All you really need is a valid Windows license
and Linux box with libvirt.
