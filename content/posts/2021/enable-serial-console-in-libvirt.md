---
type: "post"
aliases:
- /2021/03/enable-serial-console-in-libvirt.html
date: "2021-03-31T00:00:00Z"
tags:
- linux
- fedora
- rhel
title: Enable serial console for libvirt
---

QEMU/KVM libvirt virtual machine can be acessed via serial console. When a new
VM is created, serial console device is created. However to fully utilize this,
several steps are needed on the guest machine.

The first option is to start getty service on serial console to get a login
prompt when system finishes booting. This is as easy as:

    # systemctl enable --now serial-getty@ttyS0.service

To access serial console via libvirt command line do:

    # virsh console virtual_machine_name

This approach is simple enough, but when something goes wrong and VM does not
boot, it is not possible to access the VM during early boot or even bootloader.
In that case, perform the additional configuration:

    # grep console /etc/default/grub
    GRUB_TERMINAL_INPUT="console serial"
    GRUB_TERMINAL_OUTPUT="console serial"
    GRUB_CMDLINE_LINUX="... console=ttyS0"

Then write new grub configuration, for EFI systems do the following:

    # grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg

For BIOS systems do:

    # grub2-mkconfig -o /boot/grub2/grub.cfg

Reboot and connect early to access grub or to see early boot messages. These
commands will work on Fedora, CentOS, Red Hat Enterprise Linux and clones.
