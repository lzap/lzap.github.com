---
type: "post"
aliases:
- /2021/11/swap-y-and-z-keys-on-us-keyboard-in-macos.html
date: "2021-11-29T00:00:00Z"
tags:
- macos
title: Swap Y and Z keys on US keyboard in MacOS
---

I work most of my day-to-day time on MacOS these days and one thing I am
struggling with is slightly different keyboard layout when it comes to dead
keys (AltGr combinations). I use Czech keyboard layout for most of my career
even for programming. These combinations are different on MacOS. I am able to
probably learn back to US keyboard layout, as I was using it previously and it
should not be a problem. Since almost all my text typing is in English anyway,
there are some advantages to that like havin' single quote much more
accessible.

One thing, however, I cannot work with is Y and Z keys swapped. See, Czech
layout uses QWERTZ whereas on US layout it's QWERTY. Problem can be easily
solved, I setup both US and Czech QWERTY layouts in the operating system and
then I can swap those two keys on the hardware (USB) level. It is as easy as
**running the following command in the Terminal**:

    hidutil property --set '{"UserKeyMapping": [{"HIDKeyboardModifierMappingSrc":0x70000001D, "HIDKeyboardModifierMappingDst":0x70000001C},{"HIDKeyboardModifierMappingSrc":0x70000001C, "HIDKeyboardModifierMappingDst":0x70000001D}]}'

Keep in mind that the keys are swapped on the hardware level, so if you use
other keyboard layouts which have both QWERTZ and QWERTY, you might get into
issues with keys being swapped in the other layout. If you use just a single
layout or all your layouts are the same QWERTX type, it's not an issue at all.
**To revert this swap back at any point**, just do the following command:

    hidutil property --set '{"UserKeyMapping": [{}]}'

To make this change permanent, make sure the first command is executed after
MacOS startup.  One way to do that would be something like:

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
          <string>{"UserKeyMapping": [{"HIDKeyboardModifierMappingSrc":0x70000001D, "HIDKeyboardModifierMappingDst":0x70000001C},{"HIDKeyboardModifierMappingSrc":0x70000001C, "HIDKeyboardModifierMappingDst":0x70000001D}]}</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>KeepAlive</key>
        <false/>
      </dict>
    </plist>
    EOF
    sudo launchctl load -w /Library/LaunchDaemons/org.custom.keyboard-remap.plist

That's all for now!

