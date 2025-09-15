---
type: "post"
aliases:
- /2017/07/git-auto-fetch-script-i-run-every-day.html
date: "2017-07-17T00:00:00Z"
tags:
- linux
- fedora
- git
title: Git auto fetch script I run every day
---

I am "shutdowner", meaning I always shutdown my laptop (now workstation) at
the end of the day. I have a script to do that which sleeps 5 seconds (so I
can change my mind - e.g. when I dig shell history incorrectly and quickly hit
enter - it really happened yeah) and it is simple:

* puts my monitors into standby mode
* applies all OS updates
* runs duplicity backup on my home folder
* fetches git repos
* filesystem sync call
* fstrim root volume
* poweroff

I learned a trick I want to write about today from colleague of mine Mirek
Suchý, but I think he runs it from cron (not a "shutdowner" guy). The idea is
simple:

* find all directories containing .git/ and run on all of them:
* git fetch --all
* git gc

So every time I do git pull on a repo that I don't use much (e.g. ruby
language), I don't need to wait seconds in order to pull all commits. Clever,
now I've improved it a bit.

With my Ryzen 1700 8 core 16 threads CPU, I am able to leverage GNU parallel
to do this in parallel. That will be faster. But how much? Let's test against
git repo I use the most: www.theforeman.org.

    # git -c pack.threads=1 gc --aggressive
    1m25.175s

    # git -c pack.threads=16 gc --aggressive
    0m16.321s

Initially I thought that running 16 GNU parallel worker processes of parallel
will be fine, but git gc is really slow on one core (see above), so I usually
end up with several very slow garbage tasks while all the others finished
downloading. The sweet spot for git is around 4 threads where it always gives
reasonable times even for bigger repos.

But I think little bit of CPU overcommit won't kill, therefore I've decided to
go with 8x4 which might sound crazy (32 threads in theory), but in practice
garbage collect is executed only on few repositories I work regularly on.

Lot of words, I know. Here is the snippet:

    find ~/work -name '.git' -type d | \
        parallel -j 6 'pushd "{}"; git fetch --all; git -c pack.threads=4 gc --aggressive --no-prune --auto; popd'

I think I could go further but this already gives me good experience and when
my PC is doing this, I am already heading away from it. No biggie. Final notes
for git flags I use:

* aggressive - much slower collect giving better results
* no-prune - I don't want to loose any commits at any point in time
* auto - git will decide when to actually run gc

