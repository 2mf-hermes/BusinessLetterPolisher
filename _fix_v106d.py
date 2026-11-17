# -*- coding: utf-8 -*-
"""v2026.10.02 part D: humane interaction details found by the audit.

1. `.btn-sm` gets a 28px minimum height - icon-less small buttons (the letter
   preference save / reset pair) were only 25px tall, below a comfortable target.
2. A visible keyboard focus ring for buttons / chips / tabs / dropdown rows /
   floating buttons; mouse clicks stay ring-free.
3. Honour `prefers-reduced-motion`.
"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
P = 'letter-polisher.html'
s = io.open(P, encoding='utf-8', newline='').read()
n = 0

old = '.btn-sm{padding:6px 14px;font-size:11px;}'
new = '.btn-sm{padding:6px 14px;font-size:11px;min-height:28px;}'
assert s.count(old) == 1, 'btn-sm rule not found'
s = s.replace(old, new, 1)
n += 1

anchor = '\r\n</style>'
assert s.count(anchor) == 1, 'style end not found'
extra = (
    '\r\n/* Keyboard focus: clearly visible for keyboard users, silent for mouse users. */\r\n'
    '.btn:focus-visible,.chip:focus-visible,.tab:focus-visible,.cs-btn:focus-visible,\r\n'
    '.cs-opt:focus-visible,.fab:focus-visible,.px:focus-visible,\r\n'
    '.pref-switch input:focus-visible,.pref-switch:focus-within{\r\n'
    '  outline:2px solid var(--ac);outline-offset:2px;\r\n'
    '}\r\n'
    '/* Respect the system "reduce motion" setting. */\r\n'
    '@media (prefers-reduced-motion:reduce){\r\n'
    '  *,*::before,*::after{\r\n'
    '    transition-duration:.01ms!important;animation-duration:.01ms!important;\r\n'
    '    animation-iteration-count:1!important;scroll-behavior:auto!important;\r\n'
    '  }\r\n'
    '}\r\n'
)
s = s.replace(anchor, extra + '</style>', 1)
n += 1

io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('v106d applied: %d edits (small-button height, focus ring, reduced motion)' % n)
