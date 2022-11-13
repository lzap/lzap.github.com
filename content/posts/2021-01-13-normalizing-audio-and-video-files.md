---
type: "post"
aliases:
- /2021/01/normalizing-audio-and-video-files.html
date: "2021-01-13T00:00:00Z"
tags:
- linux
- fedora
title: Normalizing audio and video files
---

To normalize audio or video files without reencoding video stream, use
[ffmpeg-normalize](https://github.com/slhck/ffmpeg-normalize/) script. In
Fedora, it is available in the `python3-ffmpeg-normalize` package.

Usage is very simple:

    ffmpeg-normalize a_file.wav a_file.mp4 a_file.mkv

By default, the output stream will be PCM at 192kHz which will usually be a bit
overkill. For example, I often record screencast with speech and before
uploading to YouTube it's a good idea to normalize and encode the audio channel
into 44.1kHz with AAC at 96kbps:

    ffmpeg-normalize -nt ebu -ar 44100 -c:a aac -b:a 96k a_file.mkv
