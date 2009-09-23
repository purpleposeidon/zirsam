#!/usr/bin/python3.0
# -*- coding: utf-8 -*-

"""
If you want a general understanding of how this program works, look at common.py
"""

TODO = """
Released under GPLv3. I reserve the right to change this at any time or permit others to use it under other licenses, unless that's illegal, in which case this sentence does not apply.
Contact: purpleposedon@gmail.com

At some point I'll make this the entry point program.
Technically, run "morphology.py" or "orthography.py". I'm going to run morphology because that's what you're probably interested in. I would like to point out that I also accept command line arguments. See "morphology.py --help". I'm also certainly full of bugs!

Now, start typing lo jbobau. It returns each word (except for the most recent) as it recieves it. Terminate input with Ctrl-D (on *nix, probably Ctrl-Z under the foul domain of the winblowzer)

"""
print(TODO)

import morphology
morphology.main()
#raise SystemExit(TODO)
