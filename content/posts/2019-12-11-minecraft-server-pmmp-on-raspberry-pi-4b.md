---
type: "post"
aliases:
- /2019/12/minecraft-server-pmmp-on-raspberry-pi-4b.html
date: "2019-12-11T00:00:00Z"
tags:
- linux
- minecraft
title: Minecraft server PMMP on Raspberry Pi 4B
---

I've purchased the new Raspberry Pi 4B (4GB model) with a slick Flirc case
which is also a passive-cooled alu case and it looks good on my table. The idea
is to run Minecraft server for Windows 10, iOS, Android, XBox and PS4 edition
(which launched yesterday).

First things first, wihich server software to install. Microsoft has an alpha
build of Bedrock Server but unfortunately builds are only for x86_64 (Windows
and Linux), this is ARM. Second option was some custom-made Java version and
the third was quite popular one (many forks) written in PHP. That sounds fine,
name's Pocketmine MP (PMMP, https://pmmp.io/). I've picked the latter.

While I waited for my Raspberry, I tried to install it on my Turris home router
which is powered by an ARMv7 (32 bit) CPU. After PHP installation from OpenWRT
repositories, the application refused to start requiring 64bit processor. So I
gave up at this point. When RPi arrived, I was impressed with the case - it
looks really cool. The RPi 4B gets quite hot, with the case which also works as
a small passive cooler it's 45 degrees C while idle and during compilation it
did not work over 60 degrees. Granted I've switched off bluetooth, wifi and GPU
has nothing to do as this is all headless.

At the time of writing (December 2019), Raspbian already had 64bit kernel to
choose from but all userspace is still 32bits. There was an option to install
Minecraft in a chroot, but I've chosen a different option. After 11 years, I've
decided to return to Gentoo which I used as a user and a casual packager. There
is [someone maintaining](https://github.com/sakaki-/gentoo-on-rpi-64bit) Gentoo
build for Raspberry Pi 3 and 4(B) including optimizations, 3rd party portage
mirror with weekly binary builds. Great work right there!

Installation was super smooth, I've followed the README, downloaded "lite"
image (about 700 MB), booted up and it all worked like charm! I secured it, set
SSH keys and disabled WiFi, BT and decreased graphics memory:

    # passwd
    ... (set new strong root password! ...

    # userdel -r demouser

    # cat /boot/config.txt
    ...
    dtoverlay=disable-wifi
    dtoverlay=disable-bt
    gpu_mem=16
    #start_x=1
    ...

Warning: If you don't have experience with administrating Linux servers, make
sure to issue the `userdel` command to delete the default user with publicly
known password. If you want to expose the server via SSH, this would be a
seroius security threat! Also pick a good root password. I also recommend to
disable password authentication and use SSH keys instead (not covered in this
article).

Update was very fast because the maintainer deployed a binary portage tree, so
no compilation for the base system:

    # genup

Kudos! Then I've installed few more programs I usually need. A good editor,
screen utility and Midnight Commander is also handy sometimes. None of these
are needed to run Minecraft servers, use `nano` editor if you like (actually
I'd suggest you to avoid `vim` if you don't know it at this point):

    # emerge vim app-misc/screen app-misc/mc

I tried to install PHP 7.4 from Gentoo tree but Minecraft MP sever did not like
it. So I went the official way of compiling PHP and libraries using their
script, which worked surpringlisly smooth. First, create a regular user because
it's really bad idea to run the software under root account:

    # useradd -m minecraft
    # passwd minecraft

Log in over SSH as minecraft, all commands from now on are under this user
(note `$`). The working and home directory should be:

    $ pwd
    /home/minecraft

I've followed the [official instructions](https://pmmp.readthedocs.io/en/rtfd/installation.html):

    $ curl -sL https://get.pmmp.io | bash -s -

It has downloaded `PocketMine-MP.phar` and `start.sh` script, executed it,
detected it needs to download PHP and then it failed to download binary beacuse
the project doesn't provide aarch64 rpi binaries yet. It also created an empty
`compile.sh` script and executed it apparently not resulting in any
compilation. Now comes the trick, I've checked out their build script from git
and executed it. I've used `screen` because compilation was slow and I left it
over night (with Screen you can detach via Ctrl+a d and attach back via `screen
-rd` command):

    $ git clone https://github.com/pmmp/php-build-scripts
    $ cd php-build-scripts
    $ ./compile.sh

I dettached, signed off and powered off my laptop. The next morning I connected
back, moved the resulting `bin` directory up and exited the screen session:

    $ screen -rd
    $ mv ./bin ..
    $ exit
    $ cd ..

The server is now ready for the initial launch. It asks few questions and start
itself:

    $ ./start.sh
    [*] PocketMine-MP set-up wizard
    [*] Please select a language
    ...

Hope it helps. Looking forward to new adventures with my son and his friends!
Cheers. I am out.

ps - I've realied there are no mobs in the PocketMine-MP as of 2019. There are
some plugins with rather experimental support, but I am giving up. Running the
official Minecraft server on RPi4 is possible, but the server crashes too often
because the CPU can't keep up with the high tick rate. I've purchased an 8th
gen Intel NUC and decided to replace my Synology with it.
