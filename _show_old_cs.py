# -*- coding: utf-8 -*-
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = subprocess.run(['git', 'show', '42c6295^:letter-polisher.html'],
                   capture_output=True, encoding='utf-8').stdout
i = s.find('function csToggle')
print('--- BEFORE (42c6295^) ---')
print(s[i - 800:i + 700])
j = s.find('function csPlaceMenu')
print('--- csPlaceMenu exists before?', j)
