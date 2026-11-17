# -*- coding: utf-8 -*-
"""Confirm the packaged HTML is the one that was committed."""
import io
import hashlib
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')
z = zipfile.ZipFile(r'C:\Users\MINFU LIAO\OpenWorker\4e6bb304-22a\dist\BusinessLetterPolisher.zip')
names = z.namelist()
print('zip entries:', len(names))
html = None
for n in names:
    if n.replace('\\', '/').endswith('letter-polisher.html'):
        html = z.read(n)
if html is None:
    raise SystemExit('no letter-polisher.html in the zip')
disk = io.open('letter-polisher.html', 'rb').read()
print('html bytes  zip=%d disk=%d' % (len(html), len(disk)))
print('sha256 equal:', hashlib.sha256(html).hexdigest() == hashlib.sha256(disk).hexdigest())
s = html.decode('utf-8')
for probe in ["APP_VERSION='2026.10.01.5'", '.cs-dd-fx', 'function csSettleFix', 'provEditBox',
              '.prov-edit.open', '.btn.on{background', 'cs-dd{', 'function setProvEdit']:
    print('  %-30s %s' % (probe, 'FOUND' if probe in s else 'MISSING'))
print('transition:all inside the .cs-dd rule:', 'transition:all .18s' in s[s.index('.cs-dd{'):s.index('.cs-dd{') + 900])
print('entries:', sorted(x.replace('\\', '/') for x in names))
