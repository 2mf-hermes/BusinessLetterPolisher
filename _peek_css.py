# -*- coding: utf-8 -*-
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.index('.cs-dd{')
print(s[i:i + 400].replace('\r', ''))
print('---- keyframes ----')
for m in re.finditer(r'@keyframes\s+(\w+)\s*\{.{0,200}', s, re.S):
    if 'cs' in m.group(1).lower() or 'dy' in m.group(1).lower():
        print(m.group(0).replace('\r', '').replace('\n', ' ')[:220])
print('---- ids ----')
for m in re.finditer(r'id="(prov[A-Za-z]*|model[A-Za-z]*)"', s):
    print(m.group(1))
