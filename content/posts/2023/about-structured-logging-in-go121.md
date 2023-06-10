---
title: "About Structured Logging in Go 1.21"
date: 2023-06-10T21:38:40+02:00
type: "post"
tags:
- golang
draft: true
---

About structured logging in Go 1.21

Upcoming version of the Go programming language, which is expected to be
released in the fall of 2023, will introduce a new package named `slog`. It
provides a clean and consistent API for structured logging. Let's take a closer
look on how to use this new library.

Structured logging utilizes key-value structures for storing messages which can
be parsed, filtered and analyzed more efficiently in contrast to traditional
logging which is rather human readable and natural to write. Compare the
following:

    // Human-readable logging
    logger.Printf("user with ID %d was authenticated", user.ID)

    // Machine-readable logging
    slog.Info("user was authenticated", "user_id", user.ID)

While the former example, which uses the `log` package from the standard
library, is easier to read, it does not necessary provide a good format for
storing and searching data later. The structured logging from the latter example
provides a way of building data which can be indexed and efficiently processed.

A good analogy is syslog and journald from Linux. The former provides an API
for human-readable logging and the latter an API for structured logging. You
might be familiar with ElasticSearch project for storing and processing
structured logs in JSON format and Kibana project, a user interface for
working with ElasticSearch.

There are many structured logging libraries available in Go, `logrus`, `zap`
and `zerolog` to name few. Multiple projects providing the same capability is a
problem for logging across libraries. As someone who wrote probably a hundred
of logging facades, this is the most appealing aspect of the new package. It
provides a common API which can help a lot with integrating logging from other
libraries like SQL drivers, messaging broker libraries or cloud clients.

In order to start using slog, a new `Logger` with a `Handler` must be created.
There are two handlers available in the library: one for JSON and one for text.
Storing structured logs as text is not very useful for production use, however,
it is very nice option for development environments:

    logger := slog.New(slog.NewTextHandler(os.Stderr, nil))
    slog.SetDefault(logger)

The slog API is simple and easy to understand:

    slog.Info("user was authenticated", "user_id", user.ID)

The build-in text handler generates:

    time=2023-06-03T17:49:54.224+02:00 level=INFO msg="user was authenticated" user_id=424213

You will see me using all lowercase style for messages throughout the post, I
know there are two main camps. The rationale behind my decision is that when I
work on project which do logging with capital letter and this is not enforced
by a linter, I always see inconsistent results because errors are all lowercase
in Go (and this can be easily enforced by linters). So to make things more
simple, I do use all lowercase style on new projects.

I can imagine that figuring out logging levels for the `slog` package was a
hard task, you are probably familiar with the widely popular debug, info,
warning, error. Some libraries provide also trace level, others add fatal level
or even panic level. And there are libraries which do not provide any
human-readable levels and only work with numbers also known as verbosity
levels.

In `slog`, there are four constants: Debug (-4), Info (0), Warn (4) and Error
(8). There are some intentional gaps in case someone wants to have in-between
levels (e.g. Notice) and Level is in fact an integer so there is plenty of room
for additional levels if needed.

As you can probably see, the Info function is variadic: `Info(msg string, args
...any)` and it provides a convenient way of writing structured logs.  Simply
add zero, one or more key-value pairs or attributes, more about them later, and
types will be introspected via the `reflect` package. You see it right,
reflection is the price you pay if you want to type your logging statements
quickly. I spent my time on projects with all the three mentioned structured
logging libraries and I can say this is extremely convenient to work with.

Now, if you think this is slow, read on. There are ways how to optimize logging
when needed, the first option being the With function. It can be used when you
need to create multiple log events with same parameters:

    logger := slog.With("user_id", user.ID, "job_id", jobID)
    for _, _ := range something {
        logger.Info("doing something")
    }

In this case, the values passed via With function will be introspected only
once if handler in use correctly implements `WithAttrs` function.

If there is no other option, hot spots in the code can be written using `Attr`
type, it is a typed key-value pair which is faster to process, however,
slightly less convenient to type:

    slog.Info("user was authenticated", slog.Int("user_id", user.ID))

The logging functions (`Debug`, `Info`, `Warn` and `Error`) all support mixing
both `Attr` and key-value arguments:

	slog.Info("a test message",
		slog.Int("int", 1),
		"key", "value",
		slog.Bool("bool", true),
	)

Of course, traditional optimizations still apply here as these are normal
functions and arguments are evaluated immediately regardless of the logger
level. In these cases, `slog.Level` can be checked, a pointer can be passed
instead of value, or `slog.LogValuer` lazy-evaluator interface can be used.
The mentioned type can be also used to filter sensitive data:

    type Token string

    func (Token) LogValue() slog.Value {
        return slog.StringValue("REDACTED_TOKEN")
    }

When it comes to micro benchmarks, `slog` (via `Attr` arguments) is faster than
`logrus` and `zap` but slower than `zerolog` at the time of writing. Before you
make any conclusions I would like to make one point - most of applications
spend a fraction of resources on logging, unless there is a bug or
misconfiguration.

Because the most popular serialization format for structured logging is JSON,
there is a concept of groups to create sub-keys:

	slog.Info("user was authenticated",
		slog.Group("user",
			"id", user.ID,
			"name", user.Name,
		),
	)

The built-in text handler generates:

    time=2023-06-03T17:49:54.224+02:00 level=INFO msg="user was authenticated" user.id=424213 user.name=Andrew

The build-in JSON handler generates something like:

    {
        "time": "2023-06-03T17:49:54.224+02:00",
        "level": "INFO",
        "msg": "user was authenticated",
        "user": {
            "id": 424213,
            "name": Andrew
        }
    }

Let's take a closer look on the Record type:

    type Record struct {
        Time time.Time
        Message string
        Level Level
        PC uintptr
    }

The type is self-exemplary except the PC field which can be used in tandem
with `runtime.CallersFrames` to get file, line and function name information.
This is useful when writing your own wrappers for logging functions or custom
handlers. To get file, line and function information with the built-in text
handler, simply use `AddSource` handler option. To remove unwanted field like
time, use replace function:

    replace := func(groups []string, a slog.Attr) slog.Attr {
		if a.Key == slog.TimeKey && len(groups) == 0 {
			return slog.Attr{}
		}
		return a
	}
	logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{AddSource: true, ReplaceAttr: replace}))

Another aspect we need to take a look is context. Many logging libraries
encourages to store logger in the `context.Context`. For example zerolog
library provides `zerolog.Ctx` and `zerolog.WithContext` functions to get or
set logger respectively. While this is a valid approach and can be also applied
for this library, `slog` package also provides a way to utilize Handlers to
pull fields from context.

In the following example, a handler decorator is used to get a trace id from
context and put it as `trace_id` field into every record when available:

    type ctxTraceIdKey struct{}

    type ContextHandler struct {
        handler slog.Handler
    }

    func NewContextHandler(h slog.Handler) *ContextHandler {
        if lh, ok := h.(*ContextHandler); ok {
            h = lh.handler
        }
        return &ContextHandler{h}
    }

    func (h *ContextHandler) Enabled(ctx context.Context, level slog.Level) bool {
        return h.handler.Enabled(ctx, level)
    }

    func (h *ContextHandler) Handle(ctx context.Context, r slog.Record) error {
        if ctx == nil {
            return h.handler.Handle(ctx, r)
        }
        if tid, ok := ctx.Value(ctxTraceIdKey{}).(string); ctx ok {
            traceAttr := slog.Attr{
                Key:   "trace_id",
                Value: slog.StringValue(tid),
            }
            r.AddAttrs(traceAttr)
        }
        return h.handler.Handle(ctx, r)
    }

    func (h *ContextHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
        return NewContextHandler(h.handler.WithAttrs(attrs))
    }

    func (h *ContextHandler) WithGroup(name string) slog.Handler {
        return NewContextHandler(h.handler.WithGroup(name))
    }

Now, this might look like a lot of code, but every program typically need to
have one such handler. Then working with contexts is super easy, simply use
`Ctx` version of the logging function:

    slog.InfoCtx(ctx, "user was authenticated", "user_id", user.ID)

I personally find this easier to type instead of retrieving a `logger` variable
from the context in every single function. Assuming a trace id `42cafe13` in
the context, the built-in text handler decorated with the above handler
generates:

    time=2023-06-03T17:49:54.224+02:00 level=INFO msg="user was authenticated" user_id=424213 trace_id=42cafe13

The `slog` package provide a simple and common logging API that will be
hopefully picked up by libraries as a common standard for structured logging.
Even users who will continue using other logging libraries will benefit from
`slog` as adapters for most popular logging libraries already exist.

If you like to start using the API today, there is `golang.org/x/exp/slog` and
although "exp" stands for "experimental", the API is currently frozen for Go
1.21 and no changes are expected. You should switch to standard library after
Go 1.21 is out because that will probably not last forever.

I personally started a new application with `slog` myself as I really enjoy
variadic functions and I am willing to sacrifice few CPU cycles per request in
exchange for faster typing of logging statements.
