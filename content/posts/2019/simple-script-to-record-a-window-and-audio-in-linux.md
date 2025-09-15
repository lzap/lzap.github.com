---
type: "post"
aliases:
- /2019/11/simple-script-to-record-a-window-and-audio-in-linux.html
date: "2019-11-25T00:00:00Z"
tags:
- linux
- fedora
title: Simple script to record a window and audio in Linux
---

Works fine on X Window System for years, you asked, here you go. Will probably
not work on Wayland, I haven't tried. Tell me about it if you use it.

For the record, the script asks you to click on a window and then it starts
recording it in slow frames per second with audio from the default device. Stop
with Ctrl+C and then hit ENTER to merge audio+video into a single WebM stream
suitable for youtube.com.

```
#!/bin/bash

NAME=screencast-$(date +%Y%m%d%H%M)
FPS=10
THREADS=7

echo "Click the window to capture and get ready!"

tmpfile=/tmp/screengrab.tmp.$$
trap 'touch $tmpfile; rm -f $tmpfile' 0

xwininfo > $tmpfile 2>/dev/null
left=$(grep 'Absolute upper-left X:' $tmpfile | awk '{print $4}');
top=$(grep 'Absolute upper-left Y:' $tmpfile | awk '{print $4}');
width=$(grep 'Width:' $tmpfile | awk '{print $2}');
height=$(grep 'Height:' $tmpfile | awk '{print $2}');
geom="-geometry ${width}x${height}+${left}+${top}"
echo "Geometry: ${geom}"
size="${width}x${height}"
pos="${left},${top}"
echo "pos=$pos size=$size"

ffmpeg -y -f pulse -ac 2 -i default -f x11grab -r $FPS -s $size -i ${DISPLAY-0:0}+${pos} -acodec pcm_s16le $NAME-temp.wav -an -vcodec libx264 -preset ultrafast -threads 0 $NAME-temp.mp4

echo Merge audio+video and encode to webm for YouTube? && read

ffmpeg -i $NAME-temp.mp4 -i $NAME-temp.wav -acodec libvorbis -ab 128k -ac 2 -vcodec libvpx -threads $THREADS $NAME.webm
```

For the most up-to-date version visit:

https://github.com/lzap/bin-public/blob/master/recordwindow

