---
type: "post"
aliases:
- /2016/03/human-readable-name-generator.html
date: "2016-03-07T00:00:00Z"
tags:
- linux
- ruby
- foreman
title: Human readable name generator
---

Out of ideas for incoming bare-metal host names in your cluster? I wrote a
little generator which contains frequently occurring given names and surnames
from the 1990 US Census (public domain data):

* 256 (8 bits) unique male given names
* 256 (8 bits) unique female given names
* 65,536 (16 bits) unique surnames

Given names were filtered to be 3-5 characters long, surnames 5-8 characters,
therefore generated names are never longer than 14 characters (5+1+8).

This gives 33,554,432 (25 bits) total of male and female name combinations. The
generator can either generate randomized succession, or generate combinations
based on MAC adresses.

### Random generator

The random name generator makes use of [Fibonacci linear feedback shift
register](https://en.wikipedia.org/wiki/Linear_feedback_shift_register) which
gives deterministic sequence of pseudo-random numbers. Additionally, algorithm
makes sure names with same first name (or gender) and last name are not
returned in succession. Since there are about 1% of such cases, there are
about 33 million unique total names. Example sequence:

* velma-pratico.my.lan
* angie-warmbrod.my.lan
* grant-goodgine.my.lan
* alton-sieber.my.lan
* velma-vanbeek.my.lan
* don-otero.my.lan
* sam-hulan.my.lan

The polynomial used in linear feedback shift register is

    x^25 + x^24 + x^23 + x^22 + 1.

The key thing is to store register (a number) and use it for each generation
in order to get non-repeating sequence of name combinations. See example below.

### MAC generator

Examples of MAC-based names:

* 24:a4:3c:ec:76:06 -> bobby-louie-sancher-weeler.my.lan
* 24:a4:3c:e3:d3:92 -> bob-louie-sancher-rimando.my.lan

MAC addresses with same OID part (24:a4:3c in this case) generates the same
middle name ("Louie Sancher" in the example above), therefore it is possible to
guess server (or NIC) vendor from it, or it should be possible to shorten
middle names (e.g. bobby-ls-weeler.my.lan) in homogeneous environments.

## Comparison of types

MAC-based advantages

* reprovisioning the same server generates the same name
* middle names are same for unique hardware vendors

MAC-based disadvantages

* name is longer

Random-based advantages

* name is shorter

Random-based disadvantages

* reprovisioning the same server generates different name

## Usage

Visit [project homepage](https://github.com/lzap/deacon) to see some examples.
Also try [the Foreman](http://www.theforeman.org) which will (hopefully) have
a embedded generator based on Deacon library in the 1.12 release.

## Why the?

Deacon is a ministry in the Christian Church that is generally associated with
service of some kind, but which varies among theological and denominational
traditions. In many traditions the "diaconate" (or deaconate), the term for a
deacon's office, is a clerical office; in others it is for laity. -- Wikipedia

