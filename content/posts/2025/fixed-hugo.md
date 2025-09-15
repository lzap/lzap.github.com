---
title: "Fixed Hugo alias noindex bug"
date: 2025-09-15T18:46:34+02:00
type: "post"
tags:
- linux
---

I was experiencing a weird behavior of Google treating my blog - specifically
with pages that had an alias. Turned out that Hugo generator, which I use for
my blog, use client side redirect for aliases:

```
---
type: "post"
aliases:
- /2013/07/hidden-gems-of-xterm.html
date: "2013-07-17T00:00:00Z"
tags:
- linux
- fedora
title: Hidden gems of xterm
---
```

Generates this alias page:

```
<!DOCTYPE html>
<html lang="en-us">
  <head>
    <title>http://localhost:1313/posts/2013/hidden-gems-of-xterm/</title>
    <link rel="canonical" href="http://localhost:1313/posts/2013/hidden-gems-of-xterm/">
    <meta name="robots" content="noindex">
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url=http://localhost:1313/posts/2013/hidden-gems-of-xterm/">
  </head>
</html>
```

The problem is the `noindex` meta which, for some reason, Google understands as
"do not index this redirect as well as the canonical page". Therefore, all Hugo
pages with an alias are excluded from Google index completely. Other search
engines behave differently, for example duckduckgogo is fine.

I reported this to Hugo community and we agreed this is not ideal solution:
https://discourse.gohugo.io/t/google-ignoring-pages-with-alias/55811

Therefore I created a patch and it was merged into the mainline Hugo branch:
https://github.com/gohugoio/hugo/pull/13951 and version 0.150 was just
released.

Now, if you suffered from this it is not easy to correct it. All my attempts to
force Google to revisit my site and fix this are unsuccessful to the degree
that I had to completely regenerate the whole site and the sitemap. This might
break my RSS feed, sorry about that:

```
for file in $(find content -name "*.md"); do if grep -q "aliases:" "$file"; then echo "" >> "$file"; fi; done
```

This needs last modification config like:

```
[frontmatter]
lastmod = [":git", ":fileModTime", ":default"]
```

Hope it helps.
