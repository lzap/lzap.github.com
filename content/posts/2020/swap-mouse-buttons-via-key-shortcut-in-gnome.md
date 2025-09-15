---
type: "post"
aliases:
- /2020/12/swap-mouse-buttons-via-key-shortcut-in-gnome.html
date: "2020-12-02T00:00:00Z"
tags:
- linux
- fedora
- gnome
title: Swap mouse buttons via key shortcut in Gnome
---

Gnome provides an easy way to swap mouse buttons which is a useful feature for
left-handed people. I am right-handed, however I am trying to swap mouse in my
hands to compensate and prevent injury. Swapping buttons via *Mouse and
Touchpad* settings is slow and clunky.

You will find many tutorials on how to swap buttons from the command line but
these are XOrg or xinput remappings. I wanted to do it consistently so Gnome is
not confused and also the *Mouse and Touchpad* dialog or other applications
work properly. It was an easy find, to swap buttons from a terminal:

    gsettings set org.gnome.desktop.peripherals.mouse left-handed true

And indeed to flip it back:

    gsettings set org.gnome.desktop.peripherals.mouse left-handed false

There's also a `get` command to find the current state, I think it's obvious
now how to do a script that toggles the setting:

    $ cat bin/swap-mouse-buttons
    #!/bin/bash
    SCHEMA=org.gnome.desktop.peripherals.mouse
    NOW=$(/usr/bin/gsettings get $SCHEMA left-handed)
    if [[ "$NOW" == "true" ]]; then
      /usr/bin/gsettings set $SCHEMA left-handed false
    else
      /usr/bin/gsettings set $SCHEMA left-handed true
    fi

I have an unused key on my keyboard which is probably a "Home" key, I can't
tell from the icon on that key. To use the key for quick swap, just head over
to *Keyboard Shortcuts* in Gnome settings, scroll down to the bottom, enter
path to the script above and map a key of your choice. If you open up *Mouse
and Touchpad* dialog, you can watch how it swaps live as you press the key.
How cool is that!

Now you can be swapping mouse between both hands just like I do. Have fun
learning your secondary hand! And remember, take regular breaks. You can use
[Workrave](https://workrave.org) counter which I maintain for Fedora, just
install `workrave` package and enable Gnome Extension which is shipped in that
package. Cheers!

