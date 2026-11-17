# -*- coding: utf-8 -*-
"""Print a slice of letter-polisher.html around a marker, with CR stripped."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')

marker = sys.argv[1]
length = int(sys.argv[2]) if len(sys.argv) > 2 else 900

s = io.open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.find(marker)
if i < 0:
    print('!! marker not found:', marker)
    sys.exit(2)
print(s[i:i + length].replace('\r', ''))
print('---- flags ----')
for name in ['function splitResult', 'function cleanResult', 'function cleanSuggestions', 'var outRule',
             'OUTPUT RULES', 'LEAD_RE', 'esc(sug)']:
    print('%-28s %s' % (name, name in s))
