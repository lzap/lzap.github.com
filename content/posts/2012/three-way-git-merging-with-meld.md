---
type: "post"
aliases:
- /2012/09/three-way-git-merging-with-meld.html
date: "2012-09-17T00:00:00Z"
tags:
- linux
- fedora
title: Three way git merging with meld
---

This article is updated version of [Three-way git merging and meld][1] and it
was updated once again in 2015 (thanks to Eric Drechsel).

Although I am vim-lover, when it comes to git merging I use excellent tool
called Meld instead of vim. It's a GTK-based application written in Python and
it has very nice capabilities of showing diffs. Particularly, I like how Meld
shows changes on the same lines (highlighing portions of them), it's editable
text pane with source highlighting and ability to visually merge conflicts
using arrow icons.

I was not considering Meld as a three-way merging tool, until Tomek Bury
pointed out that Meld supports three-way merging. This feature is not
advertised on the main page and even in the program itself (help command line
output page). More about this later.

Basic idea of three-way merging is taking third merging source into the loop,
so instead traditional LOCAL and REMOTE (or MINE and THEIRS if you like) there
is additional one: BASE. That's the parent for both commits in git. Still
don't see the drawback?

For manual three-way merging you need four panes, because you want to see
LOCAL, REMOTE, BASE and also the file you will be actually merging. In the git
case, that would be:

    test.txt
    test.txt.LOCAL
    test.txt.REMOTE
    test.txt.BASE

Typical three-way merging tool shows differences between LOCAL, BASE and
REMOTE on the top while offering one additional text pane on the bottom. For
example, vimdiff can do this four-pane merging with a little tuning (you need
to move merged buffer window to the bottom of the screen). Another great
example of this approach is Perforce (p4merge).

Please note workflow is a bit different than in three-pane merging tools - you
usually don't touch the file in the middle (BASE) and edit the bottom (merged)
file manually. At least I don't know any tool that would offer you visual
merging of blocks from LOCAL, BASE or REMOTE panes, except vim getdiff and
putdiff capabilities. But that is not visual.

If you start three-pane merging tool (e.g. meld, kdiff3 and most of the
others), you usually see LOCAL, merging file and REMOTE. What you don't see is
BASE file, how it looked like before it was changed in any way.

Fortunately Meld supports tabs, so you can still see something. I configured
my git to start three tabs in Meld. On the first one I see differences between
BASE and LOCAL. On the second one I see BASE and REMOTE. And the third one is
usual: LOCAL, merged file, REMOTE. The configuration is pretty easy:

    [merge]
    tool = mymeld
    [mergetool "mymeld"]
    cmd = meld --diff $BASE $LOCAL --diff $BASE $REMOTE --diff $LOCAL $MERGED $REMOTE

This is what I call *traditional two-way merge with tabs*. Now, since I
already noted Meld supports three-way merging, there is another option.
When "diff3" git conflict style is set, Meld prints "(??)" on the line showing
the content from BASE. In this mode, LOCAL and REMOTE files are read-only
which is also handy. Therefore it is possible to configure git to use this
*three-way merging*:

    [merge]
    tool = mymeld
    conflictstyle = diff3
    [mergetool "mymeld"]
    cmd = meld $LOCAL $BASE $REMOTE -o $MERGED --auto-merge

Note `--auto-merge` option was added in Meld 1.7.0 and it merges all
non-conflicting code after start automatically.

You can also use combination of both approaches, because sometimes it's better
to see side-by-side comparison. I call the final setup *three-way merge with
tabs*.

    [merge]
    tool = mymeld
    conflictstyle = diff3
    [mergetool "mymeld"]
    cmd = meld $LOCAL $BASE $REMOTE -o $MERGED --diff $BASE $LOCAL --diff $BASE $REMOTE --auto-merge

This way you can still use Meld with three windows, but it will read lines
from the BASE file showing you history. And you can still use tabs to do
side-by-side comparison.

Now how the third approach look like when you start Meld. The first tab shows
the changes in the branch I am merging into (e.g. "master"):

![Meld](/assets/img/posts/2012-09-17-three-way-git-merging-with-meld/meld1.png)

The second is similar, shows changes from the branch I am merging (e.g.
"feature" branch):

![Meld](/assets/img/posts/2012-09-17-three-way-git-merging-with-meld/meld2.png)

And the third (opened by default) has traditional three-pane layout where I do
the work.

![Meld](/assets/img/posts/2012-09-17-three-way-git-merging-with-meld/meld3.png)

I sometimes use little bit different configuration when I want to see plain
git marks in the file that is being merged (the middle file). I have a
separate merge tool configured and use it explicitly when I want. In rare
cases, it can be faster to manually edit the file in the editor visualizing
the changes via meld.

    [merge]
    tool = mymeld_plain
    conflictstyle = diff3
    [mergetool "mymeld_plain"]
    cmd = meld --diff $LOCAL $MERGED $REMOTE --diff $BASE $LOCAL --diff $BASE $REMOTE

That's all for today.

[1]: http://lukas.zapletalovi.com/2012/06/three-way-git-merging-and-meld.html
