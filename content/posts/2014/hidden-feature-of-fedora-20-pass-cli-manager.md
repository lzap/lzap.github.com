---
type: "post"
aliases:
- /2014/04/hidden-feature-of-fedora-20-pass-cli-manager.html
date: "2014-04-15T00:00:00Z"
tags:
- linux
- fedora
title: Hidden feature of Fedora 20 - pass cli manager
---

When it comes to password management, I've always been happy user of KeepassX
for many years. But when I stumbled upon new and simple tool called "pass" and
I realized that I use mouse (trackball actually) with only two applications:
Google Chrome and, of course, KeepassX in my workflow (i3, mutt, vim, ssh).

This tool is basically a shell wrapper around gpg, git and few other tools:

    # yum install pass pinentry-gtk

It's definitely not a monster tool, which I appreciate:

    # rpm -ql pass
    /etc/bash_completion.d/password-store
    /usr/bin/pass
    /usr/share/doc/pass
    /usr/share/doc/pass/COPYING
    /usr/share/doc/pass/README
    /usr/share/man/man1/pass.1.gz

Let's read the completion (or re-login to your shell):

    # source /etc/bash_completion.d/password-store

What you want is to create separate gpg key for your passwords:

    # gpg --gen-key

Give it a name (you can skip the e-mail) and comment. In my case this was
"Lukas Zapletal (my passwords)". You will not share this one at all. And make
sure to use safe master password (passphrase).

Now you want to load gpg agent. Make sure you put this in your .bashrc as
well, otherwise you would need to put your master password over and over
again:

    # eval "$(gpg-agent --daemon 2>/dev/null)"

In Fedora, *do not* miss the step of starting a gpg-agent, otherwise pass will
not work as it spawns gpg with `--batch` parameter. If you do not like
gpg-agent, you need to remove this option from `/usr/bin/pass` or upgrade to
the latest upstream version 1.5+ which does not have this.

The (pass)[http://www.zx2c4.com/projects/password-store/] tool provides many
helper scripts and importers including keepassx2pass.py which works great (you
need to export your database to the XML format first). Setting up my database
was matter of two minutes. A bit of warning - if you have multiline comments,
note that the KeepassX importer only fetches the first comment (I'll push a
fix for that most likely).

Usage is simple enough:

    # pass init "Lukas Zapletal (pass)"
    # pass insert Business/cheese-whiz-factory
    # pass -c Email/zx2c4.com
    Copied Email/jason@zx2c4.com to clipboard. Will clear in 45 seconds.

Upgrade to "pass", your whist will appreciate that.

