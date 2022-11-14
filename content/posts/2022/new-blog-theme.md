---
title: "New Blog Theme"
date: 2022-11-14T22:46:26+01:00
type: "post"
tags:
- blog
---

I have deployed a new blog theme named gokarna and my blog was converted from
Jekyll to Hugo. It is still hosted on github.com but now instead of GitHub
Pages, new (Beta) GitHub Action for Pages is used. I still use Cloudflare for
DNS, caching and HTTPS termination. Please give it a visit and report bugs.

The new theme is way better than my previous one, it is clean and works on
mobile without hiccups. The theme supports light and dark mode and
automatically detect your preferred OS/browser theme, or you can switch it
using the sun/moon icon in the top-right corner and your choice is stored in
the browser local store.

I did a huge cleanup on the social front, gone are some weird links like
Google+ and say hello to Mastodon icon. I also added "Buy Me a Coffee" since it
was used in the original template.

The RSS feed was unchanged (`/feed.xml`) and hopefully it works fine and you
can read this post via your RSS reader. You might experience some older
articles to re-appear, but hopefully you will only see the last 20. Let me know
if it works or does not via Mastodon!

This was all-weekend task, but luckily Hugo's built in Jekyll importer worked
like a charm. A small Python script and few shell scripts ironed out the
details. There should be redirects from old links too. Hugo is great. Cheers!
