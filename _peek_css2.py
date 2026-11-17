# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.index('.cs-dd{')
print(s[i:s.index('}', i) + 1].replace('\r', ''))
print('========')
j = s.index('function csPlaceMenu')
print(s[j:s.index('\n}', j) + 2].replace('\r', ''))
