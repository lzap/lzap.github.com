---
type: "post"
aliases:
- /2020/01/samba-and-nfs-shared-folder-on-centos8.html
date: "2020-01-11T00:00:00Z"
tags:
- linux
- fedora
title: Samba and NFS shared folder on CentOS 8
---

Setting up a shared (guest) read-write folder across Samba and NFS was a piece
of cake on CentOS 8. I've also thrown Avahi daemon into the mix so all three
platforms we have in our family can easily access our data. Here are my notes.

First of, I've put my ethernet into trusted zone because I don't want to deal
with firewall in my home network. I am running one on router. You should
probably not do this.

    firewall-cmd --zone=trusted --change-interface=eno1
    firewall-cmd --zone=trusted --change-interface=eno1 --permanent

For the record, my new NAS server is simply an 8th gen Intel NUC with a SSD for
the OS and 2 TB Seagate drive for data. I don't have much content just photos
basically, unfortunately the bay is 9mm and there are no bigger 2.5-sized disks
available. My plan is to extend it later with an external 4-6 TB USB3 or
Thunderbolt HDD. I've configured LVM and the internal drive is mounted at
`/mnt/int`. I don't use RAID on my home NAS servers because I believe it's not
necessary - I can live with couple of days downtime until new disk arrives.
Remember: RAID is not a backup! I regularly backup all the data to a remote
location.

Overall goal is simple: have a single shared folder between Samba and NFS
mounted read-write with SELinux turned on with minimum configuration as
possible.

I've installed Samba, NFS server, SELinux utilities and Avahi daemon:

    dnf install samba samba-client nfs-utils policycoreutils-python-utils avahi

Configuration of Samba could have been more simple as many of these values are
probably default ones, I was just experimenting a bit and it won't hurt for
sure. This is /etc/samba/smb.conf:

    [global]
        netbios name = NUC
        workgroup = WORKGROUP
        local master = yes
        security = user
        passdb backend = tdbsam
        guest account = nobody
        map to guest = Bad User
        logging = systemd
        log level = 0
        load printers = no

    [data]
        comment = Data
        path = /mnt/int/data
        browseable = yes
        writeable = yes
        public = yes
        read only = no
        guest ok = yes
        guest only = yes
        force create mode = 0664
        force directory mode = 0775
        force user = nobody
        force group = nobody

The important SELinux "trick" was to configure file context correctly, so both
NFS and Samba can access read and write it:

    semanage fcontext -a -t public_content_rw_t "/mnt/int(/.*)?"
    restorecon -RvvF /mnt/int

Both services also need to be allowed to write content:

    setsebool -P allow_smbd_anon_write=1
    setsebool -P allow_nfsd_anon_write=1

Configuration of NFSv4 in RHEL 8 (CentOS 8) is super easy. If you remember the
pain of configuring firewalls with with older NFS versions like me, you want to
disable those services completely. This step is optional if you want to allow
legacy NFS clients:

    /etc/nfs.conf:
    [nfsd]
    vers2=no
    vers3=no

Stop and disable NFS services which are not needed for NFSv4:

    systemctl mask --now rpc-statd.service rpcbind.service rpcbind.socket

End of the optional step. Configuration of NFS server is super easy (compare to
Samba):

    /etc/exports:
    /mnt/int/data *(rw,async,all_squash,anonuid=65534,anongid=65534)

Since NFS server comes preinstalled in the default server CentOS8 installation
profile, I restarted it.

    systemctl restart nfs-server

And enabled Samba and Avahi services:

    systemctl enable --now nmb.service smb.service nfs-server.service avahi-daemon.service

That's really all. Testing is easy, install `samba-client` package and do:

    smbclient -U guest //nuc/data

To test NFS, just mount the directory:

    mount -t nfs nuc:/mnt/int/data /mnt/nuc

Hope the article helped you to achieve shared folder at home. This is not
recommended setup for work or coffeeshops. And remember to do regular backups
(not copies), because people can accidentaly rename, overwrite or delete files!

Drop me a comment or share via Twitter please. Have a good one.

