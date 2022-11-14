---
type: "post"
aliases:
- /2017/04/pulseaudio-headset-switcher.html
date: "2017-04-13T00:00:00Z"
tags:
- linux
- fedora
title: PulseAudio headset switcher
---

From time to time I encounter an embarrasing moment on meeting when new
headset does not work. I purchased new one which only made some noise instead.
I will return this back, but in the meantime I found a Logitech USB headset in
my closet and it works pretty well, so I think I am gonna stick with it.

I created few aliases that will help me to switch PulseAudio default input and
output to headset and back and forth. My aliases also switch all existing
streams, which is great if I open up BlueJeans or WebEx before making the
change.

This switches input and output to headset, volume is about 90 % for output,
100 % for input, unmutes input and says "Speak":

    auheadset

This puts everything back to laptop default soundcard setting full output
volume and zero input volume:

    aunormal

This mutes the card and says "Mute":

    aumute

And this unmutes it and says "Speak":

    auspeak

I have some key bindings in my i3 window manager to do mute/unmute using
keyboard shortcut. I have to say this is finally a setup that works. Here is
the script you need to put into your .bashrc:


    export MY_NORMAL_OUTPUT=alsa_output.pci-0000_00_1b.0.analog-stereo
    export MY_NORMAL_INTPUT=alsa_input.pci-0000_00_1b.0.analog-stereo
    export MY_HEADSET_OUTPUT=alsa_output.usb-Logitech_Logitech_USB_Headset-00.analog-stereo
    export MY_HEADSET_INPUT=alsa_input.usb-Logitech_Logitech_USB_Headset-00.analog-mono
    alias auvolup="pactl set-sink-volume $MY_HEADSET_OUTPUT +10% && pactl play-sample blip"
    alias auvoldown="pactl set-sink-volume $MY_HEADSET_OUTPUT -10% && pactl play-sample blip"
    alias auvolfull="pactl set-sink-volume $MY_HEADSET_OUTPUT 65536 && pactl play-sample blip"
    alias aumute="pactl set-source-mute $MY_HEADSET_INPUT yes && pactl play-sample mute"
    alias auspeak="pactl set-source-mute $MY_HEADSET_INPUT no && pactl play-sample speak"
    function pacmd-set-output-input {
      pacmd set-default-sink $1
      echo "Default output set $1 (volume $3)"
      pacmd set-default-source $2
      echo "Default intput set $2 (volume $4)"
      pacmd set-sink-volume $1 $3
      pacmd set-source-volume $2 $4
      pacmd list-sink-inputs | grep index | while read line; do
        INDEX=$(echo $line | cut -f2 -d' ')
        echo "Moving $INDEX to $1"
        pacmd move-sink-input $INDEX $1
      done
      pactl play-sample blip
      echo "Done, all set to $5"
      [[ "$5" == "HEADSET" ]] && auspeak
    }
    alias aunormal="pacmd-set-output-input $MY_NORMAL_OUTPUT $MY_NORMAL_INTPUT 65536 0 NORMAL"
    alias auheadset="pacmd-set-output-input $MY_HEADSET_OUTPUT $MY_HEADSET_OUTPUT 40000 65536 HEADSET"

You need to edit `MY_*` variables, use `pactl list` to find your device names.

You also want to put this in your startup script of your WM or somewhere else
where it is loaded just once when PulseAudio starts. In the worst case you can
put this into your .bashrc as well, but it will slow down your shell start.

    pactl upload-sample ~/.i3/blip.wav blip
    pactl upload-sample ~/.i3/mute.wav mute
    pactl upload-sample ~/.i3/speak.wav speak

I found USB headset to be much more cleaner than integrated laptop sound card.
