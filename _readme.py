import io

p = 'README.md'
with io.open(p, 'r', encoding='utf-8', newline='') as f:
    t = f.read()
NL = '\r\n' if '\r\n' in t else '\n'

old_feat = '- **各家 API** — OpenAI、Anthropic、Google Gemini、Groq、DeepSeek、自架 LLM' + NL
assert t.count(old_feat) == 1
new_feat = old_feat + \
    '- **AI 供應商模式** — 儲存多組供應商（名稱、URL、Key、格式、模型），用下拉清單快速切換' + NL + \
    '- **模型清單載入** — 填入 AI URL 與 Key 後一鍵查詢該供應商的可用模型，直接從清單挑選' + NL
t = t.replace(old_feat, new_feat)

old_use = NL.join([
    '1. 點擊右下角 ⚙ 齒輪設定 API',
    '2. 選擇預設或手動輸入 API 端點、Key、模型',
    '3. 儲存並測試連線',
    '4. 在左側輸入信件，選擇風格與用途',
    '5. 點「開始潤飾」',
    '',
])
assert t.count(old_use) == 1, t.count(old_use)
new_use = NL.join([
    '1. 點擊右下角 ⚙ 齒輪設定 API',
    '2. 在「AI 供應商」下拉清單選擇既有供應商，或按「新增」建立一組（可自行命名）',
    '3. 輸入該供應商的 AI URL 與 API Key，按「載入模型」查詢可用模型並從清單挑選（也可手動輸入）',
    '4. 儲存並測試連線',
    '5. 在左側輸入信件，選擇風格與用途',
    '6. 點「開始潤飾」',
    '',
])
t = t.replace(old_use, new_use)

with io.open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(t)
print('README updated;', len(t), 'chars')
