# -*- coding: utf-8 -*-
"""Bump the app version to 2026.10.01.6 (html APP_VERSION + version.json + notes)."""
import io
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', newline='')
VER = '2026.10.01.6'
DATE = '2026-10-01'

notes_md = """## 改善

- 輸入欄位排列。
- 小按鈕點擊區域。
- 鍵盤焦點顯示。
- 窄版版面底部留白。
"""

open('release-notes-v%s.md' % VER, 'w', encoding='utf-8', newline='\r\n').write(notes_md)

env = json.load(io.open('version.json', encoding='utf-8'))
env['version'] = VER
env['release_date'] = DATE
env['release_notes'] = {
    'zh-TW': '改善：輸入欄位排列、小按鈕點擊區域、鍵盤焦點顯示、窄版版面底部留白。',
    'zh-CN': '改善：输入栏位排列、小按钮点击区域、键盘焦点显示、窄版版面底部留白。',
    'en': 'Improved: field arrangement, small-button hit areas, keyboard focus visibility, '
          'and bottom spacing in the narrow layout.',
}
io.open('version.json', 'w', encoding='utf-8', newline='\n').write(
    json.dumps(env, ensure_ascii=False, indent=2) + '\n')

p = 'letter-polisher.html'
raw = io.open(p, encoding='utf-8', newline='').read()
old = "var APP_VERSION='2026.10.01.5';"
assert raw.count(old) == 1, 'APP_VERSION not found: %d' % raw.count(old)
io.open(p, 'w', encoding='utf-8', newline='').write(raw.replace(old, "var APP_VERSION='%s';" % VER, 1))
print('bumped to', VER)
print(io.open('version.json', encoding='utf-8').read())
