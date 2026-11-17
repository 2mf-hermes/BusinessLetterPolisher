# -*- coding: utf-8 -*-
"""Print the raw context around every 'provDeleted:' occurrence."""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
for m in re.finditer(r"provDeleted:'((?:[^'\\]|\\.)*)'", s):
    line = s[:m.start()].count('\n') + 1
    head = s.rfind('\n', 0, m.start() - 900)
    seg = s[max(0, m.start() - 700):m.end() + 40]
    print('=== line %d ===' % line)
    print('anchor: %r' % m.group(0))
    print('preview:', seg[-380:].replace('\r', ''))
    print()
