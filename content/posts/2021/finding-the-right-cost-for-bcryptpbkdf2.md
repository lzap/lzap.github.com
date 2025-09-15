---
type: "post"
aliases:
- /2021/05/finding-the-right-cost-for-bcryptpbkdf2.html
date: "2021-05-11T00:00:00Z"
tags:
- linux
- fedora
- foreman
title: Finding the right cost for bcrypt/pbkdf2
---

Foreman uses bcrypt with variable cost as the default password hashing
approach, but I learned that bcrypt is not approved for passwords by NIST the
other day. Before finishing my patch, I wanted to see what are the sane
iteration counts for PBKDF2-HMAC-SHA algorithm which is approved by NIST. Here
are results to give you rough estimation from my Intel NUC i3 8th gen running
i3-8109U, a CPU from 2018:

```
       user     system      total        real
PBKDF2 SHA-1 with 1 iters	  0.000024   0.000007   0.000031 (  0.000028)
PBKDF2 SHA-1 with 100001 iters	  0.064736   0.000000   0.064736 (  0.064842)
PBKDF2 SHA-1 with 200001 iters	  0.129461   0.000000   0.129461 (  0.129587)
PBKDF2 SHA-1 with 300001 iters	  0.195255   0.000000   0.195255 (  0.195449)
PBKDF2 SHA-1 with 400001 iters	  0.259314   0.000000   0.259314 (  0.259565)
PBKDF2 SHA-1 with 500001 iters	  0.324826   0.000000   0.324826 (  0.325150)
PBKDF2 SHA-1 with 600001 iters	  0.388826   0.000000   0.388826 (  0.389216)
PBKDF2 SHA-1 with 700001 iters	  0.453290   0.000000   0.453290 (  0.453753)
PBKDF2 SHA-1 with 800001 iters	  0.518169   0.000000   0.518169 (  0.518704)
PBKDF2 SHA-1 with 900001 iters	  0.583946   0.000000   0.583946 (  0.584603)

       user     system      total        real
PBKDF2 SHA-256 with 1 iters	  0.000041   0.000000   0.000041 (  0.000040)
PBKDF2 SHA-256 with 100001 iters	  0.100197   0.000000   0.100197 (  0.100307)
PBKDF2 SHA-256 with 200001 iters	  0.200945   0.000000   0.200945 (  0.201145)
PBKDF2 SHA-256 with 300001 iters	  0.301221   0.000000   0.301221 (  0.301541)
PBKDF2 SHA-256 with 400001 iters	  0.402317   0.000000   0.402317 (  0.402714)
PBKDF2 SHA-256 with 500001 iters	  0.502404   0.000000   0.502404 (  0.502949)
PBKDF2 SHA-256 with 600001 iters	  0.607353   0.000000   0.607353 (  0.607923)
PBKDF2 SHA-256 with 700001 iters	  0.702174   0.000000   0.702174 (  0.702893)
PBKDF2 SHA-256 with 800001 iters	  0.804487   0.000000   0.804487 (  0.805271)
PBKDF2 SHA-256 with 900001 iters	  0.904246   0.000000   0.904246 (  0.905123)

       user     system      total        real
PBKDF2 SHA-512 with 1 iters	  0.000020   0.000000   0.000020 (  0.000020)
PBKDF2 SHA-512 with 100001 iters	  0.069437   0.000000   0.069437 (  0.069507)
PBKDF2 SHA-512 with 200001 iters	  0.138220   0.000000   0.138220 (  0.138372)
PBKDF2 SHA-512 with 300001 iters	  0.206984   0.000000   0.206984 (  0.207207)
PBKDF2 SHA-512 with 400001 iters	  0.278088   0.000000   0.278088 (  0.278450)
PBKDF2 SHA-512 with 500001 iters	  0.344130   0.000000   0.344130 (  0.344481)
PBKDF2 SHA-512 with 600001 iters	  0.413116   0.000000   0.413116 (  0.413551)
PBKDF2 SHA-512 with 700001 iters	  0.482472   0.000000   0.482472 (  0.482973)
PBKDF2 SHA-512 with 800001 iters	  0.553838   0.000000   0.553838 (  0.554417)
PBKDF2 SHA-512 with 900001 iters	  0.620699   0.000000   0.620699 (  0.621316)
```

This is an output from a quick benchmark written in Ruby which uses OpenSSL
library from Fedora 34 with 40 bytes salt, password and output. The script is
below if you want to run it. Anyway.

Say I want to target 40ms password hashing time on this class of CPU, which
should be a sane default for an on-premise intranet web application. In that
case, these are the recommended iteration counts:

* PBKDF2-HMAC-SHA1: 600_000 iterations
* PBKDF2-HMAC-SHA256: 400_000 iterations
* PBKDF2-HMAC-SHA512: 600_000 iterations

For roughly 20ms calculation time you can go with 250_000 iterations which
should be probably a safe but reasonable minimum in 2021 for a web app.

One thing is interesting tho, SHA256 is actually slower than SHA512. I would
not expect that, it looks like some padding. Or maybe an error in my benchmark
or the fact the test is written in Ruby? That should not be the case because
one call into OpenSSL native library is 40ms. To verify, I have rewritten the
code in Crystal, an LLVM Ruby-like language which recently hit the 1.0.0
version milestone. It was pretty much copy and paste, here is the result:

```
                                      user     system      total        real
PBKDF2 SHA-1 with 1 iters	        0.000006   0.000020   0.000026 (  0.000022)
PBKDF2 SHA-1 with 100001 iters	   0.064808   0.000050   0.064858 (  0.064933)
PBKDF2 SHA-1 with 200001 iters	   0.129531   0.000014   0.129545 (  0.129681)
PBKDF2 SHA-1 with 300001 iters	   0.194418   0.000000   0.194418 (  0.194606)
PBKDF2 SHA-1 with 400001 iters	   0.259126   0.000000   0.259126 (  0.259377)
PBKDF2 SHA-1 with 500001 iters	   0.324371   0.000000   0.324371 (  0.324689)
PBKDF2 SHA-1 with 600001 iters	   0.389384   0.000000   0.389384 (  0.389780)
PBKDF2 SHA-1 with 700001 iters	   0.454766   0.000000   0.454766 (  0.455242)
PBKDF2 SHA-1 with 800001 iters	   0.518768   0.000000   0.518768 (  0.519265)
PBKDF2 SHA-1 with 900001 iters	   0.584092   0.000000   0.584092 (  0.584682)
                                        user     system      total        real
PBKDF2 SHA-256 with 1 iters	        0.000015   0.000000   0.000015 (  0.000015)
PBKDF2 SHA-256 with 100001 iters	   0.100220   0.000000   0.100220 (  0.100331)
PBKDF2 SHA-256 with 200001 iters	   0.200525   0.000000   0.200525 (  0.200722)
PBKDF2 SHA-256 with 300001 iters	   0.301427   0.000000   0.301427 (  0.301713)
PBKDF2 SHA-256 with 400001 iters	   0.401965   0.000000   0.401965 (  0.402360)
PBKDF2 SHA-256 with 500001 iters	   0.501238   0.000000   0.501238 (  0.501742)
PBKDF2 SHA-256 with 600001 iters	   0.605589   0.000000   0.605589 (  0.606171)
PBKDF2 SHA-256 with 700001 iters	   0.702972   0.000000   0.702972 (  0.703676)
PBKDF2 SHA-256 with 800001 iters	   0.803881   0.000000   0.803881 (  0.804708)
PBKDF2 SHA-256 with 900001 iters	   0.902646   0.000000   0.902646 (  0.903572)
                                        user     system      total        real
PBKDF2 SHA-512 with 1 iters	        0.000015   0.000000   0.000015 (  0.000014)
PBKDF2 SHA-512 with 100001 iters	   0.068897   0.000000   0.068897 (  0.068960)
PBKDF2 SHA-512 with 200001 iters	   0.137699   0.000000   0.137699 (  0.137853)
PBKDF2 SHA-512 with 300001 iters	   0.206790   0.000000   0.206790 (  0.206982)
PBKDF2 SHA-512 with 400001 iters	   0.275695   0.000000   0.275695 (  0.275972)
PBKDF2 SHA-512 with 500001 iters	   0.344550   0.000000   0.344550 (  0.344882)
PBKDF2 SHA-512 with 600001 iters	   0.412838   0.000000   0.412838 (  0.413224)
PBKDF2 SHA-512 with 700001 iters	   0.482600   0.000000   0.482600 (  0.483100)
PBKDF2 SHA-512 with 800001 iters	   0.551040   0.000000   0.551040 (  0.551562)
PBKDF2 SHA-512 with 900001 iters	   0.619910   0.000000   0.619910 (  0.620500)
```

It is roughly the same. Which means you can take these numbers when building
non-Ruby projects (C, Go, Python) too.

For "comparison", here is the ouput from bcrypt (from ruby-bcrypt library which
uses a copy-paste implementation) from my Intel NUC i3 2018 brick:

```
       user     system      total        real
bcrypt with cost 6	  0.003510   0.000000   0.003510 (  0.003549)
bcrypt with cost 7	  0.006642   0.000000   0.006642 (  0.006669)
bcrypt with cost 8	  0.013120   0.000000   0.013120 (  0.013149)
bcrypt with cost 9	  0.026097   0.000000   0.026097 (  0.026154)
bcrypt with cost 10	  0.052030   0.000000   0.052030 (  0.052104)
bcrypt with cost 11	  0.103912   0.000000   0.103912 (  0.104034)
bcrypt with cost 12	  0.207882   0.000000   0.207882 (  0.208111)
bcrypt with cost 13	  0.415320   0.000000   0.415320 (  0.415777)
bcrypt with cost 14	  0.830609   0.000000   0.830609 (  0.831516)
bcrypt with cost 15	  1.660890   0.000000   1.660890 (  1.662613)
bcrypt with cost 16	  3.321980   0.000000   3.321980 (  3.325642)
bcrypt with cost 17	  6.641207   0.000000   6.641207 (  6.647944)
```

It has an exponential characteristic, 40ms is roughly cost `13` and 20ms is
cost `12`. It is still a good choice, however keep in mind that bcrypt is not
available in most Linux distributions (including Red Hat Enterprise Linux) and,
again, not approved by NIST.

I do have another brick: Apple Mac Mini M1 16GB from 2021, just wondering how
it compares to the i3 from 2018. I will not be pasting all tests because
everything was pretty much the same - Apple M1 was a tad slower in the Ruby
test. Unfortunately, Crystal is not yet available for the M1 chip.

```
       user     system      total        real
bcrypt with cost 6	  0.004288   0.000079   0.004367 (  0.004395)
bcrypt with cost 7	  0.007669   0.000018   0.007687 (  0.007686)
bcrypt with cost 8	  0.015171   0.000076   0.015247 (  0.015254)
bcrypt with cost 9	  0.030117   0.000248   0.030365 (  0.030366)
bcrypt with cost 10	  0.060343   0.000530   0.060873 (  0.060873)
bcrypt with cost 11	  0.119880   0.000926   0.120806 (  0.120805)
bcrypt with cost 12	  0.240576   0.002135   0.242711 (  0.242947)
bcrypt with cost 13	  0.478940   0.003749   0.482689 (  0.482706)
bcrypt with cost 14	  0.957543   0.007271   0.964814 (  0.964815)
bcrypt with cost 15	  1.914573   0.014784   1.929357 (  1.929367)
bcrypt with cost 16	  3.829219   0.028846   3.858065 (  3.858162)
bcrypt with cost 17	  7.669053   0.056666   7.725719 (  7.726456)
```

The Ruby script:

```
require 'benchmark'
require 'openssl'
require 'bcrypt'

asha = "bbd2a53e6feb515d644090c4fefba1c2756cc19b"

Benchmark.bm do |bench|
  (1..1000000).step(100000).each do |iters|
    bench.report("PBKDF2 SHA-1 with #{iters} iters\t") do
      OpenSSL::PKCS5.pbkdf2_hmac_sha1(asha, asha, iters, 40)
    end
  end
end

Benchmark.bm do |bench|
  (1..1000000).step(100000).each do |iters|
    bench.report("PBKDF2 SHA-256 with #{iters} iters\t") do
      OpenSSL::PKCS5.pbkdf2_hmac(asha, asha, iters, 40, OpenSSL::Digest.new("SHA256"))
    end
  end
end

Benchmark.bm do |bench|
  (1..1000000).step(100000).each do |iters|
    bench.report("PBKDF2 SHA-512 with #{iters} iters\t") do
      OpenSSL::PKCS5.pbkdf2_hmac(asha, asha, iters, 40, OpenSSL::Digest.new("SHA512"))
    end
  end
end

Benchmark.bm do |bench|
  (6..17).each do |cost|
    bench.report("bcrypt with cost #{cost}\t") do
      BCrypt::Password.create(asha, cost: cost)
    end
  end
end
```

The same script in Crystal language:

```
require "benchmark"
require "openssl"

asha = "bbd2a53e6feb515d644090c4fefba1c2756cc19b"

Benchmark.bm do |bench|
  (1..1000000).step(100000).each do |iters|
    bench.report("PBKDF2 SHA-1 with #{iters} iters\t") do
      OpenSSL::PKCS5.pbkdf2_hmac_sha1(asha, asha, iters, 40)
    end
  end
end

Benchmark.bm do |bench|
  (1..1000000).step(100000).each do |iters|
    bench.report("PBKDF2 SHA-256 with #{iters} iters\t") do
      OpenSSL::PKCS5.pbkdf2_hmac(asha, asha, iters, OpenSSL::Algorithm::SHA256, 40)
    end
  end
end

Benchmark.bm do |bench|
  (1..1000000).step(100000).each do |iters|
    bench.report("PBKDF2 SHA-512 with #{iters} iters\t") do
      OpenSSL::PKCS5.pbkdf2_hmac(asha, asha, iters, OpenSSL::Algorithm::SHA512, 40)
    end
  end
end
```

Well, there you have it. Drop me a comment on twitter @lzap and have a nice
day!

