---
type: "post"
aliases:
- /2022/10/send-warning-email-when-your-drive-is-dying.html
date: "2022-10-22T00:00:00Z"
tags:
- linux
- fedora
title: Send warning email when your drive is dying
---

My Samsung 870 EVO 2TB SDD is dying after 13 months of basic workstation
operation. Looks like some problem with a large batch because I found many
other users complaining on forums. I am going for RMA. Fortunately, I restored
from my backup.

Lesson learned: SMART needs to be monitored on my home servers, this is not the
first time and I was lucky enough to see the errors in the system journal in
advance.

How to do that? There are multiple options, there is a shell script which ships
with the smartmontools package, but I could not get it working. So I ended
landing on a simple solution:

	# dnf install smartmontools ssmtp

A dirty shell script will do, note that smartctl utility returns a bit mask so
finding if a drive is healthy is a bit tricky. Luckily, the manpage contains an
example:

	# cat /etc/cron.weekly/smart
	for DRIVE in sda sdb sdc sdd; do
	  smartctl -H /dev/$DRIVE &>/dev/null
	  dying=$(($? & 8))
	  if [[ $dying -ne 0 ]]; then
	    echo "Subject: SMART problem $DRIVE on $(hostname)" | sendmail -v me@example.com
	  fi
	done

Super simple, just an empty email with no body. In case you don't run MTA on
your server like I do:

	# cat /etc/ssmtp/ssmtp.conf
	root=postmaster
	mailhub=smtp.example.com:587
	RewriteDomain=example.com
	Hostname=example.com
	UseTLS=NO
	UseSTARTTLS=YES
	TLS_CA_File=/etc/pki/tls/certs/ca-bundle.crt
	Debug=NO
	AuthUser=me@example.com
	AuthPass=xxxxxxxxxxxx
	AuthMethod=PLAIN

From address must match in order to pass MTA anti-spam filters:

	# cat /etc/ssmtp/revaliases
	root:me@example.com

It's dirty, but it should work.

Update: I had a typo in the script, special thanks to François Le Nalio who
spotted it and reported back. I actually had the typo in my original script,
this could have been another disaster. Like I did not have enough SSD failures
in the last three years :-)

