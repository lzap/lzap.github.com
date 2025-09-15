---
type: "post"
aliases:
- /2016/07/brother-mfc-l27000dw-and-fedora-23.html
date: "2016-07-07T00:00:00Z"
tags:
- linux
- fedora
title: Brother MFC L2700DW and Fedora 20-33
---

I bought this new device in order to have network printing *and* scanning and
it works just fine. It was a pain to get it working tho. Here is a tutorial
which was tested in Fedora 20 through 33.

## Printing over network

Add the printer using IPP protocol:

    lpadmin -p Printer -E -v ipp://printer.home.lan -m everywhere

It is possible to find printer's URL via Bonjour:

    lpinfo --include-schemes dnssd -v
    network dnssd://tiskarna.home.lan._ipp._tcp.local./?uuid=e3248000-80ce-11db-8000-30055c97b111

and then add this via CUPS web interface (IPP printer).

## Printing over USB

Download all four RPM packages from the [Brother
site](https://support.brother.com/g/b/downloadlist.aspx?c=cz&lang=cs&prod=mfcl2700dw_us_eu_as&os=127&flang=English)
and install them. Do not install Driver Install Tool because it does not work
in Fedora. Some tutorials also guides you to install package named
`brother-udev-rule-type1-1.0.0-1.noarch.rpm` but you won't need it as it was
merged into `brscan4` package.

Using Gnome, the printer was detected over USB or IPP but it never worked. The
way you can actually add this printer is to connect to cups via
`https://localhost:631/`, login as a regular user (root will no longer work in
modern distributions) and add new printer. Then use the web interface to add a
printer, mine appeared twice but I selected the option named "Brother
MFC-L2700DW series (fully driverless)" which indeed worked just fine. Select
Brother IPP Driverless (TM) PPD profile on the next screen. The "fully
driverless" item sometimes does not appear automatically, keep refreshing page
until you see it.

Because I keep forgetting the process every year, here is [video of me setting
everything up](https://youtu.be/AH01HUJaPf8).

## Scanning over network

Install the scanning RPMs from the Brother drivers page (see above). I am going
to use simple scan utility, it also needs a dependency package which somehow is
not correctly listed in some Fedora versions, so install these two guys:

    dnf -y install libnsl simple-scan sane-backends

Then visit printer's built-in web interface and configure it for static IP. You
can do the same on your DHCP server if you prefer to.

And then - aaarghhh - the hidden trick which caused me the headache:

    $ brsaneconfig4 -a name=PRACOVNA model=MFC-L2700DW ip=192.168.1.111

And done! Switch over to "Brother *PRACOVNA" scanner and you can scan over IP.
I use "simple-scan" which is quick and nice tool that aims for easy scanning
into PDF with multiple pages support. Highly recommended.

### Outdated instructions

Brother updated their RPM packages recently, I used version from 2020. If you
happen to have old versions, note that there were some problems in RPM scripts.
In that case, check that the following file exist:
`/etc/udev/rules.d/50-brother-brscan4-libsane-type1.rules` and if not fix the
installation script `/opt/brother/scanner/brscan4/udev_config.sh`.

Also check that the file `/etc/sane.d/dll.conf` contains `brscan4` line, if not
add it or fix their script `/opt/brother/scanner/brscan4/setupSaneScan4`:

    echo brother4 >> /etc/sane.d/dll.conf

This was not working in my Fedora 28 in package `brscan4-0.4.5-1.x86_64.rpm` at
all. This seems to be fixed with `brscan4-0.4.9-1.x86_64`. Most likely `sane-backends` package was not installed.

### MacOS support

This printer works out of box via Bonjour (AirPrint) for printing. It does feature also WSD (Windows "remote scanning" protocol) but I could not [get it working](https://github.com/alexpevzner/sane-airscan) in Linux. For Mac, there is the official [Image Capture](https://support.brother.com/g/b/faqend.aspx?c=ca&lang=en&prod=dcp9040cn_all&faqid=faq00000717_003) utility which works over network and also works on Apple Silicon.

