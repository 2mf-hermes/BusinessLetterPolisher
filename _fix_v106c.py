# -*- coding: utf-8 -*-
"""v2026.10.02 part C: one column keeps the DOM order, so tab order == reading order."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
P = 'letter-polisher.html'
s = io.open(P, encoding='utf-8', newline='').read()

old = ('@media(max-width:520px){\r\n'
       '  .opts-grid{grid-template-columns:1fr;gap:10px;}\r\n'
       '  .opts-grid>.fg:has(#purposeCS){grid-column:1;}\r\n'
       '  /* single column: keep each region right under its own language */\r\n'
       '  .opts-grid>.fg:has(#srcRegionCS){order:2;}\r\n'
       '  .opts-grid>.fg:has(#outLangCS){order:3;}\r\n'
       '  .opts-grid>.fg:has(#outRegionCS){order:4;}\r\n'
       '}')
new = ('@media(max-width:520px){\r\n'
       '  .opts-grid{grid-template-columns:1fr;gap:10px;}\r\n'
       '  /* One column: the DOM order already reads top to bottom, so nothing is\r\n'
       '     reordered - the tab order stays identical to the reading order. */\r\n'
       '}')
assert s.count(old) == 1, 'media query block not found'
s = s.replace(old, new, 1)
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('v106c applied: narrow layout no longer reorders fields')
