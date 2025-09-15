---
type: "post"
aliases:
- /2021/02/raspbery-pi-as-a-brother-print-server.html
date: "2021-02-01T00:00:00Z"
tags:
- linux
- fedora
title: Raspbery Pi as a Brother print server
---

This is a tutorial on how to use Raspberry Pi as a print server. In my
case it's RPi 4 with Brother 7065DN.

The first step is to download a Raspbian image, I suggest the
"headless" image which does not have a graphical environment. In my
case, I downloaded a 64bit image which is still in alpha because I
wanted to be prepared for the future.

Write the image to a SD card, I am on Fedora Linux so I use dd command:

    dd if=2021-01-11-raspios-buster-armhf-lite.zip of=/dev/null status=progress bs%4096

Now, remove the SD card and put it back to mount it. Two new drives
will appear named "boot" and "rootfs". Create a new file named
wpa_supplicant.conf on the boot volume if you want to use WiFi:

    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=CZ
    network={
     ssid="Internet_41"
     psk="SecretPassword"
    }

Make sure to put the correct ISO country code (CZ in my case)
otherwise the 5Ghz band can be turned off due to regulatory
limitations.

Add another empty file called "ssh" which will make the service to be
automatically enabled during the first boot.

If you want to use DHCP, skip this step. Otherwise edit
/etc/dhcpd.conf in the rootfs volume:

    interface wlan0
    static ip_address=10.0.0.130/24
    static routers=10.0.0.138
    static domain_name_servers=10.0.0.138

Unmount the SD card, insert it into your Raspberry, start it and
connect over SSH. The default username and password is: pi /
raspberry. First step, change the password. I suggest also to create a
new user, lock the pi one and configure ssh keys. If you choose to
create a brand new account, make sure it's in all supplementary groups
as the pi user, namely sudo group is important to have sudo access.
The minimum step is to set new password:

    passwd

Setup some reasonable hostname:

    hostnamectl set-hostname printer

Optional: Remove X Windows if you downloaded full image or used used
64bit alpha image which comes only with X:

    sudo systemctl set-default multi-user.target
    sudo apt-get remove --auto-remove --purge 'libx11-.*'
    sudo apt-get autoremove --purge

Now install the print server. I am lucky because my printer driver is
actually in printer-driver-brlaser package:

    sudo apt-get install cups printer-driver-brlaser foomatic-db-engine printer-driver-all openprinting-ppds hp-ppd

Optional: If you know your printer is not in Debian, install drivers
for your printer. Warning: Raspberry Pi is ARM architecture, most
vendors only provide intel drivers and very few do provide full source
codes for their filter programs. This is the breaking point, your
printer might not be supported on Raspberry.

Make sure the user account in use is in the lpadmin group:

    sudo usermod -a -G lpadmin pi

Modify the printer service to listen on the IP address instead of localhost:

    $ grep Listen /etc/cups/cupsd.conf
    Listen 10.0.0.130:631

Put Allow All statements to all Location blocks:

    <Location />
      Order allow,deny
      Allow All
    </Location>

When Pi is on a wifi network, it can take some time until the network
is brought up and CUPS can without a web interface. This helps to
mitigate this problem:

    $ sudo cat /etc/systemd/system/cups.service.d/override.conf
    [Install]
    WantedBy=default.target multi-user.target printer.target
    [Service]
    ExecStartPre=/bin/sleep 30

Reload the systemd service:

    sudo systemctl daemon-reload

And only NOW start the printing service:

    sudo systemctl enable --now cups

That's all. You should be able to print from Linux, ChromeOS, MacOS,
iOS and Android. The only OS I haven't tested is Windows.

As a bonus I am giving you quick few commands to setup file sharing
which is a handy thing to have in a household:

    sudo apt-get install samba cifs-utils
    sudo chmod 777 /mnt/data

    $ cat /etc/samba/smb.conf
    [global]
    netbios name = Printer
    server string = Printer
    [public]
    comment = My USB drive
    path = /mnt/data
    public = yes
    writable = yes
    create mask = 0777
    directory mask = 0777
    force user = nobody
    force group = nogroup

Now start the Samba services:

    sudo systemctl enable --now smbd nmbd

Note that you do NOT need to run Samba in order to print from most
operating systems, laptops of phones. However if you will not be able
to print from Windows, it's possible that Samba needs to be configured
and printing must be enabled. Follow [some
instructions](https://wiki.debian.org/SystemPrinting#CUPS_and_Samba)
in order to do that.

Have fun!

