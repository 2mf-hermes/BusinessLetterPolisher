# -*- coding: utf-8 -*-
"""Bump to 2026.10.01.2 and rewrite version.json notes."""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

NEW = '2026.10.01.2'
OLD = '2026.10.01.1'

# 1. letter-polisher.html
p = 'letter-polisher.html'
d = open(p, encoding='utf-8', newline='').read()
needle = "var APP_VERSION='%s';" % OLD
if needle not in d:
    print('FAIL: APP_VERSION %s not found' % OLD); sys.exit(1)
d = d.replace(needle, "var APP_VERSION='%s';" % NEW, 1)
open(p, 'w', encoding='utf-8', newline='').write(d)
print('OK letter-polisher.html ->', NEW)

# 2. version.json
v = json.load(open('version.json', encoding='utf-8'))
v['version'] = NEW
v['release_date'] = '2026-10-01'
v['release_notes'] = {
    "zh-TW": "修復：新增 AI 供應商後，供應商下拉清單看不到、無法選擇（清單被定位到視窗外）。\r\n同時修復設定面板內的供應商／API 格式／模型清單被裁切與超出畫面的問題。",
    "zh-CN": "修复：新增 AI 供应商后，供应商下拉清单看不到、无法选择（清单被定位到窗口外）。\r\n同时修复设置面板内的供应商／API 格式／模型清单被裁切与超出窗口的问题。",
    "en": "Fixed: after adding an AI provider the provider dropdown was invisible and unusable because the list was positioned outside the window. The provider, API format and model lists inside the settings sheet are no longer clipped or off screen."
}
open('version.json', 'w', encoding='utf-8', newline='\n').write(json.dumps(v, ensure_ascii=False, indent=2) + '\n')
print('OK version.json ->', NEW)
