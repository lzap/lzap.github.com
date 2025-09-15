---
type: "post"
aliases:
- /2017/10/ryzen-and-linux-is-a-disaster-2017.html
date: "2017-10-06T00:00:00Z"
tags:
- linux
- fedora
- ryzen
title: Ryzen and Linux is a disaster (2017)
---

*If you are reading this blog post in 2018 or later, chances are that AMD has
fixed all Linux issues. But that was not the case months after launch in 2017.
Also, I work at Red Hat, these lines are solely my own opinion blah blah.
Let's start, shall we?*

Ryzen 7 series was introduced early March 2017, I bought parts for my Ryzen
workstation beginning June 2017 thinking that few months will allow AMD to
settle down and release necessary BIOS updates and CPU microcode upgrade. I
was wrong. Terribly wrong.

I was excited when doing the build, mostly because of the new case I bought:
Fractal Design Define R5 and Seasonic M12 EVO Bronze 520W. This is premium
case and I enjoyed every bit of doing the build. Plenty of space for
hard-drives, many cool ideas or things in the case design (screw-less
mounting), huge and silent fans, modularity of the case. With a big enough
SATA Seagate drive, I was planning to do bcache and never run out of space for
home directory.

My primary storage for OS was NVMe SSD drive Intel 600p M.2 256GB but shortly
after installation of Fedora 25 when I performed the initial grub2 package
upgrade, UEFI was not able to boot. Weird error, I spent a week of figuring
out until I found a Red Hat Bugzilla describing corruption with non-Windows
filesystems (specifically XFS).

In short, Intel did not care enough to test this premium (expensive) drive
under Linux on XFS. Since I wanted to start working with my workstation, I
replaced the drive with Samsung NVMe and I doublechecked before my purchase it
works just fine with Linux. The bug has not yet been resolved (October 2017),
some users still report problems with Fedora or CentOS:
https://bugzilla.redhat.com/show_bug.cgi?id=1402533

Anyway, I needed a graphics card and I had one spare MSI GTX 750 Ti which I
used. Noevau driver, PC was freezing, artifacts, terrible experience. After
years and years with Intel CPU and IGP, I almost forgot how terrible this is.
Well, I wanted to buy AMD Radeon RX 5xx anyway, but I couldn't due to Bitcoin
(cards were sold out). I sold the NVidia and bought entry-level used and very
old Radeon card which worked like a charm. Later on I bought RX 540 by ASUS.
Radeon with open-source is like day and night compared to NVidia. It used to
be the other way around.

Now, the Ryzen thing. Get ready.

My PC was freezing, restarting and coredumping when I was working with VMs
running Red Hat Satellite, the product I work on. Tried Ryzen GCC compiler
test, my CPU was affected indeed. My CPU unit was batch from week 22, people
were saying that units produced before week 25 are affected. Since this was a
hardware issue, I contacted AMD support and RMA process started. I did not
care calling to Alza (Czech "Amazon") where I purchased my CPU, because I'd
not expect them to be able to figure out the issue.

I was reseting BIOS, doing pictures of BIOS screens of my ASUS B350 mobo with
certified Kingston DDR4 2400MHz (32 GB), trying various settings. After one
week with AMD support, they sent DHL Express and I was missing my CPU for
another two weeks until they sent a replacement (week 30, UA 1730SUS). And it
worked, memtest passed twice overnight. Problem solved?

Nope, my PC did random restarts or hard freezes when it was idle. What a
disaster - you put Ryzen 7 into decent load, problem. You leave it idling,
another problem! The solution? Googled out to turn off C-State support in
BIOS, which increased power consumption of course. Well, I can live with this
for now, but I want this to be fixed with BIOS/microcode update.

Will my Ryzen PC freeze again? I don't know. But one thing is clear - AMD
clearly did not care testing their hardware under Linux enough. This is rather
surprising, I remember Opteron CPU launch which was pretty good compared to
this.

Anyway, I am big fan of AMD, my very first x86 chip was made by AMD and I am
glad there is some competition for Intel hopefully. Things will settle down, I
just hope AMD will work hard with motherboard manufactures to solve these
issues for Linux early adopters.

And here is a bonus:

Since there was a plenty of space in my case, I took my old SATA SSD (Samsung
840) and installed Windows 10 on this to be able to perform upgrades of BIOS
and SSD firmware. Windows was randomly erroring out during boot about
corrupted "winload.efi". Spent endless nights with this, I thought that
Windows 10 do not like my Fedora on the same ESP partition. Went through
countless tutorials, restoring windows boot files, checking ESP. Since I
partitioned everything as GPT, I could not zap EFI for BIOS anymore. Then I
found it - I had a loose SATA cable to my Windows SSD. The Samsung drive did
not have holes so SATA plug did not "click" in. Common issue with SATA cables,
I swapped it with a different one and taped it just to be sure.

