---
type: "post"
aliases:
- /2021/11/a-sane-vim-configuration-for-fedora.html
date: "2021-11-11T00:00:00Z"
tags:
- linux
- fedora
title: A sane vim configuration for Fedora
---

When you start Vim with the `--clean` option, it shows up in "vanilla" mode. No
plugins, no configuration, just back to the roots. I have collected a ton of
configuration statements over the years some of them dating from MS-DOS or
Windows 3.1. Here is the deal: I am going to start from scratch to find a good
starting-point configuration with just plugins which are available in Fedora 35.
Will I survive a week of coding? Let's find out!

Let's set the rules: Minimum possible configuration statements and only plugins
which ship with Fedora 35+. By the way, if you are not Fedora user, continue
reading. You can always install these plugins from your OS package manager,
manually or via a Vim plugin manager.

Before we start, there's the elephant in the room: Vim or Neovim (fork of Vim)
question. Well, this is up to you, everything that is in this post should work
for both, however, I only tested with Vim. All the skill will come handy when
you logon to a server where only vi is available. It can be either an old UNIX
system, Linux server with minimum software installed for better security, an
interative shell in a container or an embedded system where space is precious.

Without further ado, here is what I distilled to the absolute bare minimum to
be effective with Vim for coding:

	# dnf install --allowerasing vim-default-editor \
		vim-enhanced \
		vim-ctrlp \
		vim-airline \
		vim-trailing-whitespace \
		vim-fugitive \
		vim-ale \
		ctags

Do not worry about the `--allowerasing` option, just review the installation
transaction prior confirming. This option is there to tell the package manager
to replace existing package `nano-default-editor` with `vim-default-editor`. It
is a small package that drops a shell configuration files to set EDITOR
environment variable to `vim` and this is a must have if you want to use Vim
(e.g. with git). This is a special thing for Fedora, you will not need to do
this on other distributions or OSes - just make sure your EDITOR shell variable
is correctly set.

A quick overview what I consider a good and clean plugin set:

* ctrlp - smallest possible fuzzy-finder plugin (pure vimscript)
* fugitive - a must have tool for git
* trailing-whitespace - shows and fixes, well, trailing whitespace
* airline - an improved status line (pure vimscript)
* ale - highlights typos or syntax errors as you type
* ctags - not a Vim plugin but a very much needed tool

There are other fuzzy-finder plugins like Command-T or my faviourite (very
fast) fzf.vim. Thing is, fzf.vim is not in Fedora and I want the smallest
possible configuration. CtrlP will do just fine and it is much more easier to
configure as it requires nothing.

If I were to choose absolute minimum configuration it would be:

	# cat ~/.vimrc
	let mapleader=","
	let maplocalleader="_"
	filetype plugin indent on
	let g:ctrlp_map = '<leader><leader>'
	let g:ctrlp_user_command = ['.git/', 'git --git-dir=%s/.git ls-files -oc --exclude-standard']
	set exrc
	set secure

But that is probably too extreme, so here is slightly bigger configuration with
my detail explanation below:

	" vim: nowrap sw=2 sts=2 ts=2 et:

	" leaders
	let mapleader=","
	let maplocalleader="_"

	" filetype and intent
	filetype plugin indent on

	" incompatible plugins
	if has('syntax') && has('eval')
	  packadd! matchit
	end

	" be SSD friendly (can be dangerous!)
	"set directory=/tmp

	" move backups away from projects
	set backupdir=~/.vimbackup

	" fuzzy searching
	let g:ctrlp_map = '<leader><leader>'
	let g:ctrlp_user_command = ['.git/', 'git --git-dir=%s/.git ls-files -oc --exclude-standard']
	nnoremap <leader>b :CtrlPBuffer<cr>
	nnoremap <leader>t :CtrlPTag<cr>
	nnoremap <leader>f :CtrlPBufTag<cr>
	nnoremap <leader>q :CtrlPQuickfix<cr>
	nnoremap <leader>m :CtrlPMRU<cr>

	" buffers and quickfix
	function! ToggleQuickFix()
	  if empty(filter(getwininfo(), 'v:val.quickfix'))
	    copen
	  else
	    cclose
	  endif
	endfunction
	nnoremap <leader>w :call ToggleQuickFix()<cr>
	nnoremap <leader>d :bd<cr>

	" searching ang grepping
	nnoremap <leader>g :copen<cr>:Ggrep! <SPACE>
	nnoremap K :Ggrep "\b<C-R><C-W>\b"<cr>:cw<cr>
	nnoremap <leader>s :set hlsearch! hlsearch?<cr>

	" ctags generation
	nnoremap <leader>c :!ctags -R .<cr><cr>

	" per-project configs
	set exrc
	set secure

I like having my leader key mapped to comma instead of the default backslash.
It is the closest free key in Vim when your hands are in writing position. Also
this key is same in most keyboard layouts while `\` varies per model or layout.
I rarely use local leader but underscore looks like a good fit.

Further reading:

* `:help map-which-keys`: https://vimhelp.org/map.txt.html#map-which-keys
* https://vim.fandom.com/wiki/Unused_keys

Next up it is the very important filetype command. See, Vim comes with
"batteries included", version 8.2 contains syntax highlighting for 644
languagues, 251 filetype definitions (ftplugins) and intentation rules for 138
languages. However, indentation is not enabled by default perhaps to deliver a
consistent editing experience for all. I like to enable it.

A quick tip: If you are editing a very large file and Vim feels slow, you may
want to disable syntax highlighting to speed things up. Just type `:syn off`
command.

Further reading:

* `:help filetype`: https://vimhelp.org/filetype.txt.html
* `:help syntax`: https://vimhelp.org/syntax.txt.html
* `:help indent`: https://vimhelp.org/indent.txt.html

Vim even comes with some extra plugins which makes some feature incompatible,
one of these is quite useful. It is the matchit plugin which makes `%` key
which finds matching paren to work with some languages. Typically, you can find
beginning or end of a block (`begin` and `end`) or HTML matching tags and
similar.

Further reading:

* `:help matchit`: https://vimhelp.org/usr_05.txt.html#matchit-install

One of the many settings I want to keep from my old config is using `/tmp` for
swap and creating backups in a separate directory in my home which you need to
create with `mkdir ~/.vimbackup`. Now, it is important to understand that Vim
creates a copy called "swap file" when you start editing and all the unsaved
work is saved in this file. So even if there is a power outage, your swap will
contain most of the unsaved work. I prefer using tmpfs as all my laptops and
servers are protected with UPS and I am used to save quite often. Also, most of
the times you will utilize swap files when your ssh connection is lost rather
than thank to a power outage. Swap files can be quite big for large files and I
value my SSD wear so I am making the decision here, if you are unsure remove
this statement to use `/var/tmp` which is safer.

Further reading:

* `:help swap-file`: https://vimhelp.org/recover.txt.html#swap-file

Now, the fuzzy finder is a plugin I cannot live without. Opening files via
commands like `:Ex` or `:e` or `:tabe` is okayish on a server when you need to
open like 20 files a day. When coding, we usually need to open hundreds of
them. As I said, CtrlP does the job nicely, it is small, no dependencies, pure
Vim. It opens with Ctrl-P combination which is a bit weird to me, I know that
some famous editors use it (VSCode I think).  Thing is, these are already
important Vim keybindings I do not want to override.  So the winner for me is
leader+leader (comma pressed twice).

The `ctrlp_user_command` just changes how CtrlP is getting the file list,
instead the build-in recursive file lister (glob) it uses `git ls-files` which
is usually better as it ignores things from `.gitignore` so things like
`node_modules` or other irrelevant directories which can slow down the listing
are not in the way.

Leader+b/t/f/q/m to open list of buffers, tags, tags from current file, quick
fix buffer and most recently used files is very useful too. Specifically, once
you generated a taglist with ctags, this is essentially "Go To Definition" for
hundreds of programming languages - no plugins needed! This is all built-in
Vim. Now to put thigs straigt, when I type leader+b it means pressing comma and
then pressing b key, not together like with Control or Shift.

Further reading:

* `:help Explore`: https://vimhelp.org/pi_netrw.txt.html#netrw-explore
* https://github.com/kien/ctrlp.vim

Although Vim supports tabs these days, buffer management is an important skill
for mastering Vim, what I usually end up with is having too many buffers and I
need to do `:bdelete` way too often.  Well, leader+d seems like a good option
to do that faster. I also like to be able to close quickfix window so there is
the leader+q combination for that too. I use this very often when browsing
search results.

Further reading:

* `:help buffer-hidden`: https://vimhelp.org/windows.txt.html#buffer-hidden

Speaking about searching, it is as important as opening files. I want to be
able grep the codebase, for that there is the awesome `:Ggrep` command from
fugitive plugin which uses `git grep` which by design ignores junk files and
only searches what's in git. Since Shift-K is a free key in Vim, it is a great
fit for automatically grepping the term under cursor. And finally, being able
to enter arbitrary search pattern via leader+g is also nice. Note this opens a
window which is called Quickfix window where you can navigate the results, go
to next occurance, previous, last, first and more. The same window is used for
output from compilators or other tools so get familiar with it. I suggest
further reading in the documentation if this is new to you.

Further reading:

* `:help quickfix`: https://vimhelp.org/quickfix.txt.html
* https://github.com/tpope/vim-fugitive

By the way, searching via `/` key is smart sensitive, meaning if all characters
are lower case, Vim searches ignoring case. By default it highlights results
and I think I typed `:noh` (turn of highlighting) about a million times, that's
why I have leader+s to toggle this. I suggest to read more about searching in
the manual later on too.

Searching and grepping is next. The fugitive plugin has you covered. Use the
command `:Ggrep pattern` to do a git grep, results will go into the Quickfix
window. Then simply navigate through the results via quick fix commands (`:cn`,
`:cp` etc) or simply use `:CtrlPQuickfix` (or leader+q) to scroll them
visually. What is cool about the CtrlP quick fix integration is you can further
search the results just by typing to match filenames or content as well, if it
makes sense. Searching the results of a search.

Further reading:

* `:help grep`: https://vimhelp.org/quickfix.txt.html#grep
* `:help noh`: https://vimhelp.org/pattern.txt.html#noh
* https://github.com/tpope/vim-fugitive

Leader+c to generate ctags file for better navigation is useful when I am
dealing with a new codebase or doing some longer coding session with lots of
jumps around. Ctags supports hundreds of languages and Vim can use all this
knowledge to navigate it. More about how to configure it later. Note we already
discussed leader+t to open fuzzy search for all tags, remember? It is the very
same thing.

Further reading:

* `:help ctags`: https://vimhelp.org/tagsrch.txt.html
* https://ctags.io

Being able to override any other setting in projects by creating `.vimrc` file
in a project directory is a good idea to do. Just put it in the (global)
`.gitignore` to make sure you don't need to edit thousands of git ignore files
in each project.  Such a project `.vimrc` could be something like (for C/C++
project with GNU Makefile):

	" coding style
	set tabstop=4
	set softtabstop=4
	set shiftwidth=4
	set noexpandtab
	" include and autocomplete path
	let &path.="/usr/local/include"
	" function keys to build and run the project
	nnoremap <F9> :wall!<cr>:make!<cr><cr>
	nnoremap <F10> :!LD_LIBRARY_PATH=/usr/local/lib ./project<cr><cr>

As you can see, I typically map F2-F10 keys to compile, run, test and similar
actions. Using F9 for calling `make` sounds about right, remember the blue
Borland IDE from MS-DOS?

As mentioned earlier, is a good idea to ignore both `.vimrc` and `tags`
(generated by `ctags`) globally so there is no need to update every each
`.gitignore`:

	# git config --global core.excludesfile ~/.gitignore
	# cat ~/.gitignore
	/.vimrc
	/tags
	/TAGS

There are actually few more statements in my personal config which are only
relevant for those with non-US keyboard layouts (I am on Czech). I need to use
dead keys for many characters and it is simply not possible and I'd rather type
the command instead of doing those hard-to-reach combinations. Here is a
solution to the problem:

	" CTRL-] is hard on my keyboard layout
	map <C-K> <C-]>
	" CTRL-^ is hard on my keyboard layout
	nnoremap <F1> :b#<cr>
	nnoremap <F2> :bp<cr>
	nnoremap <F3> :bn<cr>
	" I hate entering Ex mode by accient
	map Q <Nop>

Further reading:

* `:help map`: https://vimhelp.org/map.txt.html

Function keys are all free in Vim, except F1 which is bound to help. I don't
need help, not that I would already know everything about Vim. Not at all. But
I can simply type `:help` if needed. And F1 is cruical key, so close to the Esc
key. I like to use buffer swapping (`:b#`) for that as well as F2-F3 for
next/previous. The more you work with buffers the more you will need this. If
you haven't used Ctrl-^ I suggest to get used to it. Oh, have you ever entered
the Ex mode with the ugly `type :visual`? Many begginners had no idea how to
quit Vim from that mode, for me it is just disturbing as I rarely use it. 

Now, getting familiar with `ctags` is a key thing to be successful with Vim.
This tool supports hundreds of languages and it can easily create tags for
files you do not want to create, therefore I suggest to ignore typical junk
directories:

	# cat ~/.ctags.d/local.ctags
	--recurse=yes
	--exclude=.git
	--exclude=build/
	--exclude=.svn
	--exclude=vendor/*
	--exclude=node_modules/*
	--exclude=public/webpack/*
	--exclude=db/*
	--exclude=log/*
	--exclude=test/*
	--exclude=tests/*
	--exclude=\*.min.\*
	--exclude=\*.swp
	--exclude=\*.bak
	--exclude=\*.pyc
	--exclude=\*.class
	--exclude=\*.cache

I must not forget about vim-airline plugin, out of the two in Fedora this one
is light, no external dependencies are needed and it works out of box with all
my fonts. You can customize it, there are themes and such things. I just happen
to like the default setting.

One thing I must mention is that there are two main ctag projects, Exuberant
Ctags and Universal Ctags. The latter is a more modern fork, if your
distribution have it, use that. If you are on Fedora 35+ all you need to know
that you are now on Universal Ctags.

Before I wrap it up, here is what I suggest. Try to keep your Vim configuration
slick and clean. It will pay off in the future. After I switched, I had to
re-learn "write and quit" command because I was typing it as `:Wq` accidentaly
all the time and I had a "hack" in the old configuration that actually did what
I meant. Okay, this one might be actually useful and make the cut, I hope you
get what I mean:

	:command Wq wq
	:command WQ wq

Here is a final quick tip - you may need to change your default Vim
configuration a lot while finding the sweetspot of what I presented you here
and your own taste. Use the following alias so you don't need to search the
history all the time. Trust me, when a Vim user searches history for "vim",
nothing is relevant:

	alias vim-vimrc='vim ~/.vimrc'

There you have it, maybe this can help you navigating through the rich world of
Vim without ton of plugins. "Vanilla" Vim is fun!

To try out what you just read, install the packages and check out the config:

	test -f ~/.vimrc && mv ~/.vimrc ~/.vimrc.backup
	curl -s https://raw.githubusercontent.com/lzap/vim-lzap/master/.vimrc -o ~/.vimrc
	mkdir ~/.vimbackup

Special thanks to Marc Deop and Melanie Corr for reviewing my article.

