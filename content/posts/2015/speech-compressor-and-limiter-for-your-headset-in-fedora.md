---
type: "post"
aliases:
- /2015/01/speech-compressor-and-limiter-for-your-headset-in-fedora.html
date: "2015-01-07T00:00:00Z"
tags:
- linux
- fedora
title: Speech compressor and limiter for your headset in Fedora
---

Last couple of months I've been using Google Hangouts and Bluejeans
conferencing technologies more than my VoIP phone. I got used to crisp and
clear voice from my Polycom and Platronics headset so I had a question.

Is it possible to achieve the same with my cheap USB Logitech headset which I
use for this purpose? The obvious answer is -- yes.

This is tutorial how to setup PulseAudio in Fedora 20+ with LADSPA plugins to
improve audio experiences for conferences. It works best if you have a
dedicated audio interface (e.g. USB headset) so you don't need to play around
with the configuration every time you start your conference. This setup is
definitely not good for listening music!

What we need? Just couple of LADSPA audio plugins. Install them with:

    yum -y install ladspa-swh-plugins

Our goal today is to improve volume with two well-known audio technique called
signal compression. We will be using two plugins for that: a compressor and a
limiter (which is technically also a compressor). Both are distributed in the
package we have installed:

    $ analyseplugin /usr/lib64/ladspa/dyson_compress_1403.so

    Plugin Name: "Dyson compressor"
    Plugin Label: "dysonCompress"
    Plugin Unique ID: 1403
    Maker: "Steve Harris <steve@plugin.org.uk>"
    Copyright: "GPL"
    Must Run Real-Time: No
    Has activate() Function: Yes
    Has deactivate() Function: No
    Has run_adding() Function: Yes
    Environment: Normal or Hard Real-Time
    Ports:  "Peak limit (dB)" input, control, -30 to 0, default 0
            "Release time (s)" input, control, 0 to 1, default 0.25
            "Fast compression ratio" input, control, 0 to 1, default 0.5
            "Compression ratio" input, control, 0 to 1, default 0.5
            "Input" input, audio
            "Output" output, audio

    $ analyseplugin /usr/lib64/ladspa/fast_lookahead_limiter_1913.so

    Plugin Name: "Fast Lookahead limiter"
    Plugin Label: "fastLookaheadLimiter"
    Plugin Unique ID: 1913
    Maker: "Steve Harris <steve@plugin.org.uk>"
    Copyright: "GPL"
    Must Run Real-Time: No
    Has activate() Function: Yes
    Has deactivate() Function: No
    Has run_adding() Function: Yes
    Environment: Normal or Hard Real-Time
    Ports:  "Input gain (dB)" input, control, -20 to 20, default 0
            "Limit (dB)" input, control, -20 to 0, default 0
            "Release time (s)" input, control, 0.01 to 2, default 0.5075
            "Attenuation (dB)" output, control, 0 to 70
            "Input 1" input, audio
            "Input 2" input, audio
            "Output 1" output, audio
            "Output 2" output, audio
            "latency" output, control

Long story short, a compressor filter is able to gain volume of a signal in a
dynamic way. Quiet portions of the stream will be boosted more than loud
portions. This ratio can be configured as well as peak limit and release time
of the limitation phase.

A limiter is basically high-ratio compressor which is used to hard-limit
signal that is too loud. It is often used as the very last plugin to make sure
you are getting the loudest signal possible, but not too high.

In other words, a person who talks quiet will be boosted on volume while loud
conference attendees will be limited. That's what we want.

In traditional setup, application sends the stream to the PulseAudio which
sends it directly to the audio card:

    Application -> PulseAudio -> Headset

We want to achieve the following setup:

    Application -> PulseAudio -> Compressor -> Limiter -> Headset

With the LADSPA plugins we just installed this is a piece of cake. Before we
start, we need to find out audio interface we want to "enhance". In my case,
this is the Logitech USB headset:

    $ pacmd list-sinks | grep name:
    name: <alsa_output.pci-0000_00_1b.0.analog-stereo>
    name: <alsa_output.usb-Logitech_Logitech_USB_Headset-00-Headset.analog-stereo>

Now, to create those filters, just type in the following commands:

    pacmd load-module module-ladspa-sink sink_name=ladspa_output.fast_lookahead_limiter_1913.fastLookaheadLimiter master=alsa_output.usb-Logitech_Logitech_USB_Headset-00-Headset.analog-stereo plugin=fast_lookahead_limiter_1913 label=fastLookaheadLimiter control=0,-10,0.25

    pacmd load-module module-ladspa-sink sink_name=ladspa_output.dyson_compress_1403.dysonCompress master=ladspa_output.fast_lookahead_limiter_1913.fastLookaheadLimiter plugin=dyson_compress_1403 label=dysonCompress control=0,1,0.5,0.99

Note you need to make sure the master is set to the name of your output device
(in my case the Logitech USB thing). That's really it. Now, startup the
PulseAudio mixer:

    pavucontrol

Start up your conferencing software (or if it's that a plugin in a browser)
and redirect the output on the Playback tab to "Dyson Compressor". You should
immediately hear the difference - everything should be louder. You will likely
hear more background noise - this is expected.

Having the mixed opened, head over to Output Devices to see how signal is
being boosted and limited. You should see the input monitors on the two filter
plugins and the output.

If you want to tune up parameters, just unload the module and try again:

    pacmd list-modules
    pacmd unload-module XYZ

When you are happy with this, put these two lines in the
/etc/pulse/default.pa (skip the "pacmd" command) and you are good to go.
PulseAudio will remember your setting per application, so you can route
particular applications or plugins through this setup.

If you want to play more with this, there are LADSPA plugins for noise
cancellation and equalizer to cut off low and high frequencies to clean out
speech. Share your setup with me in the comments bellow.

