---
type: "post"
aliases:
- /2014/05/systemtap-as-a-system-wide-strace-tool.html
date: "2014-05-16T00:00:00Z"
tags:
- linux
- fedora
- systemtap
title: SystemTap as a system wide strace tool
---

I needed to find a process that was searching for several file patterns. I
could use strace tool but since this one was a Apache2 module, I would need to
hack startup scripts and probably create a wrapper script. There was another
way of doing that - using SystemTap.

My problem was simple - I wanted to see process name, pid and full absolute
path for a filename pattern. The goal was set, with little bit of googling, I
was able to write this (not ideal and hacky) SystemTap script:

    $ cat syscall_open.stp
    #!/usr/bin/env stap
    #
    # System-wide strace-like tool for catching file open syscalls.
    #
    # Usage: stap syscall_open filename_regexp
    #
    global myfilename
    probe syscall.open {
      myfilename = filename
    }
    probe syscall.open.return {
      if (myfilename =~ @1) {
        printf ("%s(%d) opened %s -> %d\n", execname(), pid(), myfilename, $return)
      }
    }

Before we can use SystemTap, we need to install those packages (this is for
RHEL6/CentOS6). Note you _do need_ debug info packages, otherwise this will
not work (enable them via subscription-manager or in repo files):

    $ yum -y install systemtap systemtap-runtime kernel-debuginfo-`uname -r` \
        kernel-debuginfo-common-`uname -i`-`uname -r` kernel-devel-`uname -r`

Usage is super simple, you can either make it executable or to see more
verbose output just do:

    $ stap -v syscall_open.stp native_support.so

This is effective for the whole system, after Apache2 httpd server restart and
first access, I was able to find why the heck mod_passenger searches on wrong
paths:

    ruby(4257) opened "/usr/lib/ruby/gems/1.8/gems/passenger-4.0.18/lib/native/passenger_native_support.so" -> -2
    ruby(4257) opened "/opt/rh/ruby193/root/usr/local/share/ruby/site_ruby/native/passenger_native_support.so" -> -2
    ruby(4257) opened "/opt/rh/ruby193/root/usr/local/lib64/ruby/site_ruby/native/passenger_native_support.so" -> -2
    ruby(4257) opened "/opt/rh/ruby193/root/usr/share/ruby/vendor_ruby/native/passenger_native_support.so" -> -2
    ruby(4257) opened "/opt/rh/ruby193/root/usr/lib64/ruby/vendor_ruby/native/passenger_native_support.so" -> -2
    ruby(4257) opened "/opt/rh/ruby193/root/usr/share/rubygems/native/passenger_native_support.so" -> -2
    ruby(4257) opened "/opt/rh/ruby193/root/usr/share/ruby/native/passenger_native_support.so" -> -2
    ruby(4257) opened "/opt/rh/ruby193/root/usr/lib64/ruby/native/passenger_native_support.so" -> -2
    ruby(4257) opened "/usr/share/foreman/.passenger/native_support/4.0.18/ruby-1.9.3-x86_64-linux/passenger_native_support.so" -> -2
    ruby(4257) opened "/usr/share/foreman/.passenger/native_support/4.0.18/ruby-1.9.3-x86_64-linux/passenger_native_support.so.rb" -> -2
    ruby(4257) opened "/usr/share/foreman/.passenger/native_support/4.0.18/ruby-1.9.3-x86_64-linux/passenger_native_support.so.so" -> -2
    ruby(4282) opened "/usr/lib/ruby/gems/1.8/gems/passenger-4.0.18/lib/native/passenger_native_support.so" -> -2
    ruby(4282) opened "/opt/rh/ruby193/root/usr/local/share/ruby/site_ruby/native/passenger_native_support.so" -> -2
    ruby(4282) opened "/opt/rh/ruby193/root/usr/local/lib64/ruby/site_ruby/native/passenger_native_support.so" -> -2
    ruby(4282) opened "/opt/rh/ruby193/root/usr/share/ruby/vendor_ruby/native/passenger_native_support.so" -> -2
    ruby(4282) opened "/opt/rh/ruby193/root/usr/lib64/ruby/vendor_ruby/native/passenger_native_support.so" -> -2
    ruby(4282) opened "/opt/rh/ruby193/root/usr/share/rubygems/native/passenger_native_support.so" -> -2
    ruby(4282) opened "/opt/rh/ruby193/root/usr/share/ruby/native/passenger_native_support.so" -> -2
    ruby(4282) opened "/opt/rh/ruby193/root/usr/lib64/ruby/native/passenger_native_support.so" -> -2
    ruby(4282) opened "/usr/share/foreman/.passenger/native_support/4.0.18/ruby-1.9.3-x86_64-linux/passenger_native_support.so" -> -2
    ruby(4282) opened "/usr/share/foreman/.passenger/native_support/4.0.18/ruby-1.9.3-x86_64-linux/passenger_native_support.so.rb" -> -2
    ruby(4282) opened "/usr/share/foreman/.passenger/native_support/4.0.18/ruby-1.9.3-x86_64-linux/passenger_native_support.so.so" -> -2

SystemTap is awesome tool. It helps me every week :-)

