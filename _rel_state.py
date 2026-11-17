# -*- coding: utf-8 -*-
"""Print the state of a release's assets (avoids PowerShell redirect encoding)."""
import json
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
tag = sys.argv[1] if len(sys.argv) > 1 else 'v2026.10.01.6'
p = subprocess.run(['gh', 'release', 'view', tag, '--json',
                    'name,tagName,isDraft,isPrerelease,publishedAt,assets,body'],
                   capture_output=True, text=True, encoding='utf-8')
if p.returncode != 0:
    print('gh error:', p.stderr[-400:])
    sys.exit(1)
d = json.loads(p.stdout)
print('name     :', d['name'])
print('tag      :', d['tagName'])
print('draft    :', d['isDraft'], ' prerelease:', d['isPrerelease'])
print('published:', d['publishedAt'])
for a in d['assets']:
    print('  %-46s %-12s %s' % (a['name'], a['size'], a['state']))
print('--- body ---')
print(d['body'])
