# -*- coding: utf-8 -*-
"""Bump to 2026.10.01.3 with concise release notes."""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

NEW, OLD = '2026.10.01.3', '2026.10.01.2'

p = 'letter-polisher.html'
d = open(p, encoding='utf-8', newline='').read()
needle = "var APP_VERSION='%s';" % OLD
if needle not in d:
    print('FAIL: APP_VERSION %s not found' % OLD); sys.exit(1)
open(p, 'w', encoding='utf-8', newline='').write(d.replace(needle, "var APP_VERSION='%s';" % NEW, 1))
print('OK letter-polisher.html ->', NEW)

v = json.load(open('version.json', encoding='utf-8'))
v['version'] = NEW
v['release_date'] = '2026-10-01'
v['release_notes'] = {
    "zh-TW": "修復：AI 供應商下拉清單位置偏移。",
    "zh-CN": "修复：AI 供应商下拉清单位置偏移。",
    "en": "Fixed: the AI provider dropdown menu was offset from its button."
}
open('version.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(v, ensure_ascii=False, indent=2) + '\n')
print('OK version.json ->', NEW)
