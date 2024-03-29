---
type: "post"
aliases:
- /2013/04/managing-many-servers-with-foreman.html
date: "2013-04-10T00:00:00Z"
tags:
- linux
- fedora
title: Managing many servers with Foreman
---

Recently I joined the Foreman team - an open-source provisioning and
configuration management software written in Ruby on Rails. If you manage more
than one server and you need to automate server installations and
configuration, maybe Foreman is good fit for you. If you use Puppet for
configuration deployment, then Foreman is great fit for sure.

In this blog post, I want to share how to do a small installation
everythin-on-one-box for evaluating Foreman. This kind of setup is great for
evaluating Foreman or for development or testing. It is definitely not
recommended to run production setup configured according to this blog post!
I will repeat this several times, *do not* install Foreman for serious use
following this page.

*Warning*: I used this setup to _learn_ how Foreman works, how Foreman
Smart-Proxy works and how everything fit together. Foreman does have
puppet-based installer which configures all services out-of-box (except
libvirt of course). It is highly recommended to use it instead of this manual
installation. If you are going to evaluate Foreman, it is more recommended to
do this:

 * Get a RHEL 6.4+ box with some memory and space and hypervisor capabilities
 * Install libvirt and create a virtual NAT network without DHCP enabled (see
 bellow how to do that)
 * Install Foreman and Foreman-Proxy using our installers
 * Reconfigure ISC DHCP to listen only on the virtual network (see bellow)
 * Register the proxy and the libvirt in the Foreman using the UI
 * Play with Foreman

Ok if you decided *not* to stop reading here, you want to do the "hard" setup.
And that is fine, this is the purpose of my blog post.

The idea is simple - I will have one hardware box running RHEL6 where I want
to install KVM/libvirt hypervisor with a virtual network. In this network, I
will run DHCP, DNS and TFTP services for automated installations of RHEL6,
CentOS6 or Fedora. Note that Foreman does support other distributions like
SUSE, Debian, Ubuntu or even Solaris OS, but for simplicity I will focus only
on RHEL-based systems.

Also, I will not use libvirt DHCP server since I wanted to try out full
integration with ISC DHCP service. Ready, steady. Let's do this!

First of all, get a decent hardware box with at least 4 GB RAM and a CPU with
native virtualization support, install RHEL6 (I am using 6.4) and install
necessary Virtualization yum group (or just libvirt if you want).

For the sake of simplicity we will configure libvirt without any
authentication. This is dangerous, but for our testing purposes it will work.
On the libvirt server make the following changes:

    # cat /etc/libvirt/libvirtd.conf
    listen_tls = 0
    listen_tcp = 1
    auth_tcp = "none"

    # grep listen /etc/sysconfig/libvirtd
    LIBVIRTD_ARGS="--listen"

Restart the guy.

    # service libvirtd restart

You should be able to reach this instance via TCP. Note the above setting is
perhaps not necessary for the whole setup, but I just did this for my
convenience. Test it out:

    # virsh -c 'qemu+tcp://libvirt:16509/system' list

Now, we want to create a *virtual network* where we will run our services. I
want to stress out using virtual network instead physical one, because I can
imagine you are already running a DHCP server there and starting our own one
could cause some pains :-)

To create it, the easiest method is to use virt-manager, connect to your
hypervisor and using Details - Virtual Network - Add add new one with a name
"virtual". Do *NOT* set DHCP server there and leave the default network
configuration. Also put NAT option in there. It will likely have device virbr1
since virbr0 is usually taken by network "default". The configuration should
look like this (note the network 192.168.100.0/24 I use here):

    # cat /etc/libvirt/qemu/networks/virtual.xml 
    <!--
    WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE 
    OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
    virsh net-edit virtual or other application using the libvirt API.
    -->
    <network>
    <name>virtual</name>
    <uuid>f00c9416-0b28-3cbf-4144-b9b95bd3c651</uuid>
    <forward mode='nat'/>
    <bridge name='virbr1' stp='on' delay='0' />
    <mac address='52:54:00:20:1F:20'/>
    <ip address='192.168.100.1' netmask='255.255.255.0'>
    </ip>
    </network>

You should be also able to create this via virsh, or even manually (but you
need to stop libvirt, edit the file and then start it). Also create the
autostart symlink if you are doing this manually. The UI is highly recommended
for this tho.

Note you could use the "default" network which has the very same configuration
(but usually with 192.168.122.0/24 network), but with DHCP. I tend to prefer
creating very own network not to confuse others which would like to use
"default" one.

Now, the following step is really not necessary, because there will not be any
TFTP NAT traversal, but we can load our iptables modules since it does not
hurt at all (actually I just wanted to keep these lines somewhere not to
forget about these :-)

    # cat /etc/sysconfig/modules/foreman.modules
    #!/bin/sh
    modprobe nf_nat_tftp
    modprobe nf_conntrack_tftp
    exit 0

Make sure it has executable flag and load these modules by executing this
file.

Let's install ISC DHCP software, ISC Bind (DNS) software and BSD TFTP.

    # yum -y install dhcp bind tftp-server syslinux

Before we start configuring DHCP, we need to generate security token:

    # dnssec-keygen -r /dev/urandom -a HMAC-MD5 -b 512 -n HOST omapi_key
    # cat Komapi_key.+*.private |grep ^Key|cut -d ' ' -f2-

Copy the output and paste it bellow to the dhcpd.conf.

Note: If you get an package conflict error in Fedora 16 or RHEL 6.0, do yum
update dhclient and try again then. Now configure dhcpd and make it listen on
the correct interface (virbr1 in our case). This is *very* important - do NOT
run DHCP daemon on your physical device like eth0 :-)

    # cat /etc/dhcp/dhcpd.conf
    default-lease-time 604800;
    max-lease-time 2592000;
    log-facility local7;

    subnet 192.168.100.0 netmask 255.255.255.0 {
        range 192.168.100.10 192.168.100.200;
        option routers 192.168.100.1;
        option subnet-mask 255.255.255.0;
        option domain-search "virtual.lan";
        option domain-name "virtual.lan";
        option domain-name-servers 8.8.8.8;
    }

    omapi-port 7911;
    key omapi_key {
        algorithm HMAC-MD5;
        secret "0pD4fT+...";
    };
    omapi-key omapi_key;

As you can see our network will have "virtual.lan" domain. Also change your
DNS servers from Google public (8.8.x.x) to yours. This network has NAT, so it
will use your physical interface.

Again, do not forget to set the correct listening interface!

    # cat /etc/sysconfig/dhcpd
    DHCPDARGS=" virbr1"

    # service dhcpd restart
    # chkconfig dhcpd on

If you do not want to break your current LAN setup, double check in the
/var/log/messages dhcpd is listening on the correct interface! I know I am
repeating myself, I promise - this is the last time.

Let's configure DNS, bind is already installed so we can edit it's
configuration:

    # cat /etc/named.conf
    include "/etc/rndc.key";

    controls  {
        inet 127.0.0.1 port 953 allow { 127.0.0.1; } keys { "foreman"; };
    };

    options  {
        directory "/var/named";
        forwarders { 8.8.8.8; 8.8.4.4; };
    };

    include "/etc/named.rfc1912.zones";

    zone "100.168.192.in-addr.arpa" IN {
        type master;
        file "dynamic/100.168.192-rev";
        update-policy {
            grant "foreman" zonesub ANY;
        };
    };

    zone "virtual.lan" IN {
        type master;
        file "dynamic/virtual.lan";
        update-policy {
            grant "foreman" zonesub ANY;
        };
    };

There is a key section in the rndc.key file - it is good idea to keep it
separate:

    # cat /etc/rndc.key
    key "foreman" {
        algorithm hmac-md5;
        secret "WqEdq...Kk2vWhcw==";
    };

As you can see, it is pretty much standard named.conf configuration with acl
virtual-lan added, zone "virtual.lan" and key section which was generated by
the following command:

    # ddns-confgen -k foreman -a hmac-md5

Make sure the DNS does listen on the virtual lan only. I am not configuring
IPv6 at all. Now let's create a simple zone file:

    # cat /var/named/dynamic/virtual.lan
    $ORIGIN .
    $TTL 86400  ; 1 day
    virtual.lan     IN SOA  virtual.lan. lzap+pub.redhat.com. (
                    2013041903 ; serial
                    28800      ; refresh (8 hours)
                    7200       ; retry (2 hours)
                    864000     ; expire (1 week 3 days)
                    86400      ; minimum (1 day)
                    )
                NS  ns.virtual.lan.
                A   192.168.100.1
                MX  10 mail.virtual.lan.
    $ORIGIN virtual.lan.
    foreman         A   192.168.100.1
    mail            A   192.168.100.1
    ns              A   192.168.100.1
    tftp            A   192.168.100.1

And the reverse file:

    # cat /var/named/dynamic/100.168.192-rev
    $ORIGIN .
    $TTL 86400  ; 1 day
    100.168.192.in-addr.arpa IN SOA virtual.lan. lzap+pub.redhat.com. (
                    2013041903 ; serial
                    28800      ; refresh (8 hours)
                    7200       ; retry (2 hours)
                    864000     ; expire (1 week 3 days)
                    86400      ; minimum (1 day)
                    )
                NS  ns.virtual.lan.
    $ORIGIN 100.168.192.in-addr.arpa.
    1           PTR foreman.virtual.lan.

Start the thing!

    # service named start
    # chkconfig named on

Now you should be able to connect to the management interface. To test this
issue the following command:

    # echo -e "update add aaa.virtual.lan 3600 IN A 192.168.100.99\nsend\n" |\
        nsupdate -k /etc/rndc.key

Note you will not see the entry in the zone file, but in the transfer jnl
binary file. To move all the entries from the binary file to the zone text
file, use the following commands:

    # rndc freeze virtual.lan
    # rndc freeze 100.168.192.in-addr.arpa
   
Now you can remove it and restart named.

Warning: Since I will install Foreman and Smart Proxy as root (NOT
recommended), I do not need to care about permissions. You should make sure
that the key file is readable by Smart Proxy user.

Configuration of TFTP will be pretty straightforward, the software is already
installed and we just need to do few steps. Create a directory structure for
files:

    # mkdir -p /var/lib/tftpboot/pxelinux.cfg

Now, copy essential files from syslinux package to our TFTP root directory.

    # cp /usr/share/syslinux/{pxelinux.0,menu.c32,chain.c32} \
        /var/lib/tftpboot/

If you are thinking about "service tftp start" command, forget about it.
Muhahahahahaaaa! The TFTP service is started via xinetd, so we need to start
it. Remove disabled line from the tftp xinetd file:

    # grep disable /etc/xinetd.d/tftp
    disable         = yes

And start it.

    # service xinetd start
    # chkconfig xinetd on

You should be able to download a file via TFTP now:

    # cd /tmp
    # tftp 192.168.100.1
    tftp> get pxelinux.0
    tftp> exit
    # rm -i pxelinux.0

We are not there yet, but quite close. We want to install smart proxy at this
point. Smart proxy is a very small daemon that Foreman talks to via HTTPS
REST. Smart proxy is able to interact with all the services like DHCP, DNS,
TFTP and Puppet/PuppetCA.

For both Smart proxy and Foreman, I will use rbenv installation, because both
projects need recent ruby libraries which are not avaiable in RHEL6 yet. It is
not recommended to use rbenv for production setups, but for our evaluation
purposes it should work just fine and it is very quick.

I will install everything in /root (yeah) and will run everything under root
(on my test/development servers I only have the root user). Because rbenv script
will compile it's own Ruby, we need some devel libraries.

    # yum -y install git libvirt-devel mysql-devel pg-devel openssl-devel \
        libxml2-devel sqlite-devel libxslt-devel zlib-devel readline-devel 

We are following rbenv installation instructions now. Let's install rbenv and
Ruby 1.9:

    # cd /root
    # git clone git://github.com/sstephenson/rbenv.git ~/.rbenv
    # echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bash_profile
    # echo 'eval "$(rbenv init -)"' >> ~/.bash_profile
    # exec $SHELL -l
    # git clone git://github.com/sstephenson/ruby-build.git \
        ~/.rbenv/plugins/ruby-build
    # rbenv install 1.9.3-p327

It will take a while to finish. Now, let's move on to smart-proxy. We will
configure to run it in the *foreground* instead of deamonizing. Good for
testing.

    # git clone git://github.com/theforeman/smart-proxy.git
    # cd smart-proxy
    # cp config/settings.yml.example config/settings.yml

Configure Smart Proxy to use all the services we have just configured.

    # grep '^:' config/settings.yml
    :daemon: false
    :daemon_pid: /var/run/foreman-proxy/foreman-proxy.pid
    :port: 8443
    :tftp: true
    :tftproot: /var/lib/tftpboot
    :tftp_servername: 192.168.100.1
    :dns: true
    :dns_key: /etc/rndc.key
    :dns_server: 192.168.100.1
    :dhcp: true
    :dhcp_vendor: isc
    :dhcp_config: /etc/dhcp/dhcpd.conf
    :dhcp_leases: /var/lib/dhcpd/dhcpd.leases
    :dhcp_key_name: omapi_key
    :dhcp_key_secret: 0pD4fT+hJ...==
    :puppetca: true
    :ssldir: /etc/puppet/ssl
    :puppetdir: /etc/puppet
    :puppet: true
    :puppet_conf: /etc/puppet/puppet.conf
    :bmc: false
    :log_file: logs/development.log
    :log_level: WARN

Note I am not setting Proxy up for SSL, again, this is NOT recommended for
production setups. For fast readers - warning - this is testing installation.

Since Puppet in RHEL/EPEL is pretty outdated, we will run latest Puppet from
rubygems.org directly. Add this line to the Gemfile:

    # grep puppet Gemfile
    gem 'puppet'

Start the proxy:

    # bundle install
    # bundle exec bin/smart-proxy

We need to configure Puppet first. Although we will run the latest puppet from
rubygems.org, we configured standard paths.

    # mkdir /etc/puppet
    # puppet master --genconfig > /etc/puppet/puppet.conf

You can review the configuration, I made just three changes there. I will run
puppet master daemon as root, which is *not* recommended for production
setups.

    # grep -E '^\s*(modulepath|user|group)' /etc/puppet/puppet.conf
    user = root
    group = root
    modulepath = /etc/puppet/modules/$environment

Now you can start puppet master:

    # puppet master --no-daemonize --verbose

Finally, you can follow Foreman installation:

    # cd /root
    # git clone https://github.com/theforeman/foreman.git -b develop
    # cd foreman
    # bundle install
    # cp config/settings.yaml.example config/settings.yaml
    # cp config/database.yml.example config/database.yml

I will keep the default database setting on sqlite3, but if you intend to
evaluate Foreman with more than one user, I highly recommend to configure
postgresql database (more info in the Foreman manual about that). Settings are
standard:

    # grep '^:' config/settings.yaml
    :unattended: true
    :login: true
    :require_ssl: false
    :locations_enabled: true
    :organizations_enabled: true
    :support_jsonp: false

Migrate db and start the thing! It is recommended to run in the production mode
which is much more faster.

    # RAILS_ENV=production bundle exec rake db:migrate assets:precompile locale:pack
    # RAILS_ENV=production bundle exec rails server

We are almost there, go to http://localhost:3000 and visit main settings page.
Review it and setup root password for newly created hosts and also foreman_url
to foreman.virtual.lan.

Configure Smart Proxy first, you whould see all its features there.

Now you can create architecture, OS, associate templates and provision hosts and 
do stuff. More about that maybe later.
