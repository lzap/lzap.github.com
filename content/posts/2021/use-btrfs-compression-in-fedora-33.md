---
type: "post"
aliases:
- /2021/02/use-btrfs-compression-in-fedora-33.html
date: "2021-02-21T00:00:00Z"
tags:
- linux
- fedora
title: Use btrfs compression in Fedora 33
---

Btrfs have been available in Fedora for quite some time and starting from
Fedora 33, new installations of Workstation edition use it by default. Btrfs is
pretty capable file system with lots of options, let's take a look on one
aspect: transparent per-file compression.

There's little bit of misunderstanding how this works and some people recommend
to mount with `compress` option. This is actually not necessary and I would
actually strongly suggest NOT to use this option. See, this option makes btrfs
to attempt to compress all files that are being written. If the beginning of a
file cannot be effectively compressed, it's marked as "not for compression" and
this is never attempted again. This can be even forced via a different option.
This looks nice on paper.

The problem is, not all files are good candidates for compression. Compression
takes time and it can dramatically worsen performance, things like database
files or virtual machine images should never be compressed. Performance of
libvirt/KVM goes terribly down by order of magnitude if an inefficient backing
store is used (qcow2).

I suggest to keep the default mount options Anaconda installer deploys, note
there is none related to compression. Instead, use per-file (per-directory)
feature of btrfs to mark files and directories to be compressed. A great
candidate is `/usr` which contains most of the system including binaries or
documentation.

One mount option is actually useful which Anaconda does not set by default and
that is `noatime`. Writing access times for copy on write file system can be
very inefficient. Note this option implies `nodiratime` so it's not necessary
to set both.

To enable compression for `/usr` simply mark this directory to be compressed.
There are several compression algorithms available: zlib (slowest, best ratio),
zstd (decent ratio, good performance) and lzo (best performance, worse ratio).
I suggest to stick with zstd which lies in the middle. There are also
compression level options, unfortunately the utility does not allow setting
those at the time of writing. Luckily, the default level (3) is reasolable.

	# btrfs property set /usr compression zstd

Now, btrfs does not immediately start compressing contents of the directory.
Instead, everytime a file is written data in those blocks is compressed. To
explicitly compress all files recursively, do this:

	# btrfs filesystem defragment -r -v -czstd /usr

Let's find out how much space have we saved:

	# compsize /usr
	Processed 55341 files, 38902 regular extents (40421 refs), 26932 inline.
	Type       Perc     Disk Usage   Uncompressed Referenced  
	TOTAL       50%      1.1G         2.2G         2.3G       
	none       100%      337M         337M         338M       
	zstd        42%      844M         1.9G         1.9G  

Exactly half of space is saved on a standard installation of Fedora 33 Server
when `/usr` is compressed using zstd algorithm with the default level. Note
some files are not compressed, these are too small files when it does not make
any sense (a block would be used anyway). Not bad.

To disable compression perform the following command:

	# btrfs property set /usr compression ""

Unfortunately, at the time of writing it is not possible to force decompression
of a directory (or files), there is no defragment command to do this. If you
really need to do this, create a script which reads and writes all files but be
careful.

Keep in mind the `btrfs property` command will *force* all files to be
compressed, even if they do not compress well. This will work pretty well for
`/usr` just make sure there is no 3rd party software installed there writing
files. There is also a way to mark files for compression and if they don't
compress well btrfs could give up on it. You can do that by setting `chattr +c`
on files or directories.  Unfortunately, you can't set compression algorithm
that way - btrfs will default to slower `zlib`.

Remember: Do not compress everything, specifically directory `/var` should
definitely not be compressed. If you happened to accidentally mark files
within `/var` to be compressed, you can fix this with:

	# find /var -exec btrfs property set {} compression "" \;

Again, this will only mark them not to be compressed, it's currently not
possible to explicitly decompress them. Use the `compsize` utility to find out
how much of data is still compressed.

That's all for today, I will probably sharing some more btrfs posts.
