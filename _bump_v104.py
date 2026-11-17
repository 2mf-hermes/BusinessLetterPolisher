# -*- coding: utf-8 -*-
"""Bump the app version to 2026.10.01.4 (html APP_VERSION + version.json + notes)."""
import io
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', newline='')
VER = '2026.10.01.4'
DATE = '2026-10-01'

notes_md = """## 修復

- AI 供應商下拉選單顯示穩定性。
- AI 供應商模型下拉選單位置。

## 改善

- AI 模型清單支援再次點擊收合。
"""

open('release-notes-v%s.md' % VER, 'w', encoding='utf-8', newline='\r\n').write(notes_md)

env = json.load(io.open('version.json', encoding='utf-8'))
env['version'] = VER
env['release_date'] = DATE
env['release_notes'] = {
    'zh-TW': '修復：AI 供應商下拉選單顯示穩定性、模型下拉選單位置。改善：AI 模型清單支援再次點擊收合。',
    'zh-CN': '修复：AI 供应商下拉菜单显示稳定性、模型下拉菜单位置。改善：AI 模型列表支持再次点击收起。',
    'en': 'Fixed: the AI provider dropdown disappearing after it opened, and the model dropdown position. Improved: the model list closes when its button is clicked again.',
}
io.open('version.json', 'w', encoding='utf-8', newline='\n').write(
    json.dumps(env, ensure_ascii=False, indent=2) + '\n')

p = 'letter-polisher.html'
raw = io.open(p, encoding='utf-8', newline='').read()
old = "var APP_VERSION='2026.10.01.3';"
assert raw.count(old) == 1, raw.count(old)
io.open(p, 'w', encoding='utf-8', newline='').write(raw.replace(old, "var APP_VERSION='%s';" % VER, 1))
print('bumped to', VER)
print(io.open('version.json', encoding='utf-8').read())
