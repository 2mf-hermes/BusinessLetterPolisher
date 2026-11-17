# -*- coding: utf-8 -*-
import io
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('_portal2.html', encoding='utf-8', newline='').read()
m = re.search(r'<script>\s*\(function\(\)\{\s*var log=\[\].*?</script>', s, re.S)
print('found probe script:', bool(m))
if m:
    js = m.group(0)[len('<script>'):-len('</script>')]
    open('_probe_only.js', 'w', encoding='utf-8', newline='').write(js)
    r = subprocess.run(['node', '--check', '_probe_only.js'], capture_output=True, text=True)
    print('node --check rc', r.returncode)
    print(r.stdout, r.stderr)
