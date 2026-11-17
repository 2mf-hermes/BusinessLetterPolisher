# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.index('provEditBox')
print('----- markup around the block -----')
print(s[i - 1500:i + 2200].replace('\r', ''))
