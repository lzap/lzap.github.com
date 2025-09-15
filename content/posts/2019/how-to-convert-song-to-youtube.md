---
type: "post"
aliases:
- /2019/02/how-to-convert-song-to-youtube.html
date: "2019-02-07T00:00:00Z"
tags:
- music
- linux
title: How to convert song to YouTube
---

I wrote few songs, mostly dance music (house, techno) years go. Since now I don't have time for this (I wish) I only listen to my music from time to time. I realized I haven't uploaded any of my songs to YouTube yet. There is one particular I would like to upload. I was searching for a command to convert an audio (OGG Vorbis in my case) to MP4 Yoube-friendly format with a cover art. After few minutes of googling and searching in man page, this is it:

    ffmpeg -loop 1 -i onthemoon-cover.jpg -i onthemoon.ogg -shortest -acodec copy onthemoon-video.mp4

That's it, easy. Here is it: https://www.youtube.com/watch?v=I6qKn1AYN-Q

