---
type: "post"
aliases:
- /2021/02/what-is-waking-my-hdd-up-in-linux.html
date: "2021-02-22T00:00:00Z"
tags:
- linux
- fedora
title: What is waking my HDD up in Linux
---

When my disks wake up during the day, I am angry. I want silence, so I started investigating which process makes them to do that. I suspect that something is browsing Samba share, but to confirm I created this simple SystemTap script:

	# cat syscall_open.stp 
	#!/usr/bin/env stap
	#
	# System-wide strace-like tool for catching file open syscalls.
	#
	# Usage: stap syscall_open filename_regexp
	#
	probe syscall.open* {
	  if (filename =~ @1) {
	    printf("%s(%d) opened %s\n", execname(), pid(), filename)
	  }
	}

It's as easy as starting this up and waiting until the process is found. It accepts regular expression, not a glob:

	# dnf install systemtap systemtap-runtime
	# stap syscall_open.stp '/mnt/int/data.*'

This will work on all SystemTap operating systems, I tested this on Fedora and any EL distribution should work too.


