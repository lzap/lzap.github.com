---
title: "Directory Similarity Comparison Tool: walkalike"
date: 2025-04-24T08:00:03+02:00
type: "post"
tags:
- linux
- fedora
- golang
---

I wrote a small but fast tool called
[walkalike](https://github.com/lzap/walkalike) which calculates how two or more
filesystem trees (or OS images) are similar. Usage:

    walkalike dir1 dirN

Processing is optimized for SSDs and index creation is parallelized. Example
command:

    walkalike testdata/a testdata/b

Should print:

    0.4444444444444 testdata/a testdata/b

Similarity coefficient is between 0.0, when two trees are not similar at all,
or 1.0, when two trees are exactly the same. When multiple directories are
provided, the first directory is compared against 2nd, 3rd and so on.

    walkalike testdata/a testdata/b testdata/c

Should print:

    0.4444444444444 testdata/a testdata/b
    0.9814814814815 testdata/a testdata/c

The tool support listing files inside OS images, it requires the tool `virt-ls`
to be installed:

    sudo dnf -f install guestfs-tools

The utility from guestfs-tools is executed as a subprocess and automatically
detect OS image, finds root partition and walks the directory tree passing
results and checksums to the parent process which calculates the index.

    walkalike a-fedora-40-minimal-raw-x86_64.raw b-fedora-40-minimal-raw-x86_64.raw

Building the indices will take a little bit more time as walking the tree is
not parallelized and some images might be compressed but the result is exactly
the same:

    0.9995304751005 a-fedora-40-minimal-raw-x86_64.raw b-fedora-40-minimal-raw-x86_64.raw

Use releases page on github to download binary for your OS and architecture.
Cheers!
