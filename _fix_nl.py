# -*- coding: utf-8 -*-
"""Normalise line endings: every line except a trailing final one must end with CRLF."""
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
P = 'letter-polisher.html'
s = io.open(P, encoding='utf-8', newline='').read()
lines = s.split('\n')
fixed = 0
for i in range(len(lines) - 1):
    if not lines[i].endswith('\r'):
        lines[i] += '\r'
        fixed += 1
out = '\n'.join(lines)
io.open(P, 'w', encoding='utf-8', newline='').write(out)
print('lines fixed:', fixed)
chk = io.open(P, encoding='utf-8', newline='').read()
print('LF-only lines now:', chk.count('\n') - chk.count('\r\n'))
