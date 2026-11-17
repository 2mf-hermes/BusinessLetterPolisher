# -*- coding: utf-8 -*-
"""Bump the app version to 2026.10.01.5 (html APP_VERSION + version.json + notes)."""
import io
import json
import sys

sys.stdout.reconfigure(encoding='utf-8', newline='')
VER = '2026.10.01.5'
DATE = '2026-10-01'

notes_md = """## 修復

- AI 供應商下拉選單位置與穩定性。
- AI 模型下拉選單位置。

## 改善

- AI 連線設定收合顯示與排列。
"""

open('release-notes-v%s.md' % VER, 'w', encoding='utf-8', newline='\r\n').write(notes_md)

env = json.load(io.open('version.json', encoding='utf-8'))
env['version'] = VER
env['release_date'] = DATE
env['release_notes'] = {
    'zh-TW': '修復：AI 供應商下拉選單位置與穩定性、AI 模型下拉選單位置。改善：AI 連線設定收合顯示與排列。',
    'zh-CN': '修复：AI 供应商下拉菜单位置与稳定性、AI 模型下拉菜单位置。改善：AI 连接设置收起显示与排列。',
    'en': 'Fixed: the AI provider and model dropdown positions and stability. Improved: the AI connection settings stay collapsed, with a tidier arrangement.',
}
io.open('version.json', 'w', encoding='utf-8', newline='\n').write(
    json.dumps(env, ensure_ascii=False, indent=2) + '\n')

p = 'letter-polisher.html'
raw = io.open(p, encoding='utf-8', newline='').read()
old = "var APP_VERSION='2026.10.01.4';"
assert raw.count(old) == 1, raw.count(old)
io.open(p, 'w', encoding='utf-8', newline='').write(raw.replace(old, "var APP_VERSION='%s';" % VER, 1))
print('bumped to', VER)
print(io.open('version.json', encoding='utf-8').read())
