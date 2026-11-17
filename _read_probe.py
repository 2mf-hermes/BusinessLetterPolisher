# -*- coding: utf-8 -*-
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
path = os.path.join(os.environ.get('TEMP', '.'), 'probe_dom.html')
d = open(path, encoding='utf-8', errors='replace').read()
m = re.search(r'<pre id="probeOut"[^>]*>(.*?)</pre>', d, re.S)
if not m:
    m = re.search(r'id="probeOut"[^>]*>(.*?)</pre>', d, re.S)
print(m.group(1) if m else 'NO PROBE OUTPUT (domlen=%d)' % len(d))
