# -*- coding: utf-8 -*-
"""Run a probe page in headless Edge and print the contents of #probeOut.

usage: python _run_probe.py _jump.html [virtual_time_ms] [WxH]
"""
import os
import re
import subprocess
import sys
import tempfile
import html as htmlmod

sys.stdout.reconfigure(encoding='utf-8')

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

page = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '_jump.html')
budget = sys.argv[2] if len(sys.argv) > 2 else '3000'
size = sys.argv[3] if len(sys.argv) > 3 else '1194,877'
url = 'file:///' + page.replace('\\', '/')
profile = os.path.join(tempfile.gettempdir(), 'edgeprobe_run')

cmd = [EDGE, '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
       '--user-data-dir=' + profile, '--window-size=' + size,
       '--virtual-time-budget=' + budget, '--dump-dom', url]
p = subprocess.run(cmd, capture_output=True, timeout=180)
dom = p.stdout.decode('utf-8', 'replace')
if len(dom) < 500:
    dom = p.stderr.decode('utf-8', 'replace')
print('domlen=%d' % len(dom))

m = re.search(r'<div id="probeOut"[^>]*>(.*?)</div>', dom, re.S)
if not m:
    print('!! no #probeOut in the dumped DOM')
    print(dom[:2000])
    sys.exit(2)
text = htmlmod.unescape(m.group(1)).strip()
print('----- probe output -----')
print(text)
print('----- end -----')
sys.exit(1 if 'FAIL' in text else 0)
