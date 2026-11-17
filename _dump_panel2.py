# -*- coding: utf-8 -*-
"""Dump the settings-panel markup, one tag per line, for reading."""
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.find('<div class="ov" id="sOv">')
j = s.find('<div class="ov" id="updOv">', i)
t = s[i:j]
lines = t.replace('><', '>\n<').split('\n')
out = []
for n, line in enumerate(lines, 1):
    out.append('%3d| %s' % (n, line))
open('_panel.txt', 'w', encoding='utf-8', newline='').write('\n'.join(out))
print('panel chars=%d lines=%d' % (len(t), len(lines)))
