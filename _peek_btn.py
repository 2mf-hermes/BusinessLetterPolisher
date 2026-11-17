# -*- coding: utf-8 -*-
"""Show btn / btn-sm / pref-row CSS and the letter-preference toggle markup."""
import io
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = io.open('letter-polisher.html', encoding='utf-8', newline='').read()

for pat in [r'\.btn\{[^}]*\}', r'\.btn-sm\{[^}]*\}', r'\.btn-p\{[^}]*\}', r'\.btns\{[^}]*\}',
            r'\.pref-row\{[^}]*\}', r'\.ps\{[^}]*\}', r'\.sect\{[^}]*\}', r'\.custom-prompt\{[^}]*\}']:
    for m in re.finditer(pat, s):
        print(m.group(0))
print()
seg = s.split('<!-- Settings Panel -->')[1].split('<!-- Detail Modal -->')[0]
i = seg.find('letterPrefEnabled')
print('LETTER PREF MARKUP:')
print(seg[max(0, i - 700):i + 1600].replace('><', '>\n<'))
