# -*- coding: utf-8 -*-
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
start = s.index('var T={')
block = s[start:s.index('\n};', start)]
names = [m.group(1) for m in re.finditer(r"(?m)^\s*'([^']+)'\s*:\s*\{", block)]
pos = [m.start() for m in re.finditer(r"(?m)^\s*'([^']+)'\s*:\s*\{", block)]
want = ['provEdit', 'provDetails', 'provSave', 'provCancel', 'provSaved', 'provNew', 'provDel',
        'provCur', 'apiKeyEye', 'temperature', 'modelName', 'aiProvider']
for idx, nm in enumerate(names):
    seg = block[pos[idx]:(pos[idx + 1] if idx + 1 < len(names) else len(block))]
    print('==', nm)
    for k in want:
        m = re.search(r"(?<![\w'])" + k + r"\s*:\s*'([^']*)'", seg)
        print('   %-12s %s' % (k, m.group(1) if m else '<MISSING>'))
