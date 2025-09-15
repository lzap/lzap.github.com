---
type: "post"
aliases:
- /2020/10/enable-vaapi-on-intel.html
date: "2020-10-16T00:00:00Z"
tags:
- linux
- fedora
title: Enable video acceleration on Intel IGP in Fedora
---

If you have a laptop with Intel integrated card and it gets little bit hot when
watching YouTube or running BlueJeans or Google Meet, you should try this guide
to enable video-acceleration API (VAAPI). This will work with Fedora 32+ with
updates applied (Firefox 81+).

To find out if your hardware meets requirements for this article, do this:

	$ lspci | grep VGA
	00:02.0 VGA compatible controller: Intel Corporation UHD Graphics 620 (rev 07)

This ThinkPad X1 has Intel IGP. Cool. Install required packages:

	sudo dnf install libva libva-intel-driver \
	    libva-vdpau-driver \
	    libva-utils

Verify VAAPI works:

	$ vainfo
	libva info: VA-API version 1.7.0
	libva info: Trying to open /usr/lib64/dri/iHD_drv_video.so
	libva info: va_openDriver() returns -1
	libva info: Trying to open /usr/lib64/dri/i965_drv_video.so
	libva info: Found init function __vaDriverInit_1_7
	libva info: va_openDriver() returns 0
	vainfo: VA-API version: 1.7 (libva 2.7.0.pre1)
	vainfo: Driver version: Intel i965 driver for Intel(R) Kaby Lake - 2.4.1
	vainfo: Supported profile and entrypoints
	      VAProfileMPEG2Simple            :	VAEntrypointVLD
	      VAProfileMPEG2Simple            :	VAEntrypointEncSlice
	      VAProfileMPEG2Main              :	VAEntrypointVLD
	      VAProfileMPEG2Main              :	VAEntrypointEncSlice
	      VAProfileH264ConstrainedBaseline:	VAEntrypointVLD
	      VAProfileH264ConstrainedBaseline:	VAEntrypointEncSlice
	      VAProfileH264ConstrainedBaseline:	VAEntrypointEncSliceLP
	      VAProfileH264Main               :	VAEntrypointVLD
	      VAProfileH264Main               :	VAEntrypointEncSlice
	      VAProfileH264Main               :	VAEntrypointEncSliceLP
	      VAProfileH264High               :	VAEntrypointVLD
	      VAProfileH264High               :	VAEntrypointEncSlice
	      VAProfileH264High               :	VAEntrypointEncSliceLP
	      VAProfileH264MultiviewHigh      :	VAEntrypointVLD
	      VAProfileH264MultiviewHigh      :	VAEntrypointEncSlice
	      VAProfileH264StereoHigh         :	VAEntrypointVLD
	      VAProfileH264StereoHigh         :	VAEntrypointEncSlice
	      VAProfileVC1Simple              :	VAEntrypointVLD
	      VAProfileVC1Main                :	VAEntrypointVLD
	      VAProfileVC1Advanced            :	VAEntrypointVLD
	      VAProfileNone                   :	VAEntrypointVideoProc
	      VAProfileJPEGBaseline           :	VAEntrypointVLD
	      VAProfileJPEGBaseline           :	VAEntrypointEncPicture
	      VAProfileVP8Version0_3          :	VAEntrypointVLD
	      VAProfileVP8Version0_3          :	VAEntrypointEncSlice
	      VAProfileHEVCMain               :	VAEntrypointVLD
	      VAProfileHEVCMain               :	VAEntrypointEncSlice
	      VAProfileHEVCMain10             :	VAEntrypointVLD
	      VAProfileHEVCMain10             :	VAEntrypointEncSlice
	      VAProfileVP9Profile0            :	VAEntrypointVLD
	      VAProfileVP9Profile0            :	VAEntrypointEncSlice
	      VAProfileVP9Profile2            :	VAEntrypointVLD

If the tool prints `vaInitialize failed with error code -1 (unknown libva
error)` try to install package named `libva-intel-hybrid-driver` which works
with older chips. If that does not help, you are out of luck - your hardware is
probably too old.

Start Firefox and visit `about:config` page and set the following flags:

* layers.acceleration.force-enabled = TRUE
* gfx.webrender.all = TRUE
* media.ffmpeg.vaapi-drm-display.enabled = TRUE
* media.ffmpeg.vaapi.enabled = TRUE
* media.ffvpx.enabled = FALSE

In my case, YouTube video playback dropped CPU utilization in `top` utility
from 150-170% to about 40-60%. That's quite huge improvement!

I haven't tried meeting software, but these use similar codecs as YouTube and
it should help as well. Let me know on twitter if this worked for you! I am
@lzap. Cheers.

