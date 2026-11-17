# -*- coding: utf-8 -*-
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
for m in re.finditer(r'provCS|provDD', s):
    i = m.start()
    print('---', m.group(0), 'at', i)
    print(s[max(0, i - 260):i + 260].replace('><', '>\n<'))
