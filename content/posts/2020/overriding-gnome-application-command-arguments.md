---
type: "post"
aliases:
- /2020/09/overriding-gnome-application-command-arguments.html
date: "2020-09-03T00:00:00Z"
tags:
- linux
- fedora
title: Overriding Gnome application command arguments
---

Google Chrome 85, which I use as a secondary browser, introduced a regresion for AMD GPUs and I have to provide it a command line option in order to mitigate the problem. I was trying to find if there is any way to override or redefine just the Exec line of the desktop entry (`app.desktop` file) but [it looks like it can't be done](https://developer.gnome.org/desktop-entry-spec/).

The solution is to copy desktop entry specification from `/usr/share/applications` to home folder. Do not change the file name if you want to override the system-wide specification, do change the file name when you want to have a copy (another icon/app). In my case, I do only want a single Google Chrome entry:

    cp /usr/share/applications/google-chrome.desktop ~/.local/share/applications

I've edited the file putting the required "use-cmd-decoder" GPU workaround. Note the new desktop action called "New Insecure Windows" which starts new session in insecure mode when server certificate errors are ignored. I only use this to access test machines signed with self-signed CA certificates, do not use this for real web!

    $ cat ~/.local/share/applications/google-chrome.desktop
    [Desktop Entry]
    Version=1.0
    Name=Google Chrome
    GenericName=Web Browser
    GenericName[cs]=WWW prohlížeč
    Comment=Access the Internet
    Comment[cs]=Přístup k internetu
    # https://bugs.chromium.org/p/chromium/issues/detail?id=1122224
    Exec=/usr/bin/google-chrome-stable %U --auth-server-whitelist="*redhat.com" --use-cmd-decoder=validating
    StartupNotify=true
    Terminal=false
    Icon=google-chrome
    Type=Application
    Categories=Network;WebBrowser;
    MimeType=application/pdf;application/rdf+xml;application/rss+xml;application/xhtml+xml;application/xhtml_xml;application/xml;image/gif;image/jpeg;image/png;image/webp;text/html;text/xml;x-scheme-handler/ftp;x-scheme-handler/http;x-scheme-handler/https;
    Actions=new-window;new-private-window;new-insecure-window;

    [Desktop Action new-window]
    Name=New Window
    Name[cs]=Nové okno
    Exec=/usr/bin/google-chrome-stable

    [Desktop Action new-private-window]
    Name=New Incognito Window
    Name[cs]=Nové anonymní okno
    Exec=/usr/bin/google-chrome-stable --incognito

    [Desktop Action new-insecure-window]
    Name=New Insecure Window
    Name[cs]=Nové nezabezečené okno
    Exec=/usr/bin/google-chrome-stable --incognito --allow-running-insecure-content --ignore-certificate-errors

No need of restarting, Gnome automatically picks the changes which is cool. That's all I have for today.
