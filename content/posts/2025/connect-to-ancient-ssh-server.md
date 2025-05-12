---
title: "Connect to Ancient SSH Server"
date: 2025-05-12T15:02:59+02:00
type: "post"
tags:
- linux
- fedora
- ssh
---

Modern Linux distributions configure OpenSSH client to refuse connecting to
servers without newer ciphers or key exchange algos. Symptoms are:

    Unable to negotiate with 192.168.200.83 port 22: no matching host key type found. Their offer: ssh-rsa,ssh-dss

The solution is clunky, so I created a small Debian-based container with
OpenSSH client installed, it is an "oldstable" version old enough not to have a
modern SSH client with modern configuration. Usage:

    podman run -it --rm ghcr.io/lzap/old-ssh-client:latest ssh root@192.168.122.2

You can inspect the container here: https://github.com/lzap/old-ssh-client
