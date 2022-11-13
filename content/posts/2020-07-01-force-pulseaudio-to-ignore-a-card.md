---
type: "post"
aliases:
- /2020/07/force-pulseaudio-to-ignore-a-card.html
date: "2020-07-01T00:00:00Z"
tags:
- linux
- fedora
title: Force PulseAudio to ignore a card
---

My workstation is dualboot with Windows 10 for gaming and audio recording, but
when I want to quickly record an idea I definitely don'ŧ want to leave my work
environment which is Linux. I have few USB cards dedicated for music recording,
but when I connect one of them, PulseAudio takes over.

PulseAudio is great for a desktop experience, but when it comes to music you
want something pretty different. For example, to record a guitar with minimum
latency, ALSA needs to be used directly without any man in the middle.
Therefore I simply wnat to prevent PulseAudio from detecting the card which
allows me to record directly via ALSA in in Bitwig Studio or Waveform (aka
Traction) DAW.

Here is a simple trick to tell PulseAudio to ignore such sound card, find out
vendor and product ID via `lsusb` command. Here it output from my Behringer
UFO202 USB soundcard which is an old but still good USB audio card with phono
amp (I use two of these for my turntable-code vinyl-mixxx DJing):

    # lsusb | grep Audio
    Bus 001 Device 007: ID 08bb:2902 Texas Instruments PCM2902 Audio Codec

Now, the trick which is quite simple. Tell PulseAudio to ignore the card with

    # cat >/etc/udev/rules.d/89-pulseaudio.rules <<EOF
    ATTRS{idVendor}=="08bb", ATTRS{idProduct}=="2902", ENV{PULSE_IGNORE}="1"
    EOF

Restart PulseAudio, you need to do this for each individual user running
graphical interface (not root):

    $ pulseaudio -k

That's all! Now I can enjoy PulseAudio for my three "normal" interfaces
(integrated soundcard, HDMI audio and USB headset for conferencing) while I can
plug in USB interface from time to time to record a guitar riff.

Oh, by the way, do not forget to set a volume and ummute the card via
`alsamixer`.

Similarly to SELinux, do not turn PulseAudio globally. Just turn it off for the
device you don't want to use with it! Both SELinux and PulseAudio are great,
the problem is the internet full of incorrect information and "solutions" which are
often too radical.
