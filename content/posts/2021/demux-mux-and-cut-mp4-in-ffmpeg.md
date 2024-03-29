---
type: "post"
aliases:
- /2021/01/demux-mux-and-cut-mp4-in-ffmpeg.html
date: "2021-01-20T00:00:00Z"
tags:
- linux
- fedora
title: Demux, mux and cut MP4 in ffmpeg
---

With the upcoming COVID-19 open-source conferences season, we record
presentations and screencasts almost on daily basis. Sometimes, it's needed to
trim a MP4 video without reencoding the content. It's easy with `ffmpeg`,
option `--s` specifies start in format of `00:00:00.000` or just `0` as number
of seconds, option `-t` represents length of the desired section:

    ffmpeg -ss 0 -i video-orig.mp4 -t 00:20:51.000 -c copy video-cut.mp4

Sometimes video and audio needs to be separated into individual files (aka
demuxed). This can be handy when some audio artifacts need to be removed (e.g.
noise or buzz) from the audio track (aka stream). This can be done easily:

    ffmpeg -i video-orig.mp4 -an -vcodec copy video-demuxed.m4v
    ffmpeg -i video-orig.mp4 -vn -acodec copy audio-demuxed.m4a

Note that `m4v` and `m4a` are not well known but standard extensions for MP4
audio and video streams. If you click on such file, most modern operating
systems should play the file, assuming it was encoded with a codec a player
understands (e.g. h265 or h264 for video and AAC for audio).

Sometimes, audio needs to be extracted into WAV format rather than M4A for
further processing. The rate can be either 44100 or 48000 depending on the
source, if you don't know just use 48000:

    ffmpeg -i video-orig.mp4 -vn -acodec pcm_s16le -ar 48000 -ac 2 audio-demuxed.wav

After corrections are made, let's say in Audacity software, audio can be
compressed back via AAC codec:

    ffmpeg -i audio-edited.wav -c:a aac -b:a 128k audio-edited.m4a

And finally, audio and video can be joined (muxed) back together. Note that at
any point, video stream hasn't been modified (encoded) so no quality is lost
during this process. In the example above, only audio was reencoded back into
AAC which is fast. Muxing and demuxing is also matter of few seconds:

    ffmpeg -i video-demuxed.m4v -i audio-edited.m4a -c:v copy -c:a copy video-final-version.mp4

All of this will also work for other video containers like MKV. This little
tool named `ffmpeg` is indeed a monster.
