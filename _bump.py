import io, json

VER = '2026.10.01'

p = 'letter-polisher.html'
with io.open(p, 'r', encoding='utf-8', newline='') as f:
    h = f.read()
old = "var APP_VERSION='2026.08.31.3';"
assert h.count(old) == 1
h = h.replace(old, "var APP_VERSION='%s';" % VER)
with io.open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(h)
print('APP_VERSION ->', VER)

notes = {
    'zh-TW': '新增：AI 供應商模式，可儲存多組供應商，並用下拉清單切換。新增：填入 AI URL 與 API Key 後可載入模型清單，直接從清單挑選模型。新增：供應商可自行命名、新增與刪除。改善：既有的單組 API 設定會自動轉成第一組供應商，不需重新輸入。',
    'zh-CN': '新增：AI 供应商模式，可保存多组供应商，并用下拉列表切换。新增：填入 AI URL 与 API Key 后可载入模型清单，直接从清单选择模型。新增：供应商可自行命名、新增与删除。改善：原有的单组 API 设置会自动转换为第一组供应商，无需重新输入。',
    'en': 'Added: AI provider mode — save multiple providers and switch between them from a drop-down list. Added: after entering the AI URL and API key, load the available model list and pick a model directly. Added: providers can be named, added and deleted. Improved: an existing single API configuration is migrated into the first provider automatically.',
}

vp = 'version.json'
with io.open(vp, 'r', encoding='utf-8', newline='') as f:
    raw = f.read()
d = json.loads(raw)
d['version'] = VER
d['release_date'] = '2026-10-01'
d['release_notes'] = notes
with io.open(vp, 'w', encoding='utf-8', newline='') as f:
    f.write(json.dumps(d, ensure_ascii=False, indent=2) + ('\r\n' if raw.endswith('\r\n') else '\n'))
print('version.json ->', VER)
