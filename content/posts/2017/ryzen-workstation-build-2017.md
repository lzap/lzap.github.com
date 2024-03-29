---
type: "post"
aliases:
- /2017/06/ryzen-workstation-build-2017.html
date: "2017-06-07T00:00:00Z"
tags:
- linux
- fedora
- hardware
title: Ryzen workstation build 2017
---

I've been waiting for so long, AMD RYZEN processors are here for some time and
I was giving few months to vendors and community to settle down and release
updates for their BIOSes, firmware and Linux drivers before I finally made my
decision. My next machine for work is AMD RYZEN 1700, unbelievable value for
the money! Eight cores, sixteen threads and only 65 watts with stock cooler
that is silent and "cool" according to all reviews.

For motherboard, I was sure to get B350 chipset which matches my requirements
and after reading my [friend's
article](https://www.heronovo.cz/amd-ryzen-r7-1700/) there was no doubt about
ASUS PRIME B350-PLUS that gives just enough of everything I need, including
M.2 (4x lanes), 1G LAN and enough USB ports.

Now, I am going to use this as typical Linux programmer workstation with some
decent virtualization workload. Since I am working on Red Hat Satellite 6
which is quite demanding (minimum requirements are 16 GB RAM for server, 8 GB
RAM for Capsule), I need more than 24 GB. I wish I could max out mobo to 64
GB, but memory prices are ridiculous these days! It went up like 200%, so I
just ordered 32GB of Kingston DDR4 2400MHz which seems to work just fine with
this ASUS mobo. I do not want any surprises, therefore I will stay at stock
2400MHz and will not do any overclocking of either memory or CPU as I prefer
stability and I really don't know how to do this exactly to be honest.

I am going to experiment with dm-cache tho, so I picked Seagate Barracuda 4TB
SATA drive along with entry-level NVMe SSD drive Intel 600p M.2 256GB where I
am going to put root of my system and cache for home folder sitting on the
Barracuda drive. I am really interested in how dm-cache is usable and what
performance it will give me for large git checkouts.

This is definitely not a gaming rig, but I need a graphics card for sure and
it looks like my old spare MSI GTX 750 Ti will service well. I know, this card
totally does not match the powerful CPU, but it is very quiet and with its TDP
of 60 watts it does not even require extra power connector. It has a DVI
output, that's all I need. Will it scroll my browser smoothly? I bet it will.

Next on the list we have Seasonic M12 EVO Bronze 520W which is total overkill
for this build, but I have one spare which returned from RMA last year (I had
to replace my wife's PSU already), so I will use it. It's a premium and
modular PSU which will keep my case clean.

Speaking about case, I have an old case with DVD burner, but when I pulled it
out this morning, I realized it's way too old, the drive is an IDE one and it
looks - well dated. I quickly made a purchase of Fractal Design Define R5
which is supposed to be most successful case these days according to all
reviews. And it's silent and extensible with many drives for the future,
that's what I aim for. No more hard drive space issues for huge Red Hat yum
repository testing anymore for me!

Hardware installation was smooth, the stock cooler is heavy, looks nice but
most importantly AM4 socket is back to good-old screws. I never liked these
clips or click things and cooler installation was always clunky. Not with AM4
anymore, four screws with a philips screwer. Although my very first chip was
MOS from my Commodore 64, the first x86 CPU was indeed AMD (i386 running at
40Mhz). It's good to be back home.

The new case is brilliant, I never owned a "gaming" case, but this piece was
given dozens of little details which are amazing. Everything is on the right
place but you can move lots of parts inside the noise-cancellation cage,
plenty of room for everything including HDD trays, extra SSD slots on the
back, cable management, dust filters, good case fans included, manual fan
control, most of the work was screwless, and there is more.

The rest of the build was pretty standard, except NVMe Intel 600p M.2 chip
which corrupted my brand new Fedora installation, turned out to be bug in the
Intel's firmware which surprised me and I swapped it with Samsung 960 EVO M.2
chip of the same size. It was a pain to find out, because it also corrupted
Grub2 loader on EFI volume and the system was booting into black screen. Had
to figure it out from Fedora Live system and fsck.

I have been using laptops for work for more than 10 years now, I almost forgot
how it feels to have much more powerful CPU, much more memory and no
limitations of adding more and more drives to the system. During the next days
I will be installing Windows 10 onto this. Lame, yes I know but I just want
smooth BIOS and (SSD) firmware upgrade experience, it is absolutely necessary
to update BIOS of AMD AM4 mobos these days before moving to real work. Then I
will be installing Fedora and setting things up and finally writing an article
about dm-cache setup and how well it hopefully performs.

Idle power consumption of my build is 50W which is nice for such a powerful
system, CPU fan rotating at 1600 RPMs in stock BIOS settings. Everything is
very silent, under load it is the same noise as my Lenovo ThinkPad T430s but
in more comfortable lower frequencies, under idle or web browsing the new
build wins because fan of the laptop never turns off.

Tomorrow is my first working day with the system, I am indeed hopping into a
video conference with BlueJeans which makes my laptop crazy (load 1.50 with
full-throttle fan). I expect much more smooth experience this time.

Some [poor photos from my ASUS
phone](https://plus.google.com/+Luk%C3%A1%C5%A1Zapletal/posts/VoABttp6cuM)

    $ lspci | grep Intel | wc -l
    0

