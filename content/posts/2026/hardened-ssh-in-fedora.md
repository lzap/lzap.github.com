---
title: "Hardened ssh in Fedora 43"
date: 2026-03-25T07:50:03+01:00
type: "post"
tags:
- linux
- fedora
---

If you have a Fedora 43 (or older) system with public IP with ssh port opened,
you are probably getting a lot of records like these:

```
sshd-session[20884]: refusing RSA key: Invalid key length [preauth]
sshd-session[31595]: Invalid user shop from 172.94.9.155 port 37434
sshd-session[57487]: Connection closed by 139.0.12.92 port 62968
```

These are scripts, bots or AI, trying to get in. As you already know, password
authentication is not something that should be used in 2026, so you are fine
with public keys. But still, this is polluting the system journal.

There are three solutions that can dramatically bring the number of logs to
almost zero and you can combine them all. Let's take a look.  Before you do any
ssh configuration, always have at least 2 connections so if you mess up, you
still have a chance to fix it.

## Hardening ssh configuration

There are many ways how you can harden ssh, but the very basic configuration I
use is something like one I have in `/etc/ssh/sshd_config.d/harden.conf`:

```
# You already have this, if not, do it immediately.
PasswordAuthentication no

# This is turned on by default, just check this.
PubkeyAuthentication yes

# Never permit this.
PermitRootLogin no

# Do not allow trying too many times.
MaxAuthTries 2

# Only allow me in.
AllowUsers lzap

# Only 5 seconds to type in password.
LoginGraceTime 5

# But when connecting from my home network things are different.
Match Address 192.168.1.0/24,127.0.0.1
    # Allow root but only with pubkeys.
    PermitRootLogin prohibit-password

    # Allow password typos more times than just 2 when having a bad day. :)
    MaxAuthTries 5

    # And finally, allow root for these IPs.
    AllowUsers root lzap
```

As you can see, security for my home network is a bit loose, perhaps too much.
You make your own decision how much you want to do any of that. Also, you
should skip the `Match` section if you do not access your server directly from
local network.

## Deploying fail2ban

A sweet utility that can ban IP address if they misbehave, like trying to sign
in too many times. There are so many fail2ban tutorials out there, so why a new
one? Well, I wanted a configuration that utilizes `nftables` through
`firewalld` on my Fedora because I always want modern solutions. For this
reason, I have the following in `/etc/fail2ban/action.d/firewallcmd-modern.conf`:

```
[Definition]

actionstart = firewall-cmd --permanent --new-ipset=f2b-<name> --type=hash:ip >/dev/null 2>&1 || true
              firewall-cmd --permanent --add-rich-rule='rule priority="-10" family="ipv4" source ipset="f2b-<name>" service name="<service>" reject' >/dev/null 2>&1 || true
              firewall-cmd --reload

actionstop = firewall-cmd --permanent --remove-rich-rule='rule priority="-10" family="ipv4" source ipset="f2b-<name>" service name="<service>" reject' >/dev/null 2>&1 || true
             firewall-cmd --permanent --delete-ipset=f2b-<name> >/dev/null 2>&1 || true
             firewall-cmd --reload

actionflush = nft flush set inet firewalld f2b-<name>

actionban = firewall-cmd --ipset=f2b-<name> --add-entry=<ip>
actionunban = firewall-cmd --ipset=f2b-<name> --remove-entry=<ip>

[Init]
service = ssh
```

This creates new ipset called `f2b-ssh` in firewalld or deletes it on service
start or stop. It needs to be permanent because this is the way firewalld does
it. And then the add and remove commands are straightforward. The main config
is in `/etc/fail2ban/jail.local`:

```
[DEFAULT]
backend = systemd
banaction = firewallcmd-modern
bantime = 1w
findtime = 1d
maxretry = 2

[Definition]
logtarget = SYSLOG

[sshd]
enabled = true
```

I tried to use the original
[firewallcmd-ipset](https://github.com/fail2ban/fail2ban/blob/master/config/action.d/firewallcmd-ipset.conf)
that comes with fail2ban but it does not work on Fedora 43 because things are
moving fast there!

Enable and start fail2ban service which will decrease number of logs slightly.
But to do more, let's add one small thing.

## GeoIP blocking

A very radical solution is to create a small script
`/etc/cron.daily/update-ssh-blacklist` that will block all SSH connection from
a particular country:

```
#!/bin/bash
COUNTRIES="cn ru br"
IPSET_NAME="blacklist_countries"
TMP_DIR=$(mktemp -d /tmp/ssh_blacklist.XXXXXX)
trap 'rm -rf "$TMP_DIR";' EXIT INT TERM

if ! firewall-cmd --get-ipsets | grep -q "$IPSET_NAME"; then
        echo "Creating firewalld ipset $IPSET_NAME"
        firewall-cmd --permanent --new-ipset=$IPSET_NAME --type=hash:net >/dev/null
fi

RULE="rule priority='-20' family='ipv4' source ipset='$IPSET_NAME' service name='ssh' drop"
if ! firewall-cmd --query-rich-rule="$RULE" >/dev/null; then
        echo "Applying rule $RULE"
        firewall-cmd --add-rich-rule="$RULE" >/dev/null
fi

CURRENT_ENTRIES="$TMP_DIR/current_entries.list"
firewall-cmd --ipset=$IPSET_NAME --get-entries > "$CURRENT_ENTRIES"
if [ -s "$CURRENT_ENTRIES" ]; then
        echo "Removing $(wc -l < "$CURRENT_ENTRIES") old entries..."
        firewall-cmd --ipset=$IPSET_NAME --remove-entries-from-file="$CURRENT_ENTRIES" >/dev/null
fi

for country in $COUNTRIES; do
        ZONE_FILE="$TMP_DIR/${country}.zone"
        CLEAN_FILE="$TMP_DIR/${country}_clean.zone"

        if curl -s -L "http://www.ipdeny.com/ipblocks/data/countries/${country}.zone" -o "$ZONE_FILE"; then
                # Filter: digits only, exclude local IPs
                grep -E '^[0-9]' "$ZONE_FILE" | grep -v -E '^(192\.168\.|127\.0\.)' > "$CLEAN_FILE"

                firewall-cmd --ipset=$IPSET_NAME --add-entries-from-file="$CLEAN_FILE" >/dev/null
                echo "Blacklisting: $country ($(wc -l < "$CLEAN_FILE"))"
        fi
done

echo "Done"
```

Update the list of countries, for me China and Russia works the best, might be
different countries for you. Make it executable and run it. Chances are this
will dramatically lower number of unsuccessful connections to your SSH. Worked
for me!

## Bonus: three connections per minute

This bonus section is for those who, like me, use NAT port forwarding to access
a private network. It is possible to further harden your setup by limiting SSH
connections to just three per minute. However, keep in mind that this is a very
strict policy which may disrupt your workflow—especially when using tools like
VSCode over SSH that open multiple sessions. For this reason, I recommend
applying the limit only to external traffic while keeping your internal network
(192.168.0.0/16) unrestricted.

```
firewall-cmd --permanent --add-rich-rule='rule priority="-100" family="ipv4" source address="192.168.0.0/16" service name="ssh" accept'
firewall-cmd --permanent --add-rich-rule='rule priority="50" family="ipv4" service name="ssh" accept limit value="3/m"'
firewall-cmd --permanent --add-rich-rule='rule priority="100" family="ipv4" service name="ssh" drop'
firewall-cmd --reload
```

Beware that these commands can cut you from SSH if you do it incorrectly, skip
the bonus section if you do not know what you are doing! Also, in case you
already applied these rules and do not know how to reverse this, just replace
`--add-rich-rule` with `--remove-rich-rule` and reload.

## Monitoring

To see how fail2ban is doing, use `fail2ban-client status sshd` but to also see
GeoIP blocked IPs, you can use `nft list sets`:

```
table ip libvirt_network {
}
table ip6 libvirt_network {
}
table ip filter {
}
table inet firewalld {
	set blacklist_countries {
		type ipv4_addr
		flags interval
		elements = {
          ...
        }
	}
	set f2b-sshd {
		type ipv4_addr
		flags interval
		elements = {
          ...
        }
	}
}
```

It can be a very long output but do not worry - this is stored very efficiently
in memory hash tables.

Okay, less logging, done.
