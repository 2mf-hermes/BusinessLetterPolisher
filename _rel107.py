import json, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
r = subprocess.run(['gh', 'release', 'view', 'v2026.10.01.7', '--json',
                    'name,tagName,isDraft,isPrerelease,publishedAt,assets,body'],
                   capture_output=True, text=True, encoding='utf-8', timeout=120)
if r.returncode != 0:
    print('gh error:', r.stderr[:400]); sys.exit(1)
d = json.loads(r.stdout)
print('title    :', d['name'])
print('tag      :', d['tagName'], 'draft=', d['isDraft'], 'prerelease=', d['isPrerelease'])
print('published:', d['publishedAt'])
for a in d['assets']:
    print('asset    :', a['name'], round(a['size'] / 1048576, 2), 'MB', 'state=', a.get('state'))
print('--- body ---')
print(d['body'])
