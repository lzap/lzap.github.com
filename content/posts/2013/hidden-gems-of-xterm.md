---
type: "post"
aliases:
- /2013/07/hidden-gems-of-xterm.html
date: "2013-07-17T00:00:00Z"
tags:
- linux
- fedora
title: Hidden gems of xterm
---

Last week I migrated from urxvt to xterm, because I noticed that beginning last
year (2012), xterm can finally open URLs nicely. This feature was a blocker for
me, since I read all my e-mails in mutt and I hate copying links.

During migration, I noticed several nice features of xterm so I decided to
write a blog post about few of them. Let's start.

Unicode support
---------------

Xterm supports UTF-8 by default, you really do not need to do anything except
starting it with -u8 option or using uxterm wrapper (which essentially does
the same thing).

If you want to start xterm always in unicode, just add this to .Xresources or
.Xdefaults (for sake of simplicity I will always refer only to .Xdefaults):

    XTerm*utf8: 1

There is one thing, you need to set correct codepage for your font which is
iso10646. Google this, if you want more information, but in short - ISO 10646
is "simplified" Unicode.

You can use xfontsel to select appropriate font, just choose the second latest
star and set it to iso10646. But if you don't want to bother with font
searching, install Terminus font (every single distribution has this one) and
use

    XTerm*font: -*-terminus-medium-*-*-*-18-*-*-*-*-*-iso10646-1

Make sure the last part is set to "1", this makes sure it's UNICODE font.

256 colors
----------

By default xterm does support 256 colors. In any modern distribution, it will
likely start in the 256 colors mode, so you really do not need to change
anything. To see what is your status, just execute the following command within
xterm:

    # echo $TERM
    xterm-256color

Note: *Never* set TERM variable manually, always let your terminal set it.
Overriding this variable means there is something wrong with your xterm setup.

Color scheme
------------

Update 2020: All colors can be set in the configuration file. This is very
subjective, it's better to browse or generate your own color scheme. A good
resource is [terminal.sexy](https://terminal.sexy) interactive site - export
selected scheme in Xresources format. An example:

    *background: rgb:00/00/00
    *foreground: rgb:ff/ff/ff
    *color0:     rgb:00/00/00
    *color1:     rgb:d3/62/65
    *color2:     rgb:ae/ce/91
    *color3:     rgb:e7/e1/8c
    *color4:     rgb:7a/7a/b0
    *color5:     rgb:96/3c/59
    *color6:     rgb:41/81/79
    *color7:     rgb:be/be/be
    *color8:     rgb:66/66/66
    *color9:     rgb:ef/81/71
    *color10:    rgb:e5/f7/79
    *color11:    rgb:ff/f7/96
    *color12:    rgb:41/86/be
    *color13:    rgb:ef/9e/be
    *color14:    rgb:71/be/be
    *color15:    rgb:ff/ff/ff

Comfortable menu
----------------

Do you miss menu from Gnome-terminal or Konsole? I don't. Actually when I was
using those, the first thing I usually did was to hide those. Xterm has a menu
as well!

Just hit Control key and left click, right click or click with middle button
and you have plenty of options there. You can toggle scrollbar, redraw window
or send signals to the console. There are many options and lots of them are
quite useful. I will go through a few of them in the next paragraphs.

Configurable pointer and cursor
-------------------------------

You can configure color of your pointer and even cursor (blinking and color):

    XTerm*pointerColor: white
    XTerm*pointerColorBackground: black
    XTerm*cursorColor: yellow
    XTerm*cursorBlink: true

Some of these are available in the VT menu (Control + middle click) so you can
change them on the fly.

Show Alternate Screen
---------------------

So you are running a vim or less program and the previous content is all
covered. How to show it so you are able to copy something from there? Well,
you can use Show Alternate Screen from the VT Menu (Control + middle click)
and you are there. Click again and guess what, you are back.

File logging
------------

You can enable logging in the main menu (Control + left click) which saves all
the session to a file. Note this feature might not be available on all
platforms as it is considered as a high security risk.

Truetype fonts
--------------

Xterm does support truetype fonts, although I do not use them. They look ugly
in my opinion and rendering of these is slower (e.g. when outputting a large
text file). If you want to preview Truetype fonts, just use the item from the
right-click menu.

You have been warned, if you really like to use xft fonts, here is an example:

    xterm*faceName: Inconsolata:size=10:antialias=false

If you want antialias, just delete that particular part. But if you like your
eyes, don't do that.

Copy and paste
--------------

Linux geeks already know the PRIMARY selection and the CLIPBOARD and how to
work with them. New users can be confused. Xterm is a typical X Window
application and users are supposed to select text into PRIMARY selection and
paste it using middle mouse click (or Control+Shift).

You can also configure xterm to copy text to CLIPBOARD with Select to
Clipboard VT menu option, then you can use Control + V in Firefox or Chrome.
If you really like this, you can set this permanently:

    XTerm*selectToClipboard: true

If you are enabling this, re-think this once again. Having PRIMARY *and*
CLIPBOARD is a good thing and once you get used to it, it's like having two
clipboards.

Left and right selection
------------------------

Some users prefer to select portions of text using left button for beginning
and right button for end as an alternative to dragging. I sometimes use this
when I want to be absolutely sure with the selection (selecting e.g. ssh key)
or I want to select something really big (click, scroll, click). Learn this, it
is nice feature.

Triple click
------------

This is an important thing. By default clicking in xterm works in the following
way:

 * one click - nothing (you can drag or use the other button to select)
 * double click - select word (alphanums plus few characters in the default configuration)
 * triple click - whole line

When working with files (/some/filename) or links (https://www.xyz.com)
selecting is difficult. It is easy to change the behavior. The following
setting changes what xterm considers as characters:

    XTerm*charClass: 33:48,36-47:48,58-59:48,61:48,63-64:48,95:48,126:48

Good complementary configuration is to select links with triple click:

    XTerm*on3Clicks: regex [[:alpha:]]+://([[:alnum:]!#+,./=?@_~-]|(%[[:xdigit:]][[:xdigit:]]))+

I usually leave out the protocol part as optional, therefore both filesystem
paths and URL links do work.

    XTerm*on3Clicks: regex ([[:alpha:]]+://)?([[:alnum:]!#+,./=?@_~-]|(%[[:xdigit:]][[:xdigit:]]))+

And additionally you can configure more regular expressions like:

    XTerm*on4Clicks: regex ...
    XTerm*on5Clicks: regex ...

Depends on what do you really do in your terminals. But what you definitely
want to set is the charClass which helps with selecting links or filenames. We
will talk about this down the article.

Open URL
--------

*Best feature ever*. I waited for years for this one. There is a new event
called exec-formatted which allows you to execute arbitrary commands. If you
make a PRIMARY selection before that, you can open URLs in browser easily. Do
this:

    XTerm*translations: #override Shift <Btn1Up>: exec-formatted("xdg-open '%t'", PRIMARY)  select-start() select-end()

And then select a link and Shift + click on the selection *once again*. This is
important - let me repeat this:

 * hover above a link
 * triple click it to select it (see above)
 * Shift + click it to open it

I recommend to setup word boundaries as described above if you want to use
double clicking and dragging to select links. But triple click is the best
solution so far.

Update 2020: In the previous version of the article, the command was causing
the terminal to "freeze" until another mouse click. I was actually working for
many years and I got used to this, but Jean Terrier pointed me to [this
post](https://pbrisbin.com/posts/selecting_urls_via_keyboard_in_xterm/), which
entails a solution. If you are a returning reader, please update your
configuration with the improved config line above. Thank you!

Search history
--------------

While there is no support for history search in XTerm, it is possible to
configure it in a way that when you hit a sequence (in this example Ctrl+/) it
will spawn another xterm instance with history of the calling terminal in a
less program. The new window is entitled "History":

    XTerm*printerCommand: xterm -T History -e sh -c 'less -r <&3' 3<&0
    XTerm*translations: #override Ctrl <Key>slash: print-everything()

Sidenote: If you want to combine multiple translation statements, you need to
do something like:

    XTerm*translations: #override \n\
      Ctrl <Key>slash: print-everything() \n\
      Shift <Btn1Up>: exec-formatted("firefox '%t'", PRIMARY)

Multiple font sizes
-------------------

You know that - you are presenting some stuff to colleagues on a video
conference using your brand-new xterm configuration when somebody asks you to
make the font bigger. If you don't know there is a "hidden" menu using the
Control key (see above), you are lost.

So when that happens, use Control + click and find a font size like Large or
Huge. XTerm does support several font sizes, it is as easy as configuring
something like:

    # default
    XTerm*font: -*-terminus-medium-*-*-*-18-*-*-*-*-*-iso10646-1
    # unreadable
    XTerm*font1: -*-terminus-medium-*-*-*-12-*-*-*-*-*-iso10646-1
    # tiny
    XTerm*font2: -*-terminus-medium-*-*-*-14-*-*-*-*-*-iso10646-1
    # small
    XTerm*font3: -*-terminus-medium-*-*-*-16-*-*-*-*-*-iso10646-1
    # medium
    XTerm*font4: -*-terminus-medium-*-*-*-22-*-*-*-*-*-iso10646-1
    # large
    XTerm*font5: -*-terminus-medium-*-*-*-24-*-*-*-*-*-iso10646-1
    # huge
    XTerm*font6: -*-terminus-medium-*-*-*-32-*-*-*-*-*-iso10646-1

One important note for users with bitmap fonts: Always select sizes which the
fonts are prepared for. If you don't stick with this rule, you will end up
with slow and ugly resampled fonts which is something you don't want to see.
In my case, make sure the sizes match installed fonts (the directory can
differ in you distribution - this is Fedora 19):

    grep medium /usr/share/fonts/terminus/fonts.dir | grep iso10646
    ter-x12n.pcf.gz -xos4-terminus-medium-r-normal--12-120-72-72-c-60-iso10646-1
    ter-x14n.pcf.gz -xos4-terminus-medium-r-normal--14-140-72-72-c-80-iso10646-1
    ter-x16n.pcf.gz -xos4-terminus-medium-r-normal--16-160-72-72-c-80-iso10646-1
    ter-x18n.pcf.gz -xos4-terminus-medium-r-normal--18-180-72-72-c-100-iso10646-1
    ter-x20n.pcf.gz -xos4-terminus-medium-r-normal--20-200-72-72-c-100-iso10646-1
    ter-x22n.pcf.gz -xos4-terminus-medium-r-normal--22-220-72-72-c-110-iso10646-1
    ter-x24n.pcf.gz -xos4-terminus-medium-r-normal--24-240-72-72-c-120-iso10646-1
    ter-x28n.pcf.gz -xos4-terminus-medium-r-normal--28-280-72-72-c-140-iso10646-1
    ter-x32n.pcf.gz -xos4-terminus-medium-r-normal--32-320-72-72-c-160-iso10646-1

As you can see sizes for the Terminus font are 12, 14, 16, 18, 20, 22, 24, 28
and 32. Note there are keyboard shortcuts for font size, more about them later
on.

Buffer history
--------------

The buffer history defaults to one thousand lines, which is a little bit low.
To change that, use something like:

    XTerm*SaveLines: 9000

Scrolling
---------

I don't like scrollbars in terminals, they just eat space. I already know how
many lines are scrolled up, because I am working there! You can hide scrollbar
and just use Shift+PageUp or PageDown to scroll.

    XTerm*ScrollBar: false

If you want your terminal to scroll down anytime you press a key, use this
setting:

    XTerm*ScrollKey: true

Secure keyboard
---------------

If you enable this option in menu (or via command line), xterm will try to do
its best to make sure there is no other application trying to log keys. Nifty
feature not only for security fans.

Bell blinking
-------------

If you want, for some reason, your screen to blink on bell, just find the menu
item and enable that. You can even make it urgent. Settings are:

    XTerm*visualbell: true
    XTerm*bellIsUrgent: true

Fullscreen Toggle
-----------------

Xterm by default uses Alt + Enter for fullscreen toggle which can conflict
with Midnight Commander feature. If you want to disable this, you can simply
disable fullscreen mode:

    XTerm*fullscreen: never

You can still put the window into the fullscreen mode using your window
manager tho.

Rich keyboard shortcuts
-----------------------

I already showed several keys, xterm has some additional keys which you can
even remap.

                     Shift <KeyPress> Prior:scroll-back(1,halfpage) \n\
                      Shift <KeyPress> Next:scroll-forw(1,halfpage) \n\
                    Shift <KeyPress> Select:select-cursor-start() \
                                            select-cursor-end(SELECT, CUT_BUFFER0) \n\
                    Shift <KeyPress> Insert:insert-selection(SELECT, CUT_BUFFER0) \n\
                            Alt <Key>Return:fullscreen() \n\
                   <KeyRelease> Scroll_Lock:scroll-lock() \n\
               Shift~Ctrl <KeyPress> KP_Add:larger-vt-font() \n\
               Shift Ctrl <KeyPress> KP_Add:smaller-vt-font() \n\
               Shift <KeyPress> KP_Subtract:smaller-vt-font() \n\
                           ~Meta <KeyPress>:insert-seven-bit() \n\
                            Meta <KeyPress>:insert-eight-bit() \n\
                           !Ctrl <Btn1Down>:popup-menu(mainMenu) \n\
                           ~Meta <Btn1Down>:select-start() \n\
                         ~Meta <Btn1Motion>:select-extend() \n\
                           !Ctrl <Btn2Down>:popup-menu(vtMenu) \n\
                     ~Ctrl ~Meta <Btn2Down>:ignore() \n\
                            Meta <Btn2Down>:clear-saved-lines() \n\
                       ~Ctrl ~Meta <Btn2Up>:insert-selection(SELECT, CUT_BUFFER0) \n\
                           !Ctrl <Btn3Down>:popup-menu(fontMenu) \n\
                     ~Ctrl ~Meta <Btn3Down>:start-extend() \n\
                         ~Meta <Btn3Motion>:select-extend() \n\
                            Ctrl <Btn4Down>:scroll-back(1,halfpage,m) \n\
                                 <Btn4Down>:scroll-back(5,line,m)     \n\
                            Ctrl <Btn5Down>:scroll-forw(1,halfpage,m) \n\
                                    <BtnUp>:select-end(SELECT, CUT_BUFFER0) \n\
                                  <BtnDown>:ignore()

All events and mapping is documented in the manual page. Read it.

Default settings
----------------

There's much more, I recommend reading through the man page.

    $ rpm -ql xterm
    /usr/bin/koi8rxterm
    /usr/bin/resize
    /usr/bin/uxterm
    /usr/bin/xterm
    /usr/share/X11/app-defaults/KOI8RXTerm
    /usr/share/X11/app-defaults/KOI8RXTerm-color
    /usr/share/X11/app-defaults/UXTerm
    /usr/share/X11/app-defaults/UXTerm-color
    /usr/share/X11/app-defaults/XTerm
    /usr/share/X11/app-defaults/XTerm-color
    /usr/share/applications/xterm.desktop
    /usr/share/doc/xterm-293
    /usr/share/doc/xterm-293/16colors.txt
    /usr/share/doc/xterm-293/README.i18n
    /usr/share/doc/xterm-293/THANKS
    /usr/share/doc/xterm-293/ctlseqs.txt
    /usr/share/doc/xterm-293/xterm.log.html
    /usr/share/icons/hicolor/48x48/apps/xterm-color.png
    /usr/share/icons/hicolor/scalable/apps/xterm-color.svg
    /usr/share/man/man1/koi8rxterm.1.gz
    /usr/share/man/man1/resize.1.gz
    /usr/share/man/man1/uxterm.1.gz
    /usr/share/man/man1/xterm.1.gz
    /usr/share/pixmaps/filled-xterm_32x32.xpm
    /usr/share/pixmaps/filled-xterm_48x48.xpm
    /usr/share/pixmaps/mini.xterm_32x32.xpm
    /usr/share/pixmaps/mini.xterm_48x48.xpm
    /usr/share/pixmaps/xterm-color_32x32.xpm
    /usr/share/pixmaps/xterm-color_48x48.xpm
    /usr/share/pixmaps/xterm_32x32.xpm
    /usr/share/pixmaps/xterm_48x48.xpm

Just go ahead and try xterm *right now*! Cheers.
