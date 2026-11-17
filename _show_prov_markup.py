# -*- coding: utf-8 -*-
import re, io, sys
sys.stdout.reconfigure(encoding='utf-8')
p = 'letter-polisher.html'
d = open(p, encoding='utf-8').read()

keys = ['loadModelsBtn', 'provName', 'id="provider"', "id='provider'", 'provCS', 'provDD', 'modelDD',
        'newProvBtn', 'delProvBtn', 'aiProvider', 'provNew', 'provDel', 'id="modelPick"']
for k in keys:
    idxs = [m.start() for m in re.finditer(re.escape(k), d)]
    print('=== %-18s hits=%d' % (k, len(idxs)))
    for i in idxs[:3]:
        seg = d[max(0, i-160):i+200].replace('\r', '').replace('\n', '\\n')
        print('   ...' + seg + '...')
