---
type: "post"
aliases:
- /2022/11/why-mastodon-instances-are-difficult-to-scale.html
date: "2022-11-10T00:00:00Z"
tags:
- linux
- fedora
- mastodon
title: Why Mastodon instances are difficult to scale
---

Mastodon, the free, open-source social network server based on ActivityPub is
written in Ruby on Rails and the network is experiencing influx of new users.
Mastodon administrators are finding how difficult and costly is to scale Ruby
on Rails applications the hard way. I've spent a deacde working on a large Ruby
on Rails project, much larger than Mastodon. Let me quickly describe what is
going on. Disclaimer: This post is solely based on my experience with scaling
other Ruby on Rails applications, take this with a grain of salt. Also, I'd
appreciate comments at `@lukas@zapletalovi.com`.

People often think that Ruby on Rails is slow because Ruby is slow, according
to various [benchmarks](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html)
and [shootouts](https://programming-language-benchmarks.vercel.app). Well,
while Ruby is not fast at all, it is not the primary reason why that is. See,
most web applications, including Mastodon, do not perform CPU-intensive
tasks. Most of the time, CPU is actually waiting for data to be read or
written from network (client, database, redis) or disk (cache). Even if you
upgrade to the most recent Ruby 3.2, which is the fastest of all Ruby
versions, it won't help at all.

Backend software these days need to respond to many of HTTP requests, when a
service is under load we are speaking about hundreds or even thousands of
requests per second. A single process (instance of software running on an
operating system) with naive implementation can handle as much as one request.
To be able to handle more, requests must be dealt concurrently, which is a very
complex topic but let's keep in simple. The solution is to create multiple
execution threads that can run concurrently on the program level and ideally in
parallel on the operating system level to utilize as much CPU resources
available.

There is a little problem in Ruby (and Python and many other interpreted
languages) called "global interpreter lock", also known as
[GIL](https://en.wikipedia.org/wiki/Global_interpreter_lock) which limits the
amount of parallelism reachable through concurrency of a single interpreter
process with multiple threads. In short, while GIL allows some parallelism when
threads are waiting for I/O (input and output, e.g. writing data into database)
in theory, in practice it does not scale. Most applications have the sweet spot
of 5-15 threads per process when the most performance can be achieved. This
highly depends on the hardware or virtual machine (CPU type, number of cores,
hyper-threading).

Don't be mistaken that other languages do not have this problem, even server
software written in C (e.g. Apache httpd 2.x) is known to have scalability
issues with many threads. For example the ThreadsPerChild Apache setting is set
to 64 by default (25 on Windows, whoops). But performance is not the only
concern, isolation and security is also at stake here.

Mastodon, like many other Ruby on Rails applications, needs to schedule
backround tasks. The backend API communicates with some kind of job scheduler
through ActiveJob API and one or more backend worker instances pick the tasks
and perform the work (e.g. delivering emails, updating database). The same
problem applies - one worker process can effectively run only the mentioned
5-15 threads, but there can be thousands of jobs in the queue.

What to do? It is farily simple. You spawn multiple processes which are simply
"copies" of the main process doing the same work. This is what Apache httpd
does too, so it can't be wrong. So roughly speaking, 10 processes can handle
150 tasks concurrently. That is a decent number, is it?. Well, there's a snag.

Ruby and Ruby on Rails specifically are not light on memory. Ruby itself
suffers from memory fragmentation problem, another complex topic but in short:
when Ruby allocates a memory, it is quite unlikely to ever return it back. And
Ruby on Rails is designed to be rather memory hungry, particularly its
ActiveRecord DAO API. One process of the application I have experience with
consumes 300 MB after start, and then it grew up to 500 MB during operation as
other parts of the app load up. Mastodon is not as big, but we are speaking
about hundreds of MBs per process after hours of operation. There is a way to
workaround the memory problem on some operating systems and that is copy on
write concept, but in practice that does only help a little after application
is started.

And that is only ideal state. Programmers are humans, they make mistakes and
one very common mistake is a memory leak. These memory leaks together with Ruby
fragmentation makes process memory consumption to steadily grow up until the
point that the process must be restarted. Most Ruby applications servers do
have some kind of memory limiter feature which triggers automatic restart of
the process when a threshold is reached.

Once a hardware or a VM runs out of memory, the OS starts
[swapping](https://en.wikipedia.org/wiki/Memory_paging#Terminology) that starts
killing the whole instance and everything is getting slower up to the point
that the application is unusable.

Now, Ruby has multiple implementations. The one that Mastodon runs on is called
CRuby and it has all of these problems I described in my post. There is also
JRuby, a JVM-based Ruby implementation which is substationally faster and does
not suffer from GIL. But there are drawbacks: it is not compatible with Ruby on
Rails and while some older versions of RoR can run on JRuby, most applications
won't due to bugs in dependencies which are only tested against CRuby. Also,
JRuby is even more memory hungry than CRuby from my experience.

So there you have it: Ruby on Rails requires multiple processes as the
application grow, these processes require substantial amount of memory which
only grow with time. Memory is a precious resource, so Mastodon instances can
burn a lot of money along the way. Be prepared for this!

Wait a moment, you just said that Ruby and Ruby on Rails sucks! That is totally
not what I mean. This is a wonderful platform that enables millions of people
to rapidly develop web applications and operate them, many major sites are
written in Ruby on Rails including github.com and even twitter.com started as a
RoR app. And there's hey.com and basecamp.com and they all run buttery smooth.
Like everything in life, it has some highlights and drawbacks. And the major
drawback of Ruby on Rails is that it is not easy to operate at all.

