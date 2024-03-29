---
type: "post"
aliases:
- /2012/11/ruby-19-mri-vs-google-dart-02-tp.html
date: "2012-11-07T00:00:00Z"
tags:
- linux
- ruby
- dart
title: Ruby 1.9 MRI vs Google Dart 0.2 TP
---

Ok, I know I know. Those are not tests, but I was just trying out Dart
language tonight and I wanted to share this. Such a young language, but driven
by V8 Google team, is that fast.

This is my Ruby version compiled about four weeks ago. By MRI I mean Matz
Reference Implementation, the widely used Ruby VM. There are more and faster,
but not much.

    $ ruby --version
    ruby 1.9.3p286 (2012-10-12 revision 37165) [x86_64-linux]

And this is Dart I just downloaded today, compiled one week ago. By TP I mean
Technology Preview. This is work in progress for sure.

    $ dart --version
    Dart VM version: 0.2.2.1_14493_chrome-bot (Fri Nov  2 11:25:18 2012)

Now the "fight" code for Ruby:

    $ cat fib.rb
    def fib(n)
        n < 2 ? n : fib(n-1) + fib(n-2)
    end
    for i in 1..40
        f = fib i
        puts "#{i} + #{f}"
    end

And the same for Dart:

    $ cat fib.dart 
    int fib(int n) {
       if (n < 2) return n;
       return fib(n - 1) + fib(n - 2);
    }
    main() {
      for (int i = 0; i <= 40; i++) {
        var f = fib(i);
        print("$i = $f");
      }
    }

Again, this says really nothing. But what can stop me from running this? ;-)

    $ time ruby fib.rb
    1 + 1
    2 + 1
    3 + 2
    4 + 3
    5 + 5
    6 + 8
    7 + 13
    8 + 21
    9 + 34
    10 + 55
    11 + 89
    12 + 144
    13 + 233
    14 + 377
    15 + 610
    16 + 987
    17 + 1597
    18 + 2584
    19 + 4181
    20 + 6765
    21 + 10946
    22 + 17711
    23 + 28657
    24 + 46368
    25 + 75025
    26 + 121393
    27 + 196418
    28 + 317811
    29 + 514229
    30 + 832040
    31 + 1346269
    32 + 2178309
    33 + 3524578
    34 + 5702887
    35 + 9227465
    36 + 14930352
    37 + 24157817
    38 + 39088169
    39 + 63245986
    40 + 102334155

    real    1m9.215s
    user    1m6.852s
    sys 0m0.035s

A minute and ten. Not bad. Now let's have a look on Dart.

    $ time dart fib.dart 
    0 = 0
    1 = 1
    2 = 1
    3 = 2
    4 = 3
    5 = 5
    6 = 8
    7 = 13
    8 = 21
    9 = 34
    10 = 55
    11 = 89
    12 = 144
    13 = 233
    14 = 377
    15 = 610
    16 = 987
    17 = 1597
    18 = 2584
    19 = 4181
    20 = 6765
    21 = 10946
    22 = 17711
    23 = 28657
    24 = 46368
    25 = 75025
    26 = 121393
    27 = 196418
    28 = 317811
    29 = 514229
    30 = 832040
    31 = 1346269
    32 = 2178309
    33 = 3524578
    34 = 5702887
    35 = 9227465
    36 = 14930352
    37 = 24157817
    38 = 39088169
    39 = 63245986
    40 = 102334155

    real    0m3.936s
    user    0m3.767s
    sys 0m0.006s

Four seconds. Wait, four seconds? Hmmm, does this mean Dart VM is faster than Ruby VM?
Not necessarily. Does this mean optimizer in Dart is better than in Ruby? Hell yeah!

