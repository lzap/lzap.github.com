---
type: "post"
aliases:
- /2021/04/remap-us-key-next-to-enter-to-enter-in-macos.html
date: "2021-04-19T00:00:00Z"
tags:
- macos
title: Remap US key next to enter to enter in MacOS
---

The Czech keyboard layout on a physical US Mac keyboard has some keys which are
pretty much useless. For example the key `|` aka `\` next to the enter is
actually also available on tilde key next to left shift in Czech layout and
since I am used to wide enter key I end up pressing it when I want to hit
enter. It renders to a weird "double tilde" character which I never use anyway.
Well, an easy help. This can be remapped pretty easily:

    hidutil property --set '{"UserKeyMapping":
        [{"HIDKeyboardModifierMappingSrc":0x700000031,
          "HIDKeyboardModifierMappingDst":0x700000058}]
    }'

That's all, really. No need to restart anything, but to do this after each boot
a property list for launcher must be created. Here it is:

    cat << EOF | sudo tee -a /Library/LaunchDaemons/org.custom.keyboard-remap.plist
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
      <dict>
        <key>Label</key>
        <string>org.custom.keyboard-remap</string>
        <key>ProgramArguments</key>
        <array>
          <string>/usr/bin/hidutil</string>
          <string>property</string>
          <string>--set</string>
          <string>{"UserKeyMapping": [{"HIDKeyboardModifierMappingSrc":0x700000031, "HIDKeyboardModifierMappingDst":0x700000058}] }</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>KeepAlive</key>
        <false/>
      </dict>
    </plist>
    EOF
    sudo launchctl load -w /Library/LaunchDaemons/org.custom.keyboard-remap.plist

Worry do not, this is still a Linux blog. I just ended up using MacOS on
desktop a bit more lately, I still run Linux remote shells :-)
