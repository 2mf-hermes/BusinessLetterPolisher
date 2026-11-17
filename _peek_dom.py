# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
p = os.path.join(os.environ['TEMP'], 'dom2.html')
s = open(p, encoding='utf-8', errors='replace').read()
i = s.find('probeOut')
print('probeOut idx', i, 'len', len(s))
print('--- around probeOut ---')
print(s[max(0, i - 300):i + 300])
print('--- tail 400 ---')
print(s[-400:])
