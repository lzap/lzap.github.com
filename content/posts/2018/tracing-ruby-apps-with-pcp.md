---
type: "post"
aliases:
- /2018/03/tracing-ruby-apps-with-pcp.html
date: "2018-03-21T00:00:00Z"
tags:
- linux
- fedora
- pcp
title: Tracing Ruby apps with PCP
---

PCP offers two APIs for instrumented applications. The first one to mention is MMV agent which uses memory mapped files for capturing high-resolution data with minimum performance impact. Currently available languages for MMV instrumentation include C/C++, Python and Perl plus native Java,Golang and Rust ports. A second agent and approach is called PMDA trace with its higher level API. It uses TCP sockets and a simple API for capturing time spent, counters, trace points and raw value observations.

The tracing API is not ideal for measuring time spent in processing web requests, but it can still be useful for tracing things like cron jobs. The API (C, Fortran and Java) is described in pmdatrace(3) man page and it is trivial, therefore I decided to create a simple Ruby wrapper which only took one evening. The wrapper offers one-to-one mapping of all functions in Ruby and also higher-level Ruby approach with blocks and more user-friendly method naming.

The first step is to install trace PMDA (agent) and pcptrace rubygem (RPM not yet available, include files and compiler required to build the rubygem). Make sure that firewall is not blocking TCP port 4323 on localhost which is used to send data from the application. Also when using SELinux the pmcd daemon will be blocked from binding, therefore it is necessary to enable boolean flag:

    setsebool -P pcp_bind_all_unreserved_ports 1

Then install and configure necessary software:

    yum -y install pcp-pmda-trace pcp-devel @development-tools
    cd /var/lib/pcp/pmdas/trace
    ./Install
    gem install pcptrace

Use pcp_pmcd_selinux(8) man page for more details about SELinux booleans for PCP. If you encounter any SELinux problem with PCP, please let the PCP maintainers know as they will fix it promptly (pcp-team@redhat.com, or open a bugzilla).  Alternatively, the workaround is to put PCP daemons into permissive mode keeping the rest of the system confined:

    semanage permissive -a pcp_pmcd_t

Using the trace API is fairly straightforward, each function returns a status code (integer), if non-zero function pmtraceerrstr can be used to find error message if needed:

    cat ruby_trace_example.rb
    #!/usr/bin/env ruby

    require "pcptrace"

    # reached a point in source code
    PCPTrace::point("a_point")

    # observation of an arbitrary value
    PCPTrace::obs("an_observation", 130.513)

    # a counter - increasing or decreasing
    PCPTrace::counter("a_counter", 1)

    # time spent in a transaction (or block)
    PCPTrace::begin("a_transaction")
    # ...
    PCPTrace::end("a_transaction")

    # transactions must be aborted (e.g. exception)
    #PCPTrace::abort("a_transaction")

    # all methods return non-zero code
    result = PCPTrace::counter("a_counter", -5))
    puts("Error: " + PCPTrace::errstr(result)) if result != 0

There is also more Ruby-friendly API available, see README file for more info: https://github.com/lzap/ruby-pcptrace

Tracing metrics are available in trace namespace:

    pminfo trace

The trace agent uses a rolling window technique to calculate rate, total, average, min and max values for some metrics, which is very useful feature for tracing durations. By default the average is recomputed every five seconds for a period covering the prior 60 seconds. To see trace counts converted to count per second:

    pmval trace.point.count

PCP also provides rate for each individual metric, let's view that with three digits precision:

    pmval -f3 trace.point.rate

Execute similar commands or use other tools like pmchart to see values for counter or observation (trace.observe.value, trace.counter.value) or to see count and rate (trace.transact.count, trace.transact.rate).

Transaction metrics (time spent) provide total_time value (trace.transact.total_time) but also ave_time, min_time and max_time aggregated values. These are quite handy for ad-hoc troubleshooting.

There is also a helper utility pmtrace for emitting tracing events from scripts like cron jobs. Although the trace API is limited and multiple syscalls are being made every measurement, it is a good starting point to go further.

