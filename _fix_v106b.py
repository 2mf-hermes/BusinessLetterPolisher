# -*- coding: utf-8 -*-
"""v2026.10.02 part B: make DOM order match the visual order of the options grid.

Before: DOM = 信件語言, 潤飾風格, 自訂風格, 信件用途, 自訂用途, 潤飾模式, 結果顯示語言, 來源地區, 結果地區
        visual (via CSS order) = 信件語言 | 結果顯示語言 / 來源地區 | 結果地區 / 潤飾風格 | 潤飾模式 / 信件用途 ...
After:  DOM == visual: 信件語言 | 結果顯示語言 / 來源地區 | 結果地區 / 潤飾風格 | 潤飾模式 /
        自訂風格(full) / 信件用途(full) / 自訂用途(full)
=> tab order, screen-reader order and reading order agree, and the full-width custom
   panel sits directly under the tone row instead of carving a hole in the grid.
"""
import io
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
P = 'letter-polisher.html'
s = io.open(P, encoding='utf-8', newline='').read()
lines = s.split('\n')

gs = None
for i, ln in enumerate(lines):
    if '<div class="opts-grid">' in ln:
        gs = i
        break
assert gs is not None, 'opts-grid not found'
ge = None
for j in range(gs + 1, len(lines)):
    if lines[j].rstrip('\r') == '    </div>':
        ge = j
        break
assert ge is not None, 'opts-grid close not found'

inner = lines[gs + 1:ge]

# --- split the grid body into (comment, block) items ---
items = []
k = 0
pending_comment = None
while k < len(inner):
    ln = inner[k].strip()
    if ln.startswith('<!--') and ln.endswith('-->'):
        pending_comment = inner[k]
        k += 1
        continue
    if ln.startswith('<div class="fg">'):
        end = k
        while inner[end].rstrip('\r') != '      </div>':
            end += 1
        items.append([pending_comment, inner[k:end + 1]])
        k = end + 1
        pending_comment = None
        continue
    if ln.startswith('<div class="cust" id='):
        items.append([pending_comment, [inner[k]]])
        k += 1
        pending_comment = None
        continue
    raise SystemExit('unexpected grid line: ' + repr(inner[k]))

def key_of(block):
    txt = '\n'.join(block)
    for cid in ['letterLangCS', 'outLangCS', 'srcRegionCS', 'outRegionCS', 'toneCS',
                'polishModeCS', 'purposeCS', 'custTone', 'custPurp']:
        if 'id="%s"' % cid in txt:
            return cid
    raise SystemExit('no id in block')

by_key = {}
for c, b in items:
    by_key[key_of(b)] = (c, b)
assert len(by_key) == 9, 'expected 9 blocks, got %d' % len(by_key)

order = ['letterLangCS', 'outLangCS', 'srcRegionCS', 'outRegionCS',
         'toneCS', 'polishModeCS', 'custTone', 'purposeCS', 'custPurp']
comments = {
    'letterLangCS': '<!-- Row 1, Col 1: letter language -->',
    'outLangCS':    '<!-- Row 1, Col 2: result language -->',
    'srcRegionCS':  '<!-- Row 2, Col 1: source region -->',
    'outRegionCS':  '<!-- Row 2, Col 2: result region -->',
    'toneCS':       '<!-- Row 3, Col 1: polishing style -->',
    'polishModeCS': '<!-- Row 3, Col 2: polishing mode -->',
    'custTone':     '<!-- Custom style input: opens right under the style selector -->',
    'purposeCS':    '<!-- Row 4 (full width): purpose -->',
    'custPurp':     '<!-- Custom purpose input: opens right under the purpose selector -->',
}

new_inner = []
for k2 in order:
    new_inner.append('      ' + comments[k2])
    new_inner.extend(by_key[k2][1])

s2 = '\n'.join(lines[:gs + 1] + new_inner + lines[ge:])
assert s2 != s

# --- CSS order values now mirror the DOM order (kept explicit + for the窄版 override) ---
old_css = ('.opts-grid>.fg:has(#toneCS){order:5;}\r\n'
           '.opts-grid>#custTone{order:6;}\r\n'
           '.opts-grid>.fg:has(#polishModeCS){order:7;}\r\n'
           '.opts-grid>.fg:has(#purposeCS){order:8;grid-column:1/-1;}\r\n'
           '.opts-grid>#custPurp{order:9;}')
new_css = ('.opts-grid>.fg:has(#toneCS){order:5;}\r\n'
           '.opts-grid>.fg:has(#polishModeCS){order:6;}\r\n'
           '.opts-grid>#custTone{order:7;}\r\n'
           '.opts-grid>.fg:has(#purposeCS){order:8;grid-column:1/-1;}\r\n'
           '.opts-grid>#custPurp{order:9;}')
assert s2.count(old_css) == 1, 'css order block not found'
s2 = s2.replace(old_css, new_css, 1)

io.open(P, 'w', encoding='utf-8', newline='').write(s2)
print('v106b applied: DOM order now matches visual order')
print('grid blocks (DOM order): ' + ', '.join(order))
