# -*- coding: utf-8 -*-
"""Headless Edge dropdown checks for the settings panel (and the main window).

Usage:
    python test_dropdown_layout.py                       # current letter-polisher.html
    python test_dropdown_layout.py <file.html>           # any other build (e.g. a pre-fix copy)

Exit code 0 only when every check passes. The probe itself lives in
_portal_probe.py and runs synchronously inside the page's load handler, because
Edge's --dump-dom snapshots the page there (the app's own update request would
otherwise stall the virtual clock and no deferred timer would ever run).
"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

src = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
tag = os.path.splitext(os.path.basename(src))[0]
probe_html = '_probe_%s.html' % tag
dom = os.path.join(os.environ['TEMP'], 'dom_%s.html' % tag)

print('=== dropdown layout test (%s) ===' % src)
subprocess.run([sys.executable, os.path.join(HERE, '_portal_probe.py'), src, probe_html], check=True)

url = 'file:///' + os.path.join(HERE, probe_html).replace('\\', '/').replace(' ', '%20')
profile = os.path.join(os.environ['TEMP'], 'edgeprobe_%s' % tag)
argv = [EDGE, '--headless=new', '--disable-gpu', '--no-first-run', '--window-size=1194,877',
        '--user-data-dir=' + profile, '--virtual-time-budget=9000', '--dump-dom', url]
with open(dom, 'w', encoding='utf-8', errors='replace') as fh:
    subprocess.run(argv, stdout=fh, stderr=subprocess.DEVNULL, timeout=180)

dom_text = open(dom, encoding='utf-8', errors='replace').read()
m = re.search(r'id="probeOut"[^>]*>(.*?)</div>', dom_text, re.S)
if not m or not m.group(1).strip():
    print('FAIL: no probe output (page did not run)')
    print('dom chars=%d, probe html present=%s' % (len(dom_text), probe_html in dom_text))
    sys.exit(1)

out = m.group(1).strip()
print(out)
passed = len(re.findall(r'^PASS ', out, re.M))
failed = re.findall(r'^FAIL .*$', out, re.M)
print('\n%d passed, %d failed' % (passed, len(failed)))
sys.exit(0 if not failed else 1)
