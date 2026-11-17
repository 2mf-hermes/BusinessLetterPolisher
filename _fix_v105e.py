# -*- coding: utf-8 -*-
"""Give the 修改 button a visible active state (`.btn.on`) so an open
connection block is obvious, matching the `.chip.on` accent styling."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8', newline='')
p = 'letter-polisher.html'
raw = io.open(p, encoding='utf-8', newline='').read()

anchor = '.btn-sm{padding:6px 14px;font-size:11px;}'
assert raw.count(anchor) == 1, raw.count(anchor)
add = anchor + '\r\n' + '.btn.on{background:rgba(var(--ac-rg),.12);border-color:rgba(var(--ac-rg),.3);color:var(--ac);}'
raw = raw.replace(anchor, add, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(raw)
print('ok .btn.on active state added')
