# -*- coding: utf-8 -*-
"""Confirm dist/BusinessLetterPolisher.zip carries the newly built HTML."""
import hashlib
import io
import sys
import zipfile

sys.stdout.reconfigure(encoding='utf-8')

a = io.open('letter-polisher.html', encoding='utf-8', newline='').read()
b = zipfile.ZipFile('../dist/BusinessLetterPolisher.zip').read('letter-polisher.html').decode('utf-8')
print('source version :', [l.strip() for l in a.split('\r\n') if 'APP_VERSION=' in l][0])
print('in-zip version :', [l.strip() for l in b.split('\r\n') if 'APP_VERSION=' in l][0])
print('same bytes     :', hashlib.sha256(a.encode('utf-8')).hexdigest() ==
      hashlib.sha256(b.encode('utf-8')).hexdigest())
for m in ['min-height:28px', 'padding-bottom:84px', 'prefers-reduced-motion',
          ':focus-visible', '.opts-grid>#custTone{order:7;}', 'grid-column:1/-1']:
    print('  %-32s %s' % (m, m in b))
