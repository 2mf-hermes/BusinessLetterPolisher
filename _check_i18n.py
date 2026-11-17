# -*- coding: utf-8 -*-
"""List every data-i / data-i-title key in the document and check it against each
locale block of `var T={...}` - a missing key renders as an empty label."""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()

start = s.index('var T={')
# the object literal ends at the first "\n};" after start
end = s.index('\n};', start)
block = s[start:end]
# split on lines that look like "xx:{"
locs = {}
for m in re.finditer(r"(?m)^\s*'([^']+)'\s*:\s*\{", block):
    locs[m.group(1)] = m.start()
print('locales:', list(locs))

keys = set(re.findall(r'data-i="([^"]+)"', s)) | set(re.findall(r'data-i-title="([^"]+)"', s))
print('document keys: %d' % len(keys))

names = list(locs)
for idx, name in enumerate(names):
    a = locs[name]
    b = locs[names[idx + 1]] if idx + 1 < len(names) else len(block)
    seg = block[a:b]
    own = set(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", seg))
    missing = sorted(k for k in keys if k not in own)
    print('%-6s own=%d missing=%d %s' % (name, len(own), len(missing), missing[:20]))
