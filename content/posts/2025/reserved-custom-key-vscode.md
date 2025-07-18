---
title: "Reserved Custom Keyboard Key in VSCode"
date: 2025-07-18T10:37:35+02:00
type: "post"
tags:
- macos
- linux
- vscode
---

While my primary editor is, and always will be, Vim, I find myself using VS Code more and more for longer editing sessions on larger projects. With its great Go support, decent (though not ideal) refactoring tools, and Copilot, it's an excellent tool.

Recently, I was exploring its Git capabilities and realized there are no default shortcuts for important actions like git commit or git push. Users are expected to perform these tasks using the mouse in the Source Control view, which is quite limited for editing commit messages; for example, it lacks automatic text wrapping.

This led me to look for a key combination reserved for custom user shortcuts. In Vim, there are several such keys, and the editor has a special concept known as the _local leader_ key for this exact purpose. In my configuration, I have it set to the comma key `,`.

However, VS Code doesn't have such a concept. The most commonly recommended combination is `Ctrl+;`, but this is difficult to reach on my Czech keyboard layout.

Therefore, I settled on a solution: I changed the shortcut for opening preferences from `Ctrl+` (`Cmd+,` on Mac) to a chord `Ctrl+, ,` (`Cmd+, ,`). This freed up the easy-to-reach `Ctrl+,` combination for my own custom chords, and it works flawlessly. What I particularly like about this setup is that I can now use the same key combinations in VS Code that I'm used to from Vim with my local leader key!

Using the comma for custom shortcuts is a well-known practice pioneered by [Pavel Satrapa](https://www.nti.tul.cz/~satrapa/docs/vim/). I set this up back in 1998 and have never looked back.
