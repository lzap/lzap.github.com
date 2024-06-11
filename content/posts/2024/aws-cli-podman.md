---
title: "AWS CLI via Podman"
date: 2024-06-11T14:46:08+02:00
type: "post"
tags:
- linux
- fedora
---

The extensive AWS CLI is quite painful to install on Fedora or RHEL since the
API is moving so fast that is gets outdated quite quickly. Luckily, Amazon
provides containers published both on AWS and Docker registries. Configuration
is easy:

    podman run --rm -it -v ~/.aws:/root/.aws amazon/aws-cli configure

    AWS Access Key ID [****************xwcz]:
    AWS Secret Access Key [****************CAC1]:
    Default region name [None]: us-east-1
    Default output format [None]:

Note the volume mapping, the configuration of the current user is shared with
the container. If you want to keep the configuration separate, use a different
directory.

Using the CLI is straightforward enough:

    podman run --rm -it -v ~/.aws:/root/.aws amazon/aws-cli s3 ls s3://my-test-bucket--use1-ax4--x-s3/

Well, that was short.
