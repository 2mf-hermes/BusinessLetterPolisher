# -*- coding: utf-8 -*-
"""Bump the app version to 2026.10.01.7 (html APP_VERSION + version.json + notes)."""
import io
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', newline='')
VER = '2026.10.01.7'
DATE = '2026-10-01'

notes_md = """## \u4fee\u5fa9

- \u5feb\u901f\u8a2d\u5b9a\u5957\u7528\u3002
- \u4fee\u6539\u5efa\u8b70\u56de\u7b54\u8a9e\u8a00\u3002
- \u6f64\u98fe\u7d50\u679c\u524d\u7db4\u8207\u8aaa\u660e\u6587\u5b57\u3002

## \u6539\u5584

- \u5feb\u901f\u8a2d\u5b9a\u5957\u7528\u5f8c\u7684\u63d0\u793a\u3002
"""

open('release-notes-v%s.md' % VER, 'w', encoding='utf-8', newline='\r\n').write(notes_md)

env = json.load(io.open('version.json', encoding='utf-8'))
env['version'] = VER
env['release_date'] = DATE
env['release_notes'] = {
    'zh-TW': '\u4fee\u5fa9\uff1a\u5feb\u901f\u8a2d\u5b9a\u5957\u7528\u3001\u4fee\u6539\u5efa\u8b70\u56de\u7b54\u8a9e\u8a00\u3001'
             '\u6f64\u98fe\u7d50\u679c\u524d\u7db4\u8207\u8aaa\u660e\u6587\u5b57\u3002\u6539\u5584\uff1a\u5feb\u901f\u8a2d\u5b9a\u5957\u7528\u5f8c\u7684\u63d0\u793a\u3002',
    'zh-CN': '\u4fee\u590d\uff1a\u5feb\u901f\u8bbe\u7f6e\u5e94\u7528\u3001\u4fee\u6539\u5efa\u8bae\u56de\u7b54\u8bed\u8a00\u3001'
             '\u6f64\u9970\u7ed3\u679c\u524d\u7f00\u4e0e\u8bf4\u660e\u6587\u5b57\u3002\u6539\u5584\uff1a\u5feb\u901f\u8bbe\u7f6e\u5e94\u7528\u540e\u7684\u63d0\u793a\u3002',
    'en': 'Fixed: applying quick presets, the language of the suggestion notes, and extra '
          'wording around the polished result. Improved: feedback after a preset is applied.',
}
io.open('version.json', 'w', encoding='utf-8', newline='\n').write(
    json.dumps(env, ensure_ascii=False, indent=2) + '\n')

p = 'letter-polisher.html'
raw = io.open(p, encoding='utf-8', newline='').read()
old = "var APP_VERSION='2026.10.01.6';"
assert raw.count(old) == 1, 'APP_VERSION not found: %d' % raw.count(old)
io.open(p, 'w', encoding='utf-8', newline='').write(raw.replace(old, "var APP_VERSION='%s';" % VER, 1))
print('bumped to', VER)
print(io.open('version.json', encoding='utf-8').read())
