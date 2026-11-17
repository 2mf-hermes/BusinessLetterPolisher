# -*- coding: utf-8 -*-
import io

p = 'letter-polisher.html'
d = io.open(p, encoding='utf-8').read()

# Remove duplicate populateLangDropdowns function (keep only first)
fn_sig = 'function populateLangDropdowns(){'
first = d.find(fn_sig)
# find the full first function body end
def match_brace(s, start):
    # start points at 'function ... {', find matching brace
    i = s.index('{', start)
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{': depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return j + 1
    return -1

first_end = match_brace(d, first)
second = d.find(fn_sig, first_end)
assert first_end > 0 and second > 0, (first, first_end, second)
# remove everything from second occurrence to its end
second_end = match_brace(d, second)
d = d[:second] + d[second_end:]

# Remove duplicated init lines (detLang/populateLangDropdowns appear twice)
dup = "\n  var detLang=detectLang();if(LO.letterLang==='auto'){LO.letterLang=(detLang==='zh-TW'||detLang==='zh-CN'||detLang==='en'||detLang==='ja')?detLang:'en';}\n  populateLangDropdowns();\n  var detLang=detectLang();if(LO.letterLang==='auto'){LO.letterLang=(detLang==='zh-TW'||detLang==='zh-CN'||detLang==='en'||detLang==='ja')?detLang:'en';}\n  populateLangDropdowns();"
one = "\n  var detLang=detectLang();if(LO.letterLang==='auto'){LO.letterLang=(detLang==='zh-TW'||detLang==='zh-CN'||detLang==='en'||detLang==='ja')?detLang:'en';}\n  populateLangDropdowns();"
if dup in d:
    d = d.replace(dup, one, 1)
    print('removed dup init')
else:
    print('dup init not found (may already be fine)')

io.open(p, 'w', encoding='utf-8').write(d)
print('done', len(d))