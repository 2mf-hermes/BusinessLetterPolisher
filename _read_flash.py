# -*- coding: utf-8 -*-
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
p = os.path.join(os.environ['TEMP'], 'flash_dom.html')
s = open(p, encoding='utf-8', errors='replace').read()
print('domlen', len(s))
m = re.search(r'id="probeOut"[^>]*>(.*?)</div>', s, re.S)
print(m.group(1).strip() if m else 'NO PROBE OUTPUT')
