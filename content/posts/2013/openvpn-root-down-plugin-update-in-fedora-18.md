---
type: "post"
aliases:
- /2013/05/openvpn-root-down-plugin-update-in-fedora-18.html
date: "2013-05-23T00:00:00Z"
tags:
- linux
- fedora
title: OpenVPN root down plugin update in Fedora 18
---

You may noticed that with recent bunch of updates your OpenVPN client may
stopped working. The error was:

    Thu May 23 09:26:35 2013 PLUGIN_INIT: could not load plugin shared object
    /usr/lib64/openvpn/plugin/lib/openvpn-down-root.so:
    /usr/lib64/openvpn/plugin/lib/openvpn-down-root.so: cannot open shared object
    file: No such file or directory: No such file or directory (errno=2)
    Thu May 23 09:26:35 2013 Exiting due to fatal error

The openvpn package version was bumped in Fedora 18 for some reasons from 2.2
to 2.3. In the new version, the down root plugin has been renamed. If your
OpenVPN script had this line:

    plugin /usr/lib64/openvpn/plugin/lib/openvpn-down-root.so /etc/openvpn/client.down

or

    plugin openvpn-down-root.so /etc/openvpn/client.down

You need to change it to

    plugin openvpn-plugin-down-root.so /etc/openvpn/client.down

Note that path has changed too, from /usr/lib64/openvpn/plugin/ to
/usr/lib64/openvpn/plugins/, but you usually don't need to provide it.

Take care!
