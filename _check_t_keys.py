# -*- coding: utf-8 -*-
"""Every key used by t('...') / data-i must exist in all three locale blocks."""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()

start = s.index('var T={')
end = s.index('\n};', start) + 3
block = s[start:end]
names = [m.group(1) for m in re.finditer(r"(?m)^\s*'([^']+)'\s*:\s*\{", block)]
pos = [m.start() for m in re.finditer(r"(?m)^\s*'([^']+)'\s*:\s*\{", block)]
locs = {}
for i, nm in enumerate(names):
    seg = block[pos[i]:(pos[i + 1] if i + 1 < len(names) else len(block))]
    locs[nm] = {m.group(1) for m in re.finditer(r"(?<![\w'])([A-Za-z_$][\w$]*)\s*:\s*'", seg)}
print('locales:', names)

used = {}
for m in re.finditer(r"\bt\(\s*'([A-Za-z_$][\w$]*)'", s):
    used.setdefault(m.group(1), 0)
    used[m.group(1)] += 1
for m in re.finditer(r'data-i(?:-title)?="([A-Za-z_$][\w$]*)"', s):
    used.setdefault(m.group(1), 0)
    used[m.group(1)] += 1
print('keys referenced:', len(used))

bad = []
for k in sorted(used):
    miss = [nm for nm in names if k not in locs[nm]]
    if miss:
        bad.append((k, miss))
if bad:
    for k, miss in bad:
        print('MISSING %-18s in %s (used %dx)' % (k, ','.join(miss), used[k]))
else:
    print('OK every referenced key exists in all %d locales' % len(names))

# keys that exist but are never referenced (dead strings) - informational only
dead = sorted(k for k in locs[names[0]] if k not in used)
print('unreferenced locale keys: %d %s' % (len(dead), dead[:12]))
raise SystemExit(1 if bad else 0)
