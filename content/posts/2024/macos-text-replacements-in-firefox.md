---
title: "MacOS Text Replacements in Firefox"
date: 2024-10-10T09:33:07+02:00
type: "post"
tags:
- macos
---

I use MacOS built-in text replacement feature a ton, however, after I started using Firefox recently I quickly found out that it does not work. The feature is disabled in `about:config` via setting named `widget.macos.automatic.text_replacement`, but even if you enable it it only works for `textarea` and not for widely used `input` element. And there is no solution so far.

Well, there is a workaround by using [TextFast extension](https://addons.mozilla.org/en-US/firefox/addon/textfast/) that does exactly what it is supposed to do. It is a tiny open-source extension and quick look does not show any network activity except optional storing of the list to Firefox Account (disabled by default). And it has a JSON-based importing / exporting capability.

Luckily, all MacOS replacements can be saved to `plist` file by selecting them all and dragging them into a folder. So in order to do that, open `Downloads` folder, MacOS settings - Keyboard - Replacements, select them all and drag it to the folder. Then type this in a terminal:

```
cd $HOME/Downloads

cat >convert.py <<EOF
#!/usr/bin/python3
import plistlib
import json
out = []
with open(0, 'rb') as stdin:
    for pair in plistlib.load(stdin):
        n = {}
        n["replace"] = pair["shortcut"]
        n["with"] = pair["phrase"]
        out.append(n)
print(json.dumps(out))
EOF

/usr/bin/python3 convert.py < "Text Substitutions.plist" > "Text Substitutions.json"
```

The first command changes the working directory to Downloads folder where text substitutions were dragged resulting into `Text Substitutions.plist` file being created. The second command creates a short script that converts `plist` into `json`. And the third command executes the script creating a new file named `Text Substitutions.json`.

Warning: Depending on your language, the file might be named differently. For example, in my Czech locale the file will be `Textové záměny.plist`. Change the third command accordingly.

Now, open up the extension and use Import JSON feature to import your replacements. Done!

Here is my replacement list just as an example (and backup for myself). In case you are wondering, I use this feature to type English via my Czech keyboard layout which has the `'` key hardly accessible via a dead-key combination:

```
[
  {
    "replace": "aintt",
    "with": "ain't"
  },
  {
    "replace": "arentt",
    "with": "aren't"
  },
  {
    "replace": "cantt",
    "with": "can't"
  },
  {
    "replace": "couldntt",
    "with": "couldn't"
  },
  {
    "replace": "couldvee",
    "with": "could've"
  },
  {
    "replace": "didntt",
    "with": "didn't"
  },
  {
    "replace": "doesntt",
    "with": "doesn't"
  },
  {
    "replace": "dontt",
    "with": "don't"
  },
  {
    "replace": "hadntt",
    "with": "hadn't"
  },
  {
    "replace": "hadvee",
    "with": "had've"
  },
  {
    "replace": "hasntt",
    "with": "hasn't"
  },
  {
    "replace": "haventt",
    "with": "haven't"
  },
  {
    "replace": "hedd",
    "with": "he'd"
  },
  {
    "replace": "helll",
    "with": "he'll"
  },
  {
    "replace": "heress",
    "with": "here's"
  },
  {
    "replace": "hess",
    "with": "he's"
  },
  {
    "replace": "howss",
    "with": "how's"
  },
  {
    "replace": "Idd",
    "with": "I'd"
  },
  {
    "replace": "Illl",
    "with": "I'll"
  },
  {
    "replace": "Imm",
    "with": "I'm"
  },
  {
    "replace": "isntt",
    "with": "isn't"
  },
  {
    "replace": "itdd",
    "with": "it'd"
  },
  {
    "replace": "itlll",
    "with": "it'll"
  },
  {
    "replace": "itss",
    "with": "it's"
  },
  {
    "replace": "Ivee",
    "with": "I've"
  },
  {
    "replace": "letss",
    "with": "let's"
  },
  {
    "replace": "njn",
    "with": "No jo no."
  },
  {
    "replace": "shedd",
    "with": "she'd"
  },
  {
    "replace": "shelll",
    "with": "she'll"
  },
  {
    "replace": "shess",
    "with": "she's"
  },
  {
    "replace": "shouldntt",
    "with": "shouldn't"
  },
  {
    "replace": "somebodyss",
    "with": "somebody's"
  },
  {
    "replace": "someoness",
    "with": "someone's"
  },
  {
    "replace": "somethingss",
    "with": "something's"
  },
  {
    "replace": "thatdd",
    "with": "that'd"
  },
  {
    "replace": "thatlll",
    "with": "that'll"
  },
  {
    "replace": "thatss",
    "with": "that's"
  },
  {
    "replace": "theydd",
    "with": "they'd"
  },
  {
    "replace": "theylll",
    "with": "they'll"
  },
  {
    "replace": "theyree",
    "with": "they're"
  },
  {
    "replace": "wasntt",
    "with": "wasn't"
  },
  {
    "replace": "welll",
    "with": "we'll"
  },
  {
    "replace": "weree",
    "with": "we're"
  },
  {
    "replace": "werentt",
    "with": "weren't"
  },
  {
    "replace": "whatss",
    "with": "what's"
  },
  {
    "replace": "wheress",
    "with": "where's"
  },
  {
    "replace": "whyss",
    "with": "why's"
  },
  {
    "replace": "youdd",
    "with": "you'd"
  },
  {
    "replace": "youlll",
    "with": "you'll"
  },
  {
    "replace": "youree",
    "with": "you're"
  },
  {
    "replace": "youvee",
    "with": "you've"
  }
]
```
