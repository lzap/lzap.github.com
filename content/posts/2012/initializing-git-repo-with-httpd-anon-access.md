---
type: "post"
aliases:
- /2012/07/initializing-git-repo-with-httpd-anon-access.html
date: "2012-07-26T00:00:00Z"
tags:
- linux
- rhel
- fedora
- git
title: Initializing git repo with httpd anon access
---

Another tutorial how to setup git repository with ssh read-write access and
anonymous httpd access. But this time, I want to focus on getting it working
on RHEL6 (Fedora should work too). There's one trick I want to record on my
blog ;-)

Fist of all, let's configure httpd to serve user directories. My first thought
was to create a file in /etc/httpd/conf.d, but this is not working since
UserDir option is *explicitely* turned off. We need to edit

    server# vim /etc/httpd/conf/httpd.conf

Search for UserDir string, somewhere on the line 370 you need to commend and
(un)comment two UserDir lines *and* uncomment the very next section with
access to /home/\*/public_html directory.

    <IfModule mod_userdir.c>
        #
        # UserDir is disabled by default since it can confirm the presence
        # of a username on the system (depending on home directory
        # permissions).
        #
        #UserDir disabled

        #
        # To enable requests to /~user/ to serve the user's public_html
        # directory, remove the "UserDir disabled" line above, and uncomment
        # the following line instead:
        # 
        UserDir public_html
    </IfModule>

    #
    # Control access to UserDir directories.  The following is an example
    # for a site where these directories are restricted to read-only.
    #
    <Directory /home/*/public_html>
        AllowOverride FileInfo AuthConfig Limit
        Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec
        <Limit GET POST OPTIONS>
            Order allow,deny
            Allow from all
        </Limit>
        <LimitExcept GET POST OPTIONS>
            Order deny,allow
            Deny from all
        </LimitExcept>
    </Directory>

Now the trick. Create public_html directory in your home folder and check
permissions are correct. On RHEL6, home folder has permissions of 700 by
default. If you don't change this, Apache will be giving you 403.

    server# mkdir /home/lzap/public_html
    server# chmod 755 /home/lzap/public_html
    server# chmod 711 /home/lzap

We are done. Now, restart Apache with

    server# service httpd restart

Creating empty git repository is a piece of cake. But we also want to make
sure it always has correct permissions. There is a git hook for that. Do this:

    server# cd /home/lzap/public_html
    server# mkdir project.git
    server# cd project.git
    server# git init --bare
    server# mv hooks/post-update.sample hooks/post-update
    server# chmod a+x hooks/post-update
    server# hooks/post-update

I usually create *git* symlink in the home folder just to make some paths
shorter.

    server# cd
    server# ln -s public_html/ git

That's it. We are done. To access your repository with read-write access just
do this

    client# git clone git+ssh://lzap@server/home/lzap/git/project.git

To get anonymous access via "dumb" http protocol use

    client# git clone http://lzap@server/git/project.git

Okay. Now I can copy&paste from here next time.
