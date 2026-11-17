import io, json, re

V = '2026.10.01.1'

# version.json
p = 'version.json'
raw = io.open(p, encoding='utf-8', newline='').read()
d = json.loads(raw)
d['version'] = V
d['release_date'] = '2026-10-01'
d['release_notes'] = {
    "zh-TW": "修復：安裝路徑含空白時更新會在重啟前失敗（出現「Windows 找不到 F:\\Program」），更新檔已無法複製到安裝目錄。",
    "zh-CN": "修复：安装路径含空白时更新会在重启前失败（出现「Windows 找不到 F:\\Program」），更新文件无法复制到安装目录。",
    "en": "Fixed: when the install path contained a space, the update failed before restarting (Windows could not find \"F:\\Program\") and the new files were never copied into the install folder.",
}
io.open(p, 'w', encoding='utf-8', newline='\r\n').write(json.dumps(d, ensure_ascii=False, indent=2) + '\n')

# letter-polisher.html
p = 'letter-polisher.html'
html = io.open(p, encoding='utf-8', newline='').read()
new, n = re.subn(r"var APP_VERSION='[^']*';", "var APP_VERSION='" + V + "';", html)
assert n == 1, n
io.open(p, 'w', encoding='utf-8', newline='').write(new)

print('version:', d['version'], '| APP_VERSION bumped:', n, '| html chars:', len(new))
