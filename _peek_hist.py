# -*- coding: utf-8 -*-
"""Show the raw markup of the history panel and the save/test buttons."""
import io
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = io.open('letter-polisher.html', encoding='utf-8', newline='').read()

seg = s.split('<!-- History Panel -->')[1].split('<!-- Settings Panel -->')[0]
print('== HISTORY PANEL ==')
print(seg.strip()[:1200])
print()

sseg = s.split('<!-- Settings Panel -->')[1].split('<!-- Detail Modal -->')[0]
for m in re.finditer(r'<button[^>]*>', sseg):
    tag = m.group(0)
    if 'saveCfg' in tag or 'testConn' in tag or 'newProvider' in tag or 'deleteProvider' in tag or 'editProvider' in tag:
        print('BUTTON:', tag)
        print('   context:', sseg[max(0, m.start() - 220):m.start()].replace('\n', ' ')[-220:])
        print()
