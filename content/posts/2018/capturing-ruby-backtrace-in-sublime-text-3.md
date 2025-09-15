---
type: "post"
aliases:
- /2018/09/capturing-ruby-backtrace-in-sublime-text-3.html
date: "2018-09-05T00:00:00Z"
tags:
- linux
title: Capturing Ruby backtrace in Sublime Text 3
---

I am a heavy Vim user for over two decades now, but from time to time I want to
give break to my hands and just browse code with mouse while doing reviews.
This is where Vim is not good at, I've never felt in love with NERDTree plugin
or these kind of stuff. Directory tree simply doesn't look good in terminal.
From all the modern editors like Textmate, Atom, VSCode and similar I like
Sublime Text the most.

Being able to execute Ruby code or tests from Sublime Text is nice, it provides
a regular expression parser to make backtrace "clickable". It comes with
definition for Ruby:
https://github.com/sublimehq/Packages/blob/master/Ruby/Ruby.sublime-build


    {
      "shell_cmd": "ruby \"$file\"",
      "file_regex": "^(...*?):([0-9]*):?([0-9]*)",
      "selector": "source.ruby"
    }

The thing is - it does not work in most cases.

There are multiple backtrace formatting in Ruby. In versions 1.8 - 2.4 the
format is:

    test.rb:7:in `partridges': Shouldn't this be recursive? (RuntimeError)
      from test.rb:3:in `turtle_doves'
      from test.rb:10:in `<main>'

Starting from Ruby 2.5 it's reversed with index numbers:

    Traceback (most recent call last):
      2: from test.rb:10:in `<main>'
      1: from test.rb:3:in `turtle_doves'
    test.rb:7:in `partridges': Shouldn't this be recursive? (RuntimeError)

The regular expression in Sublime Text 3 (build from summer 2018) does only
capture line 7 and completly ignores "from" lines. But there's more, exceptions
are often printed to console via `backtrace` call from `Exception` class from
Ruby standard library. An example from our application:

    E, [2017-01-16T12:15:59.678835 #32142] ERROR -- : undefined method `join' for #<String:0x007f1a587784a8> (NoMethodError)
    /usr/share/sinatra-1.3.5/lib/sinatra/showexceptions.rb:37:in `rescue in call'
    /usr/share/sinatra-1.3.5/lib/sinatra/showexceptions.rb:21:in `call'
    /usr/share/sinatra-1.3.5/lib/sinatra/base.rb:124:in `call'
    ...

Testing frameworks does the same often prepending whitespace (tab usually) for
each line:

    NoMethodError: undefined method `render' for "test":String
        app/models/host/base.rb:351:in `render_template'
        /home/lzap/work/foreman_discovery/lock_templates.rb:14:in `block in lock_templates'
        /home/lzap/work/foreman_discovery/lock_templates.rb:10:in `each'
        /home/lzap/work/foreman_discovery/lock_templates.rb:10:in `lock_templates'

Sublime Text needs a regular expression which captures them all. I had to find
how to do non-capturing group in Sublime regular parser and the rest was easy:

    {
      "shell_cmd": "ruby \"$file\"",
      "file_regex": "^\\s*(?:\\d:)?\\s*(?:from )?([^:]+):(\\d+):in",
      "selector": "source.ruby"
    }

I filed a PR in the Sublime Packages repo with the change: https://github.com/sublimehq/Packages/pull/1706

That should do it. Have fun!

