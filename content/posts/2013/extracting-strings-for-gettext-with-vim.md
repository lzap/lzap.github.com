---
type: "post"
aliases:
- /2013/04/extracting-strings-for-gettext-with-vim.html
date: "2013-04-03T00:00:00Z"
tags:
- linux
- fedora
- foreman
title: Extracting strings for gettext with Vim
---

Big news today, I will be working on Foreman open-source project from now on.
Recently I was working on Katello - subscription and package management
system.

The Foreman is a complete lifecycle management tool for physical and virtual
servers. More info at http://www.theforeman.org

I have been extracting strings today from the codebase for gettext support. If
you don't know what that, let me briefly describe it. I need to convert all
"strings" or 'strings' into the following format:

    _("string")
    _('string')
    _("String with %s") % (parameter)
    _("String with %{multiple} %{parameters}") % { :multiple => 'blah',
        :parameters => 43 }

To do that I have decided to create few macros/mappings for Vim. I guess it is
quite self-explanatory.

    "
    " Helper vim commands for manual gettext string extraction. Following macros
    " are optimized for Ruby language in the following format:
    "
    " _("string")
    " _('string')
    " _("One parameter: %s) % (param)
    " _("Two or more %{param1} and %{param2}") % { :param1 => 1, :param2 => :xyz }
    "
    " To use this technique just source this file:
    "
    " source ./path/to/gettext_extraction.vim
    "
    " The workflow is simple:
    " 
    " Search for "strings" and 'strings' using this key and use "n" key to find
    " required string you want to convert
    " 
    map <F12> /["'][^"]*["']<CR>
    "
    " Once a match is found and the caret is on the first quote, use one of the 
    " following keys to wrap _() around
    "
    map <F5> i_(<ESC>2f"a)<ESC>2F"
    map <F6> i_(<ESC>2f'a)<ESC>2F'
    "
    " If there is one parameter, you can create % () behind the string using this
    " key
    "
    map <F7> mXf"f)a % ()<ESC>`X
    "
    " And then press this key to change the parameter to %s and move it into
    " prepared braces
    "
    map <F8> mXf#ll"ndt}F#cf}%s<ESC>2f)"nP<ESC>`X
    "
    " If there are two or more params prepare curly braces behind the string using
    " this key
    "
    map <F9> mXf"f)a % { }<ESC>`X
    " 
    " And then pres this key multple times to rewrite #{xyz} params to %{xyz}
    " params and move them into the hash { :xyz => xyz }
    "
    map <F10> mXf#ll"ndt}F#cf}%{}<ESC>"nPf%f}i:<ESC>"npa => <ESC>"npa, <ESC>`X
    " 
    " Note if the params contains @ or @@ you will need to clean this out. Also
    " the last macro leaves tailing comma - if you don't like it, remove manually.
    "
    " The typical key flow is:
    " F12 n n n n F6 n n n F5 F7 F8 n n n F5 F9 F10 n n ...
    "

Here is a link to my git where you can find the most recent version of these
macros:
https://github.com/lzap/vim-lzap/blob/master/macros/gettext_extraction.vim


