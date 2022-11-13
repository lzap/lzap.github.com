---
type: "post"
aliases:
- /2012/11/writing-katello-upgrade-script.html
date: "2012-11-28T00:00:00Z"
tags:
- linux
- fedora
- katello
title: Writing katello upgrade script
---

With Katello, we deliver script upgrade-katello which enables users to upgrade
to the latest version interactively. Each upgrade is divided into several
steps. To see all of them, do:

    # ls /usr/share/katello/install/upgrade-scripts/ -1
    0050_start_qpid.sh
    0099_preallocate_mongo.sh
    0100_start_mongodb.sh
    0110_migrate_pulp.sh
    0200_start_httpd.sh
    0385_remove_hornet_files.sh
    0390_migrate_candlepin.sh
    0400_start_tomcat.sh
    0410_start_elasticsearch.sh
    0700_start_foreman.sh
    0710_migrate_katello.sh
    0711_reindex_elastic.sh
    0720_create_foreman_users.rb
    0800_start_katello.sh
    0805_start_katello_jobs.sh
    0900_katello_configure.sh

Each step is just an linux executable, most of them are simple bash scripts
with shebang and header which is parsed by the katello-upgrade script:

    # cat /usr/share/katello/install/upgrade-scripts/0390_migrate_candlepin.sh 
    #!/bin/bash

    #name: Migrate candlepin database
    #apply: katello headpin
    #run: always
    #description:
    #This step calls Candlepin cpdb utility to upgrade database schema
    #in postgresql database to the latest version.

    CANDLEPIN_HOME=${CANDLEPIN_HOME:-/usr/share/candlepin}

    pushd $CANDLEPIN_HOME >/dev/null
    ./cpdb --update 2>&1
    ret_code=$?
    popd >/dev/null

    exit $ret_code

Each script has a fancy name and description, which is presented to the user
either in interactive or non-interactive mode. Users can make decisions and
skip steps or completely suspend the upgrade process at any step if needed.

Katello can operate in two modes: "katello" and "headpin". The latter is
something we call katello-light - it does not have all features installed. For
upgrades, we do not want to execute particular steps. We set the apply header
only to "katello" for those.

The last but not least is run header field. It indicates if we want to run the
step every upgrade, or only once. Scripts that has been executed are recorded
in a text file and never executed again if they was marked as "once".

    # cat /var/lib/katello/upgrade-history 
    0099_preallocate_mongo.sh
    0720_create_foreman_users.rb

Our installer, katello-configure, is written in Puppet. The first idea was to
write the installation process in pure Puppet, but after experiences with bad
ordering with older Puppet versions in our installer, we have decided to take
this simple approach. In future, we can consider rewriting our upgrade steps
as Puppet classes. Until then, we need to execute Puppet at the and of the
upgrade to re-deploy all configuration files that has been changed. We do it
twice, because our classes sometimes do not fully apply during the first run.

    # cat /usr/share/katello/install/upgrade-scripts/0900_katello_configure.sh 
    #!/bin/bash

    #name: Reconfigure with katello-configure
    #apply: katello headpin
    #run: always
    #description:
    #This steps calls katello-configure twice to re-deploy configuration
    #and restart services. Configuration files are replaced from erb templates
    #which are distributed as part of katello-configure package. Make sure you
    #have backup of all configuration files if you made any changes in it.

    # do it twice - in rare cases configuration file changes needs two runs
    katello-configure -b --answer-file=/etc/katello/katello-configure.conf && \
      katello-configure -b --answer-file=/etc/katello/katello-configure.conf

Katello is easy to upgrade with this tool, it has nifty manual page and help
screen:

    # katello-upgrade -h
    Katello upgrade script
    Usage: /sbin/katello-upgrade [options]
        -a, --autostop                   Automatically stop services using "katello-service stop"
        -y, --assumeyes                  Work non-intearactively and proceed without asking
        -n, --dryrun                     Prints the upgrade steps without modifying anything
        -q, --quiet                      Do not print anything on the stdout/stderr (only log)
            --describe                   Only describe all the upgrade steps without modifying anything
            --trace                      Print exception stacktrace on error
            --noservicecheck             Do not check if all services are stopped (use with care)
            --norootcheck                Disable check for root (use with care)
            --deployment=DEPLOYMENT      Force deployment mode (use with care)
        -h, --help                       Show this short summary

Go ahead and upgrade your Katello instance today!

Links
-----

Katello: http://www.katello.org
Puppet: http://www.puppetlabs.com
