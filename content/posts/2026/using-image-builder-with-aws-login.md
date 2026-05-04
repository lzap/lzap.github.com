---
title: "Using Image Builder With AWS Dynamic Credentials"
date: 2026-05-04T14:05:03+02:00
type: "post"
tags:
- linux
- fedora
---

Image Builder supports uploading images to AWS through its `build` or `upload`
commands. For example:

```
image-builder upload rhel-10.1-ami-x86_64.raw \
    --to=aws \
    --aws-region=eu-central-1 \
    --aws-bucket=my-bucket \
    --aws-ami-name my-rhel
```

This works with static credentials (AWS access key ID and secret). The industry
is moving away from long-lived secrets toward dynamic credentials: short-lived
credentials obtained with a login command such as:

```bash
aws login --region eu-central-1
```

Logging in is as easy as following a link and pasting the response back into the
CLI.

`image-builder` uses the AWS SDK for Go v2, which does not support dynamic
credentials yet; they are silently ignored. That shows up as a cryptic error:

```
Getting: operation error S3: CreateMultipartUpload, get identity: get credentials: failed to refresh cached credentials, no EC2 IMDS role found, operation error ec2imds: GetMetadata, request canceled, context deadline exceeded
```

To use `image-builder` with dynamic credentials, log in to a separate
profile—say, `auth`. If you run the CLI over SSH, add `--remote` as well:

```bash
aws login --region eu-central-1 --profile auth --remote
```

That creates an entry like this in `.aws/config`:

```
[profile auth]
region = eu-central-1
login_session = arn:aws:sts::12345678910:assumed-role/12345678910-admin/lzap
```

Add another profile (or reuse `default` if you prefer) with `credential_process`
so a helper command supplies static-style credentials. For example:

```
[default]
region = eu-central-1
credential_process = aws configure export-credentials --profile auth --format process
```

With that in place, `image-builder` can use the `default` profile for the
upload, and the flow above should work.
