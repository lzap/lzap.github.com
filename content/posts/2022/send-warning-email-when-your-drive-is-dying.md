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

	dnf install smartmontools ssmtp

Now, chances are you have a different MTA agent already installed, but my SMTP
server does not work with `esmtp` so I want to use `ssmtp` instead which is
much more rebust with better logging.

    alternatives --set mta /usr/sbin/sendmail.ssmtp

Configure the client, use `Debug` to further debug issues if needed:

```
root=postmaster
mailhub=smtp.example.com:587
RewriteDomain=example.com
Hostname=example.com
UseTLS=NO
UseSTARTTLS=YES
TLS_CA_File=/etc/pki/tls/certs/ca-bundle.crt
Debug=NO
AuthUser=lzap@example.com
AuthPass=xxxxxxxxxxxx
AuthMethod=PLAIN
```

Send a test email:

```
echo -e "Subject: Test\n\nHi!" | sendmail -v lzap@example.com
```

From address must match in order to pass MTA anti-spam filters, you can do this
in `/etc/ssmtp/revaliases`:

	root:lzap@example.com

A dirty shell script will do, note that smartctl utility returns a bit mask so
finding if a drive is healthy is a bit tricky. Luckily, the manpage contains an
example:

	cat /etc/cron.weekly/smart

Something like:

```
for DRIVE in sda sdb sdc sdd; do
  smartctl -H /dev/$DRIVE &>/dev/null
  dying=$(($? & 8))
  if [[ $dying -ne 0 ]]; then
    echo "Subject: SMART problem $DRIVE on $(hostname)" | sendmail -v me@example.com
  fi
done
```

It's dirty, but it should work. Here is slightly more elaborated version:

```
#!/bin/bash
RECIPIENT="lzap@example.com"
HOSTNAME=$(hostname)
SMARTCTL="/usr/sbin/smartctl"
SENDMAIL="/usr/sbin/sendmail"

DRIVES=$(lsblk -dno NAME | grep -E 'sd|nvme')
for DRIVE in $DRIVES; do
    DEVICE="/dev/$DRIVE"
    DRIVER_FLAG="-d auto"

    if [[ "$HOSTNAME" == "yuki.internal" && "$DEVICE" == "/dev/sda" ]]; then
        DRIVER_FLAG="-d sntjmicron"
    fi

    # Run SMART check (Health -H and All Attributes -A)
    OUTPUT=$($SMARTCTL $DRIVER_FLAG -H -A "$DEVICE" 2>&1)
    EXIT_CODE=$?

    # Bit 0: Command line did not parse
    # Bit 1: Device could not be opened
    # Bit 2: SMART command failed
    # Bit 3: DISK FAILING (Critical) [Value 8]
    # Bit 4: Attributes below threshold (Pre-fail) [Value 16]
    # Bit 5: SMART status OK, but self-test log has errors [Value 32]
    # Bit 6: SMART status OK, but error log has errors [Value 64]

    # We want to alert if bits 3, 4, 5, or 6 are set (Sum = 120)
    if (( EXIT_CODE & 120 )); then

        STATUS_MSG="SMART ALERT"
        (( EXIT_CODE & 8 ))  && STATUS_MSG="CRITICAL FAILURE"
        (( EXIT_CODE & 16 )) && STATUS_MSG="PRE-FAIL WARNING"
        (( EXIT_CODE & 96 )) && STATUS_MSG="LOG ERRORS DETECTED"

        (
            echo "Subject: [$STATUS_MSG] $DEVICE on $HOSTNAME"
            echo "To: $RECIPIENT"
            echo "MIME-Version: 1.0"
            echo "Content-Type: text/plain; charset=UTF-8"
            echo ""
            echo "Attention: The health monitor detected issues with $DEVICE."
            echo ""
            echo "Detected Bits:"
            (( EXIT_CODE & 8 ))  && echo " - [BIT 3] DISK IS FAILING"
            (( EXIT_CODE & 16 )) && echo " - [BIT 4] PRE-FAIL ATTRIBUTES BELOW THRESHOLD"
            (( EXIT_CODE & 32 )) && echo " - [BIT 5] SELF-TEST LOG CONTAINS ERRORS"
            (( EXIT_CODE & 64 )) && echo " - [BIT 6] ERROR LOG CONTAINS ERRORS"
            echo ""
            echo "--- FULL SMARTCTL OUTPUT ---"
            echo "$OUTPUT"
        ) | $SENDMAIL -t

        echo "Disk Alert for $DEVICE (Exit Code $EXIT_CODE). Email sent." | logger -t disk-monitor
    fi
done
```

Update 2025: I had a typo in the script, special thanks to François Le Nalio who
spotted it and reported back. I actually had the typo in my original script,
this could have been another disaster. Like I did not have enough SSD failures
in the last three years :-)

Update 2026: Added alternatives and more elaborated script.
