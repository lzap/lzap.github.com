---
type: "post"
aliases:
- /2013/03/never-lost-your-bash-history-again.html
date: "2013-03-11T00:00:00Z"
tags:
- linux
- fedora
- bash
title: Never lost your bash history again
---

I had a cronjob which was archiving my bash history file, but after one of my
Fedora upgrades, it stopped working and I lost my .bash_history. Now, that's
unfortunate!

To prevent this in the future, I have decided to take different approach. I
have a script now which I run from my bash profile. It creates backups every
month (leaving last 200 commands there so I will not lost the latest
commands). Since I have this in my profile, it will work forever.

The script is lightweight and basically it only adds one extra check - if
backup is older than latest bash history file, copy it over. So this should
not slow down my bash startup at all (basically one cp command a day when I
start my laptop or when I append a history in a terminal).

Here it is:

    #!/bin/sh
    # This script creates monthly backups of the bash history file. Make sure you have
    # HISTSIZE set to large number (more than number of commands you can type in every
    # month). It keeps last 200 commands when it "rotates" history file every month.
    # Typical usage in a bash profile:
    #
    # HISTSIZE=90000
    # source ~/bin/history-backup
    #
    # And to search whole history use:
    # grep xyz -h --color ~/.bash_history.*
    #

    KEEP=200
    BASH_HIST=~/.bash_history
    BACKUP=$BASH_HIST.$(date +%y%m)

    if [ -s "$BASH_HIST" -a "$BASH_HIST" -nt "$BACKUP" ]; then
      # history file is newer then backup
      if [[ -f $BACKUP ]]; then
        # there is already a backup
        cp -f $BASH_HIST $BACKUP
      else
        # create new backup, leave last few commands and reinitialize
        mv -f $BASH_HIST $BACKUP
        tail -n$KEEP $BACKUP > $BASH_HIST
        history -r
      fi
    fi

