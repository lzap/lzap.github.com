---
type: "post"
aliases:
- /2013/01/faster-backporting-with-git-ssh-and-patch.html
date: "2013-01-23T00:00:00Z"
tags:
- linux
- fedora
- git
title: Faster backporting with git, ssh and patch
---

If you wort at Red Hat, be prepared to backport stuff. This is why customers
pay us - they want stable releases with fixed bugs. So while working on new
features upstream, we also fix bugs in released products.

_Interested in working at Red Hat? Contact me! ;-)_

More info at: http://jobs.redhat.com

The way we work in our team is to fix everything in the upstream project first
(for me this is Katello - www.katello.org) and then to cherry pick fixes
into internal branch which we build our product from (for me this is
CloudForms System Engine). Except security bugs which are still under embargo
of course.

_CloudForms System Engine is component of CloudForms solution by Red Hat for 
monitoring and updating running systems across physical, virtual, and cloud
environments. It ensures compliance of content and configurations, as well as
Red Hat entitlements. CloudForms System Engine works with CloudForms Cloud
Engine by supplying content required to build images and deploy them across
the cloud._

More info at: http://www.redhat.com/products/cloud-computing/cloudforms/

For bugs which can be reproduced upstream first this is pretty
straightforward. But there can be troubles when working on bugs which can be
only reproduced on the product.

At the first stage, I usually edit files directly on my testing instance where
I reproduced it. Then I need to write a patch for upstream and backport it.
And this is the time I often need to cherry pick into internal, rebuild
product, install it, restart. Pretty time consuming.

So this is what I sometimes use - maybe you find it useful. When I have the
patch ready and tested with upstream in my git (staged for commit), I can
remotely patch my instance using this command:

    katello_git# git diff | ssh repro.lan "patch -p2 -d /usr/share/katello"

If the patch applies fine, great. If not, you usually need to correct some
blocks (patch creates rejected blocks as .rej files by default), restart and
test the patch.

If I need to re-patch, I usually do this:

    repro.lan# rpm -qV katello
    S.5....T.    /usr/share/katello/app/controllers/api/api_controller.rb

    repro.lan# yum reinstall katello
    repro.lan# rpm -qV katello

Now the product is ready to be patched again. I was using contra-patching, but
it does not work well when you merge changes manually.

You can use both git diff or git am (if you have already commited something).
Depends on your git workflow.

Maybe this can be helpful for you somehow. ;-)
