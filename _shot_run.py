# -*- coding: utf-8 -*-
"""Headless Edge screenshot: python _shot_run.py <html> <png> [virtual_ms] [WxH]"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
html = os.path.abspath(sys.argv[1])
png = os.path.abspath(sys.argv[2])
vt = sys.argv[3] if len(sys.argv) > 3 else '6000'
size = sys.argv[4] if len(sys.argv) > 4 else '1194,877'
edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if os.path.exists(png):
    os.remove(png)
cmd = [edge, '--headless=new', '--disable-gpu', '--no-first-run', '--hide-scrollbars',
       '--window-size=' + size, '--user-data-dir=' + os.path.join(os.environ.get('TEMP', '.'), 'edgeshot'),
       '--virtual-time-budget=' + vt, '--screenshot=' + png,
       'file:///' + html.replace('\\', '/')]
p = subprocess.run(cmd, capture_output=True, timeout=180)
print('exit', p.returncode, 'png exists', os.path.exists(png),
      (os.path.getsize(png) if os.path.exists(png) else 0), 'bytes')
err = p.stderr.decode('utf-8', 'replace').strip()
if err:
    print(err[-400:])
