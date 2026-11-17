# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ['TEMP'], 'flash_dom.html')
s = open(path, encoding='utf-8', errors='replace').read()
print('domlen', len(s))
m = re.search(r'id="probeOut"[^>]*>(.*?)</div>', s, re.S)
if not m:
    print('NO PROBE OUTPUT')
    print('has probe script:', 'probeOut' in s)
else:
    txt = m.group(1).strip()
    print(txt if txt else '(empty probe output)')
