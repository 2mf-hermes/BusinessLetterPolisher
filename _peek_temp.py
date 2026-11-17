# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.index('id="temperature"')
print(repr(s[i - 160:i + 200]))
