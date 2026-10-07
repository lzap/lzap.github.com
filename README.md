# Lukas Zapletal's blog

This repository contains the source for my blog, published at
<https://lukas.zapletalovi.com/>. I primarily use it as a personal notepad for
technology and Linux, so I can find useful details again years later.

All content is written by me. Since 2026, I have also used LLMs for assistance,
and I carefully review any material they help produce.

The site is built with [Hugo](https://gohugo.io/) and uses the Gokarna theme as
a Git submodule.

## Writing posts

Posts live in `content/posts/<year>/`. Run `./new_post` to create a post from
the Hugo archetype; it prompts for a filename and opens the new file in Vim.
The repository's `AGENTS.md` describes the tone and structure I use.

## Preview locally

Use Hugo Extended 0.152.0, the version used by the deployment workflow.
Initialize the theme submodule, then start the local server:

```sh
git submodule update --init --recursive
hugo server
```

Hugo serves the site at <http://localhost:1313/> by default.

## Build

Build the site into `public/` with:

```sh
hugo --gc --minify
```

The GitHub Actions workflow builds and publishes the site when changes are
pushed to `main`.
