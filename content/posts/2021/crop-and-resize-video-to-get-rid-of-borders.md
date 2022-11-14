---
type: "post"
aliases:
- /2021/04/crop-and-resize-video-to-get-rid-of-borders.html
date: "2021-04-19T00:00:00Z"
tags:
- linux
- fedora
title: Crop and resize video to get rid of borders
---

We stream our community demos on youtube via Google Meet and there are borders
on each side which makes the content to be smaller and less readable. Luckily,
it is in the middle of the screen, so the following command will crop the image
to its 1/1.29 of the size, stretch it back to 720p and reencodes it for YouTube
copying the audio stream.

    ffmpeg -i intput.mp4 -vf "crop=iw/1.29:ih/1.29,scale=-1:720" -y output.mp4

If your source video is different, just play around with the 1.29 constant to
get the desired output. Use `-t` option to encode just the first 10 seconds of
the video to speed testing up:

    ffmpeg -i intput.mp4 -vf "crop=iw/1.29:ih/1.29,scale=-1:720" -t 00:00:10.0 -y output.mp4

That is all.
