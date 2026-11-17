# -*- coding: utf-8 -*-
"""v2026.10.01.7 part C (retry): localised feedback for quick presets."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')

PATH = 'letter-polisher.html'
src = io.open(PATH, encoding='utf-8', newline='').read()

items = [
    ("presetCompat:'\u81ea\u67b6',", "\u81ea\u67b6", 2,
     "presetCompat:'\u81ea\u67b6',presetApplied:'\u5df2\u5957\u7528\u5feb\u901f\u8a2d\u5b9a\uff0c\u8acb\u586b\u5165 API Key',"),
    ("presetCompat:'Self-hosted',", "Self-hosted", 1,
     "presetCompat:'Self-hosted',presetApplied:'Preset applied \u2014 add your API key',"),
    ("try{toast(nm+' \\u00b7 '+t('modelName')+': '+p.m);}catch(e){}}", "toast", 1,
     "try{toast(t('presetApplied')+' \u00b7 '+nm+' / '+p.m);}catch(e){}}"),
]

applied = 0
for old, tag, want, new in items:
    n = src.count(old)
    if want == 1:
        if n != 1:
            print('MISS %s (%d)' % (tag, n))
            continue
        src = src.replace(old, new)
    else:
        if n != 2:
            print('MISS %s (%d)' % (tag, n))
            continue
        src = src.replace(old, new, 1)          # zh-TW first
        parts = src.split("presetCompat:'\u81ea\u67b6',", 1)
        src = parts[0] + "presetCompat:'\u81ea\u67b6',presetApplied:'\u5df2\u5e94\u7528\u5feb\u901f\u9884\u8bbe\uff0c\u8bf7\u586b\u5165 API Key'," + parts[1]
    applied += 1

io.open(PATH, 'w', encoding='utf-8', newline='').write(src)
print('v107c applied: %d/%d items' % (applied, len(items)))
