---
type: "post"
aliases:
- /2012/08/new-in-fedora-17-i3-42-tiling-wm.html
date: "2012-08-28T00:00:00Z"
tags:
- linux
- fedora
title: The i3 4.2 tiling win manager
---

I was keeping sight on i3 for some time after I saw Michael's [presentation at
Google][1] the other day. Last weekend, I upgraded my Fedora 17 and when I
noticed i3 version 4.2 in the repositories, I gave it a try. First of all, I
have to admit I've fallen in love. Totally.

It's a tiling window manager which is lightweight yet powerful. What I like
about i3 is ease of adopting it. Michael, the main author of this awesome
software, made the default configuration very sane. And i3 is also very fast
by it's (UNIX) design. Last but not least, i3 saves every pixel on the screen.
You can get the most from your screen(s). And yes - it _does_ support multiple
screens very nicely.

Instead of describing how it looks like when you use i3, I'd rather publish my
(pretty new) configuration describing each line of it. Before I start, I need
to highlight one thing. It's a **tiling** window manager. You manage windows
into tiles, it's the basic idea. While you can turn windows into "normal" (the
correct term is "floating") mode, you loose lots of things and this is not the
mode you want to work in. It is mainly used by i3 for dialogs, tooltips or
other temporary windows.

## Installation

Is pretty straightforward. We need i3 itself and several other highly
recommended apps I will describe later. In short: simple screen locker,
starter menu and simple notification daemon.

    # yum -y install i3 i3lock dmenu dunst

Please note dunst is not in Fedora 17 repositories, but I have created a
[review request][2]. Feel free to take it for review.

Exit your desktop environment or window manager and log on into i3 from the
GDM menu (if you use it). i3 will ask to create initial configuration during
the first start. Say yes and do not worry - reloading/restarting i3 is fluent
and you can do this zillions of times without loosing a single window.

## i3 configuration

Configuration is located in __.i3/config__. Let's do the walkthrough.

    set $mod Mod4

i3 works best with a modifier key set to ALT (Mod1) or WIN (Mod4). I have a
windows key on my keyboard unused anyway, so I use it as my main modifier key
(with few exceptions bellow).

    # font for window titles. ISO 10646 = Unicode
    font -misc-fixed-medium-r-normal--13-120-75-75-C-70-iso10646-1

Basic font for windows titles. I was experimenting with my favourite one -
Terminus - but the default (misc-fixed) works great and is narrower.

    # Use Mouse+$mod to drag floating windows to their wanted position
    floating_modifier $mod

By default windows has 1 pixel border, so it's difficult to resize them with
mouse. With this option, you can _move_ windows with modifier + left click and
_resize_ with modifier + right click. I bet Apple patented this already, but
who cares. 

    # start a terminal
    bindsym $mod+Return exec i3-sensible-terminal

I am starting terminals a lot. Like fifty a day, or even more. Michael's
default configuration has this binding and I keep it. By the way i3 has
several i3-\* scripts (three I guess) which tries to find "the best" terminal
(editor etc). In my case its urxvt and vim, but i3-\* will find out from ENV
variables of course.

    # kill focused window
    bindsym $mod+Shift+Q kill

As you will notice shortly, i3 does not draw any minimize, maximize and close
buttons. Except the latter, they are useless. It turns out every single
application has an exit path (usually using Ctrl+q or something like that), so
you don't need the \[X\] button. Few apps do not support it (like very old
xev), you can use this shortcut that tries to close it nicely first and it
kills it if it does not work.

    # start dmenu (a program launcher)
    bindsym $mod+d exec dmenu_run

Do you think there is a start menu or icons on a desktop in i3? Well, it's a
window manager. Of course not. By default it uses excellent dmenu starter and
this simple wrapper that ships with it. Basically, it makes a cache of all
executable applications and shows them while you type in a top bar. It's fast.
It's awesome.

    # reload/restart/exit
    bindsym $mod+Shift+C reload
    bindsym $mod+Shift+R restart
    bindsym $mod+Shift+E exit

Few default key bindings you will like when playing with configuration.

    # screen locker (first move to "safe" workspace without any chat app)
    bindsym Control+Mod1+l exec i3-msg workspace 1 && i3lock -c 111111 -d

My invention here. Locking a screen is an easy task, but unlocking it without
providing your password to other team folks via IRC channel is a challenge
(for a guy in the [Pulp team][3] ;-) therefore I switch to the first workspace
first where is _not_ my IRC chat. Ever. I have to admit the issue is more when
you don't have your screen lock, but it was fun to create this key.

Please note i3lock built into Fedora 17 does _NOT_ support loading of images.
The software itself is capable of loading images instead of solid color, but
this feature was not built. Just stick with a solid color for now.

By the way, you just saw i3-msg command which is distributed with i3
distribution. Every single command you see here in the bindsym and exec
statements can be sent to i3 using i3-msg. You can create shell scripts with
starting up applications, moving them around, changing workspaces and I can't
possibly imagine what can you do with it. Everything.

    # change focus
    bindsym $mod+j focus left
    bindsym $mod+k focus down
    bindsym $mod+l focus up
    bindsym $mod+semicolon focus right
    #bindsym $mod+uring focus right

Default configuration for moving around. Notice this is not exactly what we
know from Vim (its HJKL there). I thought I will hate it, but I got used to it
in two hours. The commented line is for Czech keyboard layout (there is u with
ring instead of semicolon) - ignore it if you don't use this one.

    # alternatively, you can use the cursor keys:
    bindsym $mod+Left focus left
    bindsym $mod+Down focus down
    bindsym $mod+Up focus up
    bindsym $mod+Right focus right

I sometimes use arrow keys, usually when I don't have my hands in the working
position. It is likely when I eat :-)

    # move focused window
    bindsym $mod+Shift+J move left
    bindsym $mod+Shift+K move down
    bindsym $mod+Shift+L move up
    bindsym $mod+Shift+colon move right

Moving windows around is so simple with tiling managers. Just hold shift and
you drag the window there.

    # alternatively, you can use the cursor keys:
    bindsym $mod+Shift+Left move left
    bindsym $mod+Shift+Down move down
    bindsym $mod+Shift+Up move up
    bindsym $mod+Shift+Right move right

I don't use this with arrow keys, but it's defined by default. Why not.

    # split in horizontal orientation
    bindsym $mod+h split h

    # split in vertical orientation
    bindsym $mod+v split v

This is important. By default i3 splits the screen according to the screen
size. For wide screens it's usually horizontal split. You can configure this
behavior if you want, but sometimes you want to split different way. That is
what these bindings are for. i3 remembers that for the workspace, so you can
split multiple windows easily.

    # enter fullscreen mode for the focused container
    bindsym $mod+f fullscreen

Fullscreen is something you don't use many times with standard window
managers, but in tiling mode it is pretty useful. I use it a lot when I wan't
to "zoom in" a window.

    # change container layout (stacked, tabbed, default)
    bindsym $mod+s layout stacking
    bindsym $mod+w layout tabbed
    bindsym $mod+e layout default

Unique feature of i3, I would say. Best thing what you can do is to [see a
picture][4]. You can switch from tiling (default) to tabbed and stacking mode.
You can have multiple Firefox instances in windows tabs if you want to. By the
way, the i3 User's Guide is the definitive document you want to read twice.

    # toggle tiling / floating
    bindsym $mod+Shift+space floating toggle

Some applications does not work well in the tiling mode, because all windows
are maximalized by default and according to your screen size and number of
other containers there first application can be quite stretched. If your
application looks weird, you can always switch to the floating ("normal")
mode, and back and forth with this key mapping. By default, i3 recognizes
dialogs and tool windows, so you do not to switch all windows. Actually I had
to switch only one application by now.

    # change focus between tiling / floating windows
    bindsym $mod+space focus mode_toggle

If you have multiple windows in tiling and floating mode, you want to switch
between those two groups. You do it with this key.

    # focus the parent container
    #bindsym $mod+a focus parent

    # focus the child container
    #bindcode $mod+d focus child

I have to admit I never used this, because I try to keep number of windows on
each workspace low (up to 6 I would say). It moves focus to parent or child
window, perhaps more usable with more windows. Share your experiences with
this. Notice it's disabled because I use mod+d for the dmenu.

    # next/previous workspace
    bindsym Mod1+Tab focus right
    bindsym Mod1+Shift+Tab focus left
    bindsym $mod+Tab workspace back_and_forth

This is not standard binding, but I find Alt+Tab pretty useful combination.
It's handy (I use my right hand for mouse) and it was not used by i3. So I
started using it for cycling through windows on one workspace. If you have
various (horizontal and vertical splits), it does not cycle through all of
them. It's only moving in vertical movement (right - left). I wish there has
been a option like "focus cycle" in the next i3 version.

Shift does the other way around while Win+Tab switches to the last used
weapon. Sorry, I said weapon? I mean workspace.

    # switch to workspace
    bindsym $mod+ampersand workspace 1
    bindsym $mod+eacute workspace 2
    bindsym $mod+quotedbl workspace 3
    bindsym $mod+apostrophe workspace 4
    bindsym $mod+parenleft workspace 5
    bindsym $mod+minus workspace 6
    bindsym $mod+egrave workspace 7
    bindsym $mod+underscore workspace 8
    bindsym $mod+ccedilla workspace 9
    bindsym $mod+agrave workspace 10
    #bindsym $mod+1 workspace 1
    #bindsym $mod+2 workspace 2
    #bindsym $mod+3 workspace 3
    #bindsym $mod+4 workspace 4
    #bindsym $mod+5 workspace 5
    #bindsym $mod+6 workspace 6
    #bindsym $mod+7 workspace 7
    #bindsym $mod+8 workspace 8
    #bindsym $mod+9 workspace 9
    #bindsym $mod+0 workspace 10

    # switch to workspace (f1-f4)
    bindsym F1 workspace 1
    bindsym F2 workspace 2
    bindsym F3 workspace 3
    bindsym F4 workspace 4
    bindsym Mod1+F1 workspace 5
    bindsym Mod1+F2 workspace 6
    bindsym Mod1+F3 workspace 7
    bindsym Mod1+F4 workspace 8

Okay, the first block is default binding. But for many years I decided to
leverage F1-F4 keys for workspace movement. Until now, I was using only four
workspaces (OpenBox, KDE/GNOME, Fluxbox and XFce), but with i3 and its good
support of multiple screens I can afford eight now. Each screen has four
independent workspaces.

Please note the commented part is for Czech layout, therefore if you use this
layout uncomment it and delete the above.

Now let me explain _function keys_ a bit. First of all I realized many years
ago that no one (including me) ever use F1 key. It's reserved, it's for help.
But everybody is googling these days instead searching through built-in docs.
The same for F2, F3 and F4. Maybe some IDEs offer some important stuff, but I
use Vim that has no function keys binding. That is the reason why I gave up
with those keys and use them for workspace switching.

With i3 I have decided also to map Alt+F1-F4 for accessing numbers five to
eight. It just seem natural for me now. I am giving up with Alt-F2 (Run App in
GNOME) or Alt-F4 (Close App), but this does no work in i3 anymore. Few apps
still react on Alt-F4, but there is a different combination available for
that.

If you occasionally need those keys, you can create a re-mapping that would
trigger them with Win+F1-F4 keys. But in terminals you can always use ESC
combination (ESC;1 for F1). I don't use any X11 application that needs that.

Therefore workspaces 1-4 are on the laptop screen (LDVS1) and 5-8 are on the
main monitor (HDMI1). And there is one workspace hidden called scratch one.
More about it later.

    # move focused container to workspace
    bindsym $mod+Shift+1 move container to workspace 1
    bindsym $mod+Shift+2 move container to workspace 2
    bindsym $mod+Shift+3 move container to workspace 3
    bindsym $mod+Shift+4 move container to workspace 4
    bindsym $mod+Shift+5 move container to workspace 5
    bindsym $mod+Shift+6 move container to workspace 6
    bindsym $mod+Shift+7 move container to workspace 7
    bindsym $mod+Shift+8 move container to workspace 8
    bindsym $mod+Shift+9 move container to workspace 9
    bindsym $mod+Shift+0 move container to workspace 10

Default setting for transferring windows (containers) among workspaces. Those
works for both Czech and English layout and are installed by default.

    # border changing
    bindsym $mod+b border toggle

I cycle through normal, 1pixel and none values with this keybinding. By
default it's bound to mod+t, mod+y and mod+u.

    # scratchpad
    bindsym $mod+m move scratchpad
    bindsym $mod+o scratchpad show

Now THIS is cool. There is one hidden workspace that is nowhere and
everywhere. It's empty by default, thus invisible. You can move there any
window you want with mod+m. Container is switched over to floating mode and
it's centered on the screen giving it some decent size. Than you can quickly
show this window with mod+o key. If you hit it twice, it disappears.

This is cool feature, I like to have an extra terminal there for quick looks
while I am working. Maybe you want your favourite e-mail application there. Or
something other you want to keep hidden`n`handy.

Please note floating applications always stays on top of tiled containers. So
scratchpad is not intended for long tasks. It's better for short tasks you
need to do many times a day. Oh, you can open scratchpad on top of any
workspace you want. This is also great for copy and paste.

    # resize window (you can also use the mouse for that)
    mode "resize" {
      # These bindings trigger as soon as you enter the resize mode
      bindsym j resize shrink width 10 px or 10 ppt
      bindsym k resize grow height 10 px or 10 ppt
      bindsym l resize shrink height 10 px or 10 ppt
      bindsym semicolon resize grow width 10 px or 10 ppt
      #bindsym uring resize grow width 10 px or 10 ppt

      # same bindings, but for the arrow keys
      bindsym 113 resize shrink width 10 px or 10 ppt
      bindsym 116 resize grow height 10 px or 10 ppt
      bindsym 111 resize shrink height 10 px or 10 ppt
      bindsym 114 resize grow width 10 px or 10 ppt

      # back to normal: Enter or Escape
      bindsym Return mode "default"
      bindsym Escape mode "default"
    }

    bindsym $mod+r mode "resize"

I like to resize windows with mouse, but with keys it's more fun and also much
faster. I need to get used to it. You enter resize mode with mod+r
combination, then usint JKL and semicolon (note uring for my Czech layout) you
change the window size. And than you _must_ switch back to the normal mode
with ESC or ENTER key. Standard key bindings are not available in the resize
mode and you will notice why nothing is working. Remember, you _need to
return_.

I bet you can create your own modes like "work" and "fun" with totally
different key bindings. Never tried this.

    # pulse audio volume control
    bindsym XF86AudioLowerVolume exec /usr/bin/pactl set-sink-volume 0 -- '-5%'
    bindsym XF86AudioRaiseVolume exec /usr/bin/pactl set-sink-volume 0 -- '+5%'
    bindsym XF86AudioMute exec /usr/bin/pactl set-sink-volume 0 0
    bindsym XF86Launch1 exec /usr/bin/pactl play-sample that_was_easy
    bindsym XF86MonBrightnessUp exec /usr/bin/xbacklight -inc 10
    bindsym XF86MonBrightnessDown exec /usr/bin/xbacklight -dec 5

Few ThinkPad laptop key bindings for controlling volume, brightness and
ThinkVantage for playing That Was Easy (TM) sample just for fun. I don't use
laptop keyboard much.

    # $mod+n reserved for close all notifications
    # see ~/.config/dunst/dunstrc for more

Just a note for myself not to override mod+n which is used by dunst. More
about it later.

    # one bar on both screens
    bar {
      position top
      mode hide
      modifier $mod
      status_command i3status
      tray_output LVDS1
    }

i3 uses i3bar application to draw a very minimalistic bar that can be
positioned on the top or bottom of the screen (all screens by default). I like
having my bar on top. Content of the bar is delivered with an external program
using IPC - i3status in my case. More about its configuration later.

Only one bar can contain tray area - laptop screen in my case. The bar is very
thin, tray icons are also small. I like it. The "mode hide" statement hides
the bar and opens it once I hit "modifier" key, or on a workspace highlight.
By the way when the bar is hidden, i3 also notifies the i3status program so
it's not feeding with data to save CPU time and thus battery.

By default i3bar shows workspaces and you can switch them with a mouse. It's
good not to disable this (even if you don't use mouse for that) just to have a
nice overview about all workspaces which are kind a dynamic (like in GNOME 3),
they appear once you move there for the first time and disappear when you
leave it (and there is no other container on it). Therefore you can work with
them like in GNOME 3 if you want. I have my numbers 9 and 10 ready for that.

    # workspace screens
    workspace 1 output HDMI1
    workspace 2 output HDMI1
    workspace 3 output HDMI1
    workspace 4 output HDMI1
    workspace 5 output LVDS1
    workspace 6 output LVDS1
    workspace 7 output LVDS1
    workspace 8 output LVDS1

i3 works __very well__ with multiple monitors. The default behavior is where
you create a workspace it stays there forever, or until you disconnect the
screen respectively. Therefore it's up to you where you create your
workspaces.

I like to have an order in this, workspaces 1-4 are on the main screen, 5-8
are on the laptop. Therefore I explicitly say this in my configuration. By
the way you can easily move workspaces across screens, but I don't use any
key bindings for that.

When you disconnect your laptop from dock, everything stays "as is" until
xrandr notice the screen is off. This is not by default and I like this
behavior (depends on your distribution). You can switch off the screen using
xranrd command, but sometimes I prefer to attend a meeting or something and
then returning without _any_ change (having workspaces on the main screen
invisible for a while). I like to have an option in this case. Of course once
i3 determines screen has been turned off using xrandr, it moves all workspaces
to the remaining screen.

You can also do this manually with _i3-msg workspace N output OUTPUT_
therefore I created two bash scripts dock and undock that transfers all my
workspaces in/out of LDVDS1. This is awesome, I really love this feature. I
have never seen a window manager that plays THAT nicely with multiple screens.

    # workspace assignment (use "xprop")
    assign [class="^Google-chrome$"] 3
    assign [class="^URxvt$" instance="^mail$"] 4
    assign [class="^Xchat$"] 5
    assign [class="^Rednotebook$"] 6
    assign [class="^Decibel-audio-player.py$"] 7
    assign [title="Lingea Lexicon 5$"] 8

    # custom window settings
    for_window [class="^URxvt$" instance="scratchpad"] border 1pixel; move scratchpad
    for_window [class="^Google-chrome$"] border none
    for_window [title="Lingea Lexicon 5$"] border none

    # get elluminate working
    for_window [title="^Elluminate Live!"] floating enable
    for_window [title="^Application Sharing"] floating enable
    for_window [class="^net-sourceforge-jnlp-runtime-Boot$" title="^Downloading"] floating enable

In this block, I force some applications to start on specific screens. You can
see apps that I use everyday. IRC chat, notebook, audio player, dictionary,
browser and that's it.

Than if I start a terminal with the name of "scratchpad" it changes its border
to 1pixel and moves to the background -- scratchpad, remember? This is cool.

And I need to use Elluminate application for desktop sharing and meetings.
It's a Java application that does not look nice in the tiled mode, therefore I
force it into floating mode. Good news is it is working actually, if you use
it with Sun JRE. There are not many window managers Elluminate is working in,
seriously.

    # before autostart
    exec --no-startup-id pactl upload-sample ~/.i3/that_was_easy.wav that_was_easy
    exec urxvt -name scratchpad -e bash
    exec ~/.i3/autostart

    # autostart
    exec google-chrome
    exec urxvt -name mail -e bash -c "mutt"
    exec xchat
    exec rednotebook
    exec decibel-audio-player
    exec lexicon

The last block is just auto starting some applications during startup. I load
the funny sample, open a scratchpad terminal (which goes to the background
automatically) and then I start a shell script with additional commands. I
could put this into .xinitrc, but I keep it here. And then some applications.

When I start my laptop, I get the same. Everyday. Cool, isn't it?

## Autostart

My autostart script triggers some settings and spawns some daemons. It's
totally optional in i3, you could do everything using "exec" commands, but I
leveraged my old xinitrc script for that. Let's do the showcase again.


    #!/bin/sh

    ## Desktop background color
    xsetroot -solid '#101010' &

Again, i3 is a window manager, not a desktop environment. I don't like
"wallpapers, I just set a decent color here.

    ## Set startup volume
    pactl set-sink-volume 0 '20%' &

I hate random volume after start. Can cause injuries with my speakers.
Every time I start my laptop, volume is set to 20 per cent.

    ## Disable beeps
    xset -b &

Don't like PC-speaker beeping at all.

    ## Keybord layout setting
    setxkbmap -layout cz,us -option grp:shift_shift_toggle &

I told you -- Czech layout.

    ## DPMS monitor setting (standby -> suspend -> off) (seconds)
    xset dpms 300 600 900 &

I do not use screen "savers", blank it after 5 minutes, suspend and then go
off after 5+5 minutes. THIS is screen saving.

    ## Set LCD brightness
    xbacklight -set 90 &

The same story as with volume, backlight set to 90 % after start.

    ## Clipboard manager
    LC_ALL=C parcellite &

Parcellite clipboard manager is widely used, and I love it for my patches that
strips whitespace. Go ahead, try it and enable this feature in the
preferences. Czech translation is totally wrong, therefore I start it in
English.

    ## OSD
    dunst &

And notification daemon. More about it later.

## Bar

As I described earlier, i3bar program uses i3status -- lightweight status
generator designed to be very efficient by issuing a very small number of
system calls. No scripting support, no external commands. Communication with
i3bar is very simple using pipes, if you really need an external command, you
can create a wrapper that adds some more info to the i3status output. 

Configuration is pretty straightforward, I will not comment that. I refresh
the status line every four seconds, but my bar is hidden most of time,
therefore refreshing is suspended which saves you even more cpu ticks!

    general {
      colors = true
      interval = 4
    }

    order += "disk /home"
    order += "disk /"
    order += "run_watch VPN"
    order += "wireless wlan0"
    order += "ethernet em1"
    order += "battery 0"
    order += "volume master"
    order += "load"
    order += "time"

    wireless wlan0 {
      format_up = "W: (%quality at %essid) %ip"
      format_down = "W: down"
    }

    ethernet em1 {
      # sudo setcap cap_net_admin=ep $(which i3status)
      format_up = "E: %ip (%speed)"
      format_down = "E: down"
    }

    battery 0 {
      format = "%status %percentage %remaining"
    }

    run_watch VPN {
      pidfile = "/var/run/openvpn.pid"
    }

    time {
      format = "%d.%m.%Y %H:%M"
    }

    load {
      format = "%1min"
    }

    disk "/" {
      format = "%free"
    }

    disk "/home" {
      format = "%free"
    }

    volume master {
      format = "♪: %volume"
      device = "default"
      mixer = "Master"
      mixer_idx = 0
    }

To test it, you can just run _i3status_. It will fall back to simple text
output (real communication with i3bar is with colors):

    $ i3status 
    132,1 GB | 56,2 GB | VPN: yes | W: down | E: 192.168.1.1 (1000 Mbit/s) | FULL 55,92% | ♪: 63% | 1,56 | 28.08.2012 19:46

As you may noticed, my ThinkPad battery is dying.

## OSD

I use dunst as a notification daemon. It's very simple and it looks like a
dmenu. The configuration is stored in _~/.config/dunst/dunstrc_ and the
default one works great. And it also plays well with multi-monitor setups -
you can choose screen to show notifications on and it can also follow your
mouse or keyboard (pops up on the screen you actually work on).

Dunst can group same messages, stack them, sort them by urgency, wrap words
and keep messages when computer is in idle (so you would miss them). One can
configure colors, format and other basic things for the pop up windows.

I took the default configuration from _/usr/share/dunst/dunstrc_ and kept the
sane defaults. The most important setting change for me was:

    close_all = mod4+n

I use Win+n to close all notifications. Nice.

## Wrap-up

Okay, I think I showed you [i3][5]. Highly recommended tiling window manager.
Share your opinions on this page with me!

__Update__: I have pushed all my configuration files to [git repository][6].

[1]: http://www.youtube.com/watch?v=QnYN2CTb1hM
[2]: https://bugzilla.redhat.com/show_bug.cgi?id=852211
[3]: http://pulpproject.org
[4]: http://i3wm.org/docs/userguide.html#_changing_the_container_layout
[5]: http://i3wm.org
[6]: https://github.com/lzap/doti3
