# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.index('var T=')
print(repr(s[i:i + 700]))
print('...')
j = s.index('provDetails')
print(repr(s[j - 300:j + 300]))
