---
type: "post"
aliases:
- /2020/03/linux-desktop-notifications-on-your-smart-phone-or-watch.html
date: "2020-03-10T00:00:00Z"
tags:
- linux
- fedora
title: Linux desktop notifications on your smart phone or watch
---

I use i3wm with dunst for desktop notifications, but last couple of weeks I
missed few meetings due to missed notification bubble from my calendar. I think
it's the new Super Ultra Wide LG monitor that is so huge that I actually miss
notifications in the corner. Granted, I could have configured it to appear in
the middle of the screen, I wanted some better solution for cases when I am
having a coffee or doing something in the kitchen when one arrives. Since I
have a smart phone and a smart watch, I thought like rerouting notifications
there would be nice.

Quick search found a nice service and app called
[https://pushover.net](Pushover). For $5 you can download an app for iPhone or
Android which connects to a service providing a simple notifications (title,
text). There's a simple REST API available with good documentation on how to
use it. The service is free up to 7,500 calls per month, the app is free to
evaluate for one week. That's fair!

Creating new account was quick, then you need to create new application token.
I quickly came up with a script:

    # cat ~/bin/notify-phone
    #!/bin/bash
    curl -s \
      --form-string "token=XXXXXXXXXXXXXXXXXXXXX" \
      --form-string "user=XXXXXXXXXXXXXXXXXXXXX" \
      --form-string "title=$2" \
      --form-string "message=$3" \
      https://api.pushover.net/1/messages.json & >/dev/null

All you need to do at this point is to make your notification daemon to call
this script on every notifaction. In my case (dunst), that's super easy:

    # tail ~/.config/dunst/dunstrc

    [script]
    # params: appname, summary, body, icon, urgency
    script = /home/lzap/bin/notify-phone

And then the dunst daemon needs a reload, that's all. In case your notification
daemon is built into your environment (Gnome, KDE), search for notification
daemon python example, that gives you short script that subscribes to DBus
notification API. You can call the script from there, it must run as a daemon
tho.
