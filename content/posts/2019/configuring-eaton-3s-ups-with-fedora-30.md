---
type: "post"
aliases:
- /2019/06/configuring-eaton-3s-ups-with-fedora-30.html
date: "2019-06-07T00:00:00Z"
tags:
- linux
- fedora
title: Configuring Eaton 3S UPS with Fedora 30
---

First off, make sure your UPS is connected. On my system, I had to use a
different USB port as it was disconnecting regularly for some reason - probably
USB power issues which is funny since this is a power device:

    # dmesg
    # lsusb

Install and configure nut software:

    # dnf -y install nut

    # grep ^MODE /etc/ups/nut.conf
    MODE=standalone

    # grep -v '^#' /etc/ups/ups.conf
    [eaton3s]
    driver=usbhid-ups
    port=auto

    # grep -v '^#' /etc/ups/upsmon.conf | egrep -v '^$'
    MONITOR eaton3s@localhost 1 monuser pass master
    MINSUPPLIES 1
    SHUTDOWNCMD "/sbin/shutdown -h +0"
    POLLFREQ 5
    POLLFREQALERT 5
    HOSTSYNC 15
    DEADTIME 15
    POWERDOWNFLAG /etc/killpower
    NOTIFYFLAG ONBATT SYSLOG+WALL+EXEC
    NOTIFYFLAG ONLINE SYSLOG+WALL+EXEC
    NOTIFYCMD "/etc/ups/shutdown-script"
    RBWARNTIME 43200
    NOCOMMWARNTIME 300
    FINALDELAY 5

    # grep -v '^#' /etc/ups/upsd.users | egrep -v '^$'
    [monuser]
    password=pass
    upsmon master

At this point, UPS should respond via USB which you can check with:

    # usbhid-ups -DDD -a eaton3s

Make sure to replace "pass" with some password in both files. Now, the power
outage script is where you can implement what you want. In my case, I want to
see desktop notification every 10 seconds and after 3 minutes I want my system
to poweroff:

    # cat /etc/ups/shutdown-script
    #!/bin/bash
    PATH=/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/sbin:/usr/local/bin

    trap "exit 0" SIGTERM

    notify() {
            notify-send -u $2 "$0: $1"
    }

    if [ "$NOTIFYTYPE" = "ONLINE" ]; then
            notify "power restored" critical
            killall -s SIGTERM `basename $0`
    fi

    if [ "$NOTIFYTYPE" = "ONBATT" ]; then
            notify "3 minutes until shutdown" critical
            let "n = 18"
            while [ $n -ne 0 ]
            do
                    sleep 10
                    let "n--"
                    notify "$(( $n * 10 )) seconds until to shutdown" low
            done
            notify "commencing shutdown" critical
            upsmon -c fsd
    fi

On server systems, you want to replace notify-send with probably something like
`echo $0: $1 | wall` to notify console users. Make sure the script is
executable:

    # chmod +x /etc/ups/shutdown-script

Start the services, note that one of the three services (nut-driver) is started
automatically as a dependency so do not enable it (systemd would complain
anyway):

    # systemctl start nut-monitor nut-server
    # systemctl enable nut-driver nut-monitor nut-server
    # systemctl status nut-driver nut-monitor nut-server

To diplay battery remaining capacity and other details you can use this command line tool:

    # upsc eaton3s
    Init SSL without certificate database
    battery.charge: 96
    battery.charge.low: 20
    battery.runtime: 672
    battery.type: PbAc
    device.mfr: EATON
    device.model: Eaton 3S 550
    device.serial: 000000000
    device.type: ups
    driver.name: usbhid-ups
    driver.parameter.pollfreq: 30
    driver.parameter.pollinterval: 2
    driver.parameter.port: auto
    driver.parameter.synchronous: no
    driver.version: 2.7.4
    driver.version.data: MGE HID 1.39
    driver.version.internal: 0.41
    input.transfer.high: 264
    input.transfer.low: 184
    outlet.1.desc: PowerShare Outlet 1
    outlet.1.id: 2
    outlet.1.status: on
    outlet.1.switchable: yes
    outlet.2.desc: PowerShare Outlet 2
    outlet.2.id: 3
    outlet.2.status: off
    outlet.2.switchable: yes
    outlet.desc: Main Outlet
    outlet.id: 1
    outlet.switchable: no
    output.frequency.nominal: 50
    output.voltage: 230.0
    output.voltage.nominal: 230
    ups.beeper.status: enabled
    ups.delay.shutdown: 20
    ups.delay.start: 30
    ups.firmware: 02
    ups.load: 30
    ups.mfr: EATON
    ups.model: Eaton 3S 550
    ups.power.nominal: 550
    ups.productid: ffff
    ups.serial: 000000000
    ups.status: OL
    ups.timer.shutdown: 0
    ups.timer.start: 0
    ups.vendorid: 0463

Interesting parameters which are worth putting onto my i3status bar are
probably battery.* and ups.load. Remember to perform a test! A good one is
checking if this command works fine:

    # upsmon -c fsd

And then full "integration" test - exit all programs and then pull the wire off the wall and wait :-)

Good luck!
