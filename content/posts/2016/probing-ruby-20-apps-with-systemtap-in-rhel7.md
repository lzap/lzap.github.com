---
type: "post"
aliases:
- /2016/08/probing-ruby-20-apps-with-systemtap-in-rhel7.html
date: "2016-08-02T00:00:00Z"
tags:
- linux
- fedora
- systemtap
title: Probing Ruby 2.0 apps with SystemTap in RHEL7
---

Few years ago, I wrote an article about SystemTap and Ruby in RHEL6. When RHEL
7.0 was released, things changed. It has Ruby 2.0 and the Ruby SystemTap API
changed as well, therefore I am updating my old article today according to new
changes.

Imagine you have a Ruby application that has some performance issues on a
production server and it's running RHEL 7.0 or newer. With SystemTap, you can
easily peek into the running application and investigate bottlenecks or count
memory objects. If you know DTrace from other operating systems, welcome home.

Installation of SystemTap is easy and straightforward and for our purposes we
do not need to install kernel devel and debug info packages.

    # yum -y install systemtap systemtap-runtime ruby

Let's create a trivial application called factorial.rb.

    # cat factorial.rb
    def factorial n
      f = 1; for i in 1..n; f *= i; end; f
    end
    puts factorial(ARGV[0].to_i)

And a simple SystemTap script that shows method calls:

    # cat rubycalls.stp
    probe ruby.method.entry, ruby.cmethod.entry
    {
      if (file == "factorial.rb") {
        printf("%s => %s.%s in %s:%d\n", thread_indent(1), classname, methodname, file, line);
      }
    }
    probe ruby.method.return, ruby.cmethod.return
    {
      if (file == "factorial.rb") {
        printf("%s <= %s.%s in %s:%d\n", thread_indent(-1), classname, methodname, file, line);
      }
    }

Let's just run it for now.)

    # stap rubycalls.stp -c "ruby factorial.rb 4"
    24
     0 ruby(29131): => IO.set_encoding in factorial.rb:0
     6 ruby(29131): <= IO.set_encoding in factorial.rb:0
     0 ruby(29131): => IO.set_encoding in factorial.rb:0
     3 ruby(29131): <= IO.set_encoding in factorial.rb:0
     0 ruby(29131): => #<Class:0x00000002378c80>.core#define_method in factorial.rb:1
     6 ruby(29131):  => Module.method_added in factorial.rb:1
     9 ruby(29131):  <= Module.method_added in factorial.rb:1
    45 ruby(29131): <= #<Class:0x00000002378c80>.core#define_method in factorial.rb:1
     0 ruby(29131): => String.to_i in factorial.rb:4
     2 ruby(29131): <= String.to_i in factorial.rb:4
     0 ruby(29131): => Object.factorial in factorial.rb:1
    19 ruby(29131):  => Range.each in factorial.rb:2
    23 ruby(29131):  <= Range.each in factorial.rb:2
    25 ruby(29131): <= Object.factorial in factorial.rb:3
     0 ruby(29131): => Kernel.puts in factorial.rb:4
     7 ruby(29131):  => IO.puts in factorial.rb:4
    15 ruby(29131):   => Fixnum.to_s in factorial.rb:4
    18 ruby(29131):   <= Fixnum.to_s in factorial.rb:4
    21 ruby(29131):   => IO.write in factorial.rb:4
    40 ruby(29131):   <= IO.write in factorial.rb:4
    43 ruby(29131):   => IO.write in factorial.rb:4
    48 ruby(29131):   <= IO.write in factorial.rb:4
    50 ruby(29131):  <= IO.puts in factorial.rb:4
    52 ruby(29131): <= Kernel.puts in factorial.rb:4

Please note you have to run SystemTap under root account and also expect the
first run to be a little bit slower, because SystemTap is compiling and
inserting a kernel module under the hood.

SystemTap syntax is similar to C and the easiest way of learning it is reading
[SystemTap Beginners
Guide](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/SystemTap_Beginners_Guide/).
From the book:

*SystemTap allows users to write and reuse simple scripts to deeply examine the
activities of a running Linux system. These scripts can be designed to extract
data, filter it, and summarize it quickly (and safely), enabling the diagnosis
of complex performance (or even functional) problems.*

*The essential idea behind a SystemTap script is to name events, and to give
them handlers. When SystemTap runs the script, SystemTap monitors for the
event; once the event occurs, the Linux kernel then runs the handler as a quick
sub-routine, then resumes.*

*There are several kinds of events; entering or exiting a function, timer
expiration, session termination, etc. A handler is a series of script language
statements that specify the work to be done whenever the event occurs. This
work normally includes extracting data from the event context, storing them
into internal variables, and printing results.*

The following example will count method calls to quickly search for
bottlenecks. If you don't understand how it works, head over to the Beginners
Guide for more details.

    # cat rubystack.stp
    #!/usr/bin/stap·

    global fn_calls;

    probe ruby.method.entry, ruby.cmethod.entry
    {
      fn_calls[classname, methodname] <<< 1;
    }

    probe end {
      foreach ([classname, methodname] in fn_calls- limit 30) {
        printf("%dx %s.%s\n", @count(fn_calls[classname, methodname]), classname, methodname);
      }

      delete fn_calls;
    }

Everytime a Ruby method is entered, counter is incremented by one in a global
associative array. It prints top thirty counters on exit. When we run it, it's
a surprise!

    # stap rubystack.stp -c "ruby factorial.rb 42"
    1405006117752879898543142606244511569936384000000000
    2904x Module.===
    1782x BasicObject.==
    1782x Kernel.===
    1027x Symbol.to_s
    1004x Kernel.initialize_dup
    1003x Kernel.dup
    990x Kernel.instance_variable_set
    695x String.to_s
    684x Hash.[]=
    660x Gem::Specification.default_value
    508x String.initialize_copy
    456x Class.new
    396x Array.initialize_copy
    388x String.gsub
    336x Kernel.class
    324x Array.each
    322x RbConfig.expand
    320x Module.method_added
    292x Array.flatten
    267x File.file?
    244x String.<=>
    242x #<Class:0x0000000221ad70>.core#define_method
    229x String.to_i
    210x Enumerable.any?
    185x String.strip
    184x File.join
    181x Regexp.=~
    169x Kernel.untaint
    168x Kernel.respond_to?
    161x String.=~

I'd expect multiplying operation (`Bignum.*`) but we see equality of module
instead. Since we count *all* the method calls, we can see what Ruby needs to
done in the backround to load such a trivial example. It's actually rubygems
gem which ships with Ruby 2.0 that does the loading mechanics (and it's poorly
designed in my opinion).

Anyway, if you want to see the bignum thing, increase the parameter from 42 to
let's say 500. Now another example, slightly modified example from the [SystemTap Wiki](https://sourceware.org/systemtap/wiki/RubyMarker):

    # cat rubytop.stp
    #!/usr/bin/stap
    global fn_calls
    probe ruby.method.entry, ruby.cmethod.entry
    {
      fn_calls[file, methodname, line] <<< 1
    }
    probe timer.ms(1000) {
      ansi_clear_screen()
      printf("%80s %6s %30s %6s\n", "FILENAME", "LINE", "METHOD", "CALLS")
      foreach ([filename, funcname, lineno] in fn_calls- limit 15) {
        printf("%80s %6d %30s %6d\n", filename, lineno, funcname, @count(fn_calls[filename, funcname, lineno]))
      }
    }
    probe timer.ms(300000) {
      delete fn_calls
    }

Now run the example with huge input that will cause it to loop for some time:

    # stap rubytop.stp -c "ruby factorial.rb 999999999"

You should see a top-like screen which refreshes every second. The initial
page will be full of method calls while from second one you will only see
increasing counter of the multiply method:

                                            FILENAME   LINE                         METHOD  CALLS
                                        factorial.rb      2                              * 123483
       /usr/share/rubygems/rubygems/specification.rb   1775                            ===   3663
       /usr/share/rubygems/rubygems/specification.rb   1775                             ==   1782
       /usr/share/rubygems/rubygems/specification.rb   1779          instance_variable_set    660
       /usr/share/rubygems/rubygems/specification.rb   1779                           to_s    660
       /usr/share/rubygems/rubygems/specification.rb   1471                  default_value    660
       /usr/share/rubygems/rubygems/specification.rb   1776                            dup    594
       /usr/share/rubygems/rubygems/specification.rb   1776                 initialize_dup    594
       /usr/share/rubygems/rubygems/specification.rb   1776                initialize_copy    594
       /usr/share/rubygems/rubygems/specification.rb   1769                           to_s    330
       /usr/share/rubygems/rubygems/specification.rb   1769          instance_variable_set    330
                         /usr/lib64/ruby/rbconfig.rb    235                         expand    322
                         /usr/lib64/ruby/rbconfig.rb    236                           gsub    322
       /usr/share/rubygems/rubygems/specification.rb   1402                          file?    234
         /usr/share/rubygems/rubygems/requirement.rb     51                            ===    226

SystemTap is flexible, you can ignore some files (or directories) completely.
Maybe you are only interested in code that was installed in
`/usr/share/project` and you never want to see Kernel and Bignum classes, it's
as easy as:


    probe ruby.method.entry, ruby.cmethod.entry
    {
      if (file =~ "^/usr/share/project" && classname !~ "^(Kernel|Bignum)$") {
        fn_calls[file, methodname, line] <<< 1
      }
    }

By default, the counter struct resets every 5 minutes (see the second timer
probe).

SystemTap Ruby markers in RHEL 7.0 offers the following probes:

    ruby.array.create
    ruby.cmethod.entry
    ruby.cmethod.return
    ruby.find.require.entry
    ruby.find.require.return
    ruby.gc.mark.begin
    ruby.gc.mark.end
    ruby.gc.sweep.begin
    ruby.gc.sweep.end
    ruby.hash.create
    ruby.load.entry
    ruby.load.return
    ruby.method.entry
    ruby.method.return
    ruby.object.create
    ruby.parse.begin
    ruby.parse.end
    ruby.raise
    ruby.require.entry
    ruby.require.return
    ruby.string.create

It is also possible to attach to existing process:

    # stap rubytop.stp -x 12345

When using Software Collections, note the correct SCL enable syntax (credit to
[Pavel Valena](https://bugzilla.redhat.com/show_bug.cgi?id=1362437) from Red Hat):

    # scl enable rh-ruby22 -- stap rubystack.stp -c "ruby factorial.rb 5"

That's all for now.

