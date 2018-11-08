---
layout: page
title: For students
---
## Info for students

### "KMI/SLS: Správa linuxového serveru 2018" aka CentOS 7 course

Schedule: Every Thursday at [KMI PřF UPOL](http://www.inf.upol.cz/kontakt).
(Palacký University in Olomouc)

Time: 9:45 - 12:15
Room: 5.003 (Atrium, 5th floor)

* [Syllabus and contents with assignments](https://docs.google.com/a/zapletalovi.com/document/d/16LjrMkG-EQQFHRHGYxEp76B2Zlt4kSj5NRXhOGEpfQw/edit?usp=sharing)
* [Course credit status sheet](https://docs.google.com/spreadsheets/d/1PAm2V8XAtK6WMqjpa8H1qiOfKvy1feHjQilNyw-XX50/edit#gid=506263252)
* [Nufnuf](https://copr.fedorainfracloud.org/coprs/lzap/nufnuf/)
* [Asciinema](https://asciinema.org/)
* [Feedback form](https://goo.gl/forms/1xhgI2QpFEeUqRlJ3)

Requirements:

* A laptop with Linux or MacOS or Windows
* [VirtualBox 5.2.x](https://www.virtualbox.org/wiki/Downloads)
* [CentOS 7.5 DVD 1804](http://isoredirect.centos.org/centos/7/isos/x86_64/CentOS-7-x86_64-DVD-1804.iso)

Linux users:

* OpenSSH client is most likely already present, if not install package named `openssh-client`
* Install package named `asciinema` (via yum, dnf, apt-get, zypper etc)

MacOS users:

* OpenSSH is already present (command named `ssh`)
* Have [Brew](https://brew.sh/index_cs) installed
* Install asiinema via `brew install asciinema`

Windows users:

* Enable and install [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
  * Run the following in Administrator PowerShell: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux`
  * Restart the PC
  * Install "Debian/GNU Linux" environment from Microsoft Store
  * Choose UNIX username and a password
  * Install OpenSSH clients: `sudo apt-get install openssh-client`
  * Install asciinema: `sudo apt-get install asciinema`
  * (commands prompt for your UNIX account password)
* [Screencast with installation of WSL](https://www.youtube.com/watch?v=Z1behUQ9DBI)

Theses (ideas):

* [Statsd HDR histogram agent for PCP (Czech)](https://docs.google.com/document/d/1iPPRge3NsS48kxqSKsrEoKHd_mHMYGJdrfAxTAncaOA/edit?usp=sharing)

Warning, this page is cached aggressively with 8 hours expiration, you may
need to refresh it in your browser in order to get a recent change.
