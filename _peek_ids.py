# -*- coding: utf-8 -*-
"""Peek at ids / data-i / inline handlers inside a marked region of the app."""
import io
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = io.open('letter-polisher.html', encoding='utf-8', newline='').read()

for a, b, name in [('<!-- Settings Panel -->', '<!-- Detail Modal -->', 'SETTINGS'),
                   ('<!-- History Panel -->', '<!-- Settings Panel -->', 'HISTORY'),
                   ('<!-- Output Card -->', '<!-- FABs -->', 'OUTPUT'),
                   ('<!-- Input Card -->', '<!-- Output Card -->', 'INPUT')]:
    if a not in s:
        continue
    seg = s.split(a)[1].split(b)[0]
    ids = re.findall(r'id="([^"]+)"', seg)
    di = re.findall(r'data-i="([^"]+)"', seg)
    oc = re.findall(r'onclick="([^"(]+)', seg)
    print('== %s (%d chars)' % (name, len(seg)))
    print('ids     :', ', '.join(ids))
    print('data-i  :', ', '.join(di))
    print('onclick :', ', '.join(sorted(set(oc))))
    print()
