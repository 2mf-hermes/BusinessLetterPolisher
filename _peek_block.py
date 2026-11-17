# -*- coding: utf-8 -*-
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
for pat in [r'\.prov-edit[^{]*\{[^}]*\}', r'\.pe-h[^{]*\{[^}]*\}', r'\.prov-cur[^{]*\{[^}]*\}']:
    for m in re.finditer(pat, s):
        print(m.group(0).replace('\r', '').replace('\n', ' '))
print('==== JS ====')
for name in ['openProviderEdit', 'function editProvider', 'function newProvider', 'function cancelProviderEdit',
             'function saveProviderEdit', 'function provBox']:
    i = s.find(name)
    if i < 0:
        print('-- %s: not found' % name)
        continue
    j = s.index('\n', s.index('{', i))
    j2 = s.index('\n}', i)
    print('---- %s ----' % name)
    print(s[i:j2 + 2].replace('\r', ''))
