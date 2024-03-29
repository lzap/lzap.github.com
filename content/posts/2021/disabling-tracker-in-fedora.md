---
type: "post"
aliases:
- /2021/02/disabling-tracker-in-fedora.html
date: "2021-02-02T00:00:00Z"
tags:
- linux
- fedora
title: Disabling Tracker in Fedora
---

I have realized that one of the tracker processes is dying every few seconds on
my Fedora 33, I got ton of ABRT reports and system log filled with stacktraces.
Bugs happen, however I don't actually utilize this tool very much. Searching in
contacts, files, browser history, photos, documents of files is nothing I use.
There are also other Gnome features which might stop working such as Boxes
offering ISO files, audio player suggesting music or File browser's advanced
features like tagging of files.

So think twice before you turn off Tracker daemon. I use command line a lot,
that's where I search for files, start virtual machines, listen music or even
watch video content. You have been warned!

To turn off tracking open up Settings - Search (or just type "search") and turn
it off globally. It's possible to turn off specific locations like contacts or
calendar if you want.

Then, delete tracker database completely:

	$ tracker reset -r
	CAUTION: This process may irreversibly delete data.
	Although most content indexed by Tracker can be safely reindexed, it can?t be assured that this is the case for all data. Be aware that you may be incurring in a data loss situation, proceed at your own risk.

	Are you sure you want to proceed? [y|N]: y
	Found 1 PID?
	  Killed process 24088 ? ?tracker-miner-fs-3?
	_g_io_module_get_default: Found default implementation dconf (DConfSettingsBackend) for ‘gsettings-backend’
	Setting database locations
	Checking database directories exist
	Checking database version
	Checking whether database files exist
	Removing all database/storage files
	  Removing database:'/home/lzap/.cache/tracker/meta.db'
	  Removing db-locale file:'/home/lzap/.cache/tracker/db-locale.txt'
	  Removing journal:'/home/lzap/.local/share/tracker/data/tracker-store.journal'
	  Removing db-version file:'/home/lzap/.cache/tracker/db-version.txt'

That's all. Searching for applications via "Windows" key will keep working,
this feature I use a lot.

To enable tracker back, just go to the Settings and enable it. Cheers!
