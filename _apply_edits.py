# -*- coding: utf-8 -*-
import io, re, sys

p = 'letter-polisher.html'
d = io.open(p, encoding='utf-8').read()
orig = d

# ---------- 1. Add id to letterLang dropdown ----------
d = d.replace(
    '<div class="cs" id="letterLangCS">',
    '<div class="cs" id="letterLangCS">',
    1
)
# add id to the dd following letterLangCS button
# find the dd right after letterLang button
d = d.replace(
    '<div class="cs-dd">\n            <div class="cs-opt" data-val="zh-TW"',
    '<div class="cs-dd" id="letterLangDD">\n            <div class="cs-opt" data-val="zh-TW"',
    1
)

# ---------- 2. Populate outLang & letterLang dynamically ----------
# Insert a populate function after LETTER_LANGS definition
anchor = "var locale='en',DF={"
populate_fn = '''function populateLangDropdowns(){\n  // letterLang dropdown (source language)\n  var ll=$('letterLangDD');\n  if(ll&&!ll.getAttribute('data-pop')){\n    LETTER_LANGS.forEach(function(l){\n      var exists=ll.querySelector('.cs-opt[data-val="'+l.v+'"]');\n      if(exists)return;\n      var o=document.createElement('div');\n      o.className='cs-opt';o.setAttribute('data-val',l.v);\n      o.setAttribute('onclick','csPick(this)');\n      o.innerHTML='<span>'+l.label+'</span><span class="cs-chk">\\u2713</span>';\n      ll.appendChild(o);\n    });\n    ll.setAttribute('data-pop','1');\n  }\n  // outLang dropdown (output language)\n  var ol=$('outLangDD');\n  if(ol&&!ol.getAttribute('data-pop')){\n    LETTER_LANGS.forEach(function(l){\n      var exists=ol.querySelector('.cs-opt[data-val="'+l.v+'"]');\n      if(exists)return;\n      var o=document.createElement('div');\n      o.className='cs-opt';o.setAttribute('data-val',l.v);\n      o.setAttribute('onclick','csPick(this)');\n      o.innerHTML='<span>'+l.label+'</span><span class="cs-chk">\\u2713</span>';\n      ol.appendChild(o);\n    });\n    ol.setAttribute('data-pop','1');\n  }\n}\n'''
d = d.replace(anchor, populate_fn + anchor, 1)

# ---------- 3. Fix initial language detection: sync letterLang default ----------
# detectLang returns 'zh-TW', 'zh-CN', or 'en'
# Update init: after setting locale, default LO.letterLang to a matching lang if 'auto'
init_old = "var saved=localStorage.getItem('bp_lang');locale=saved||detectLang();if(!T[locale])locale='en';"
init_new = ("var saved=localStorage.getItem('bp_lang');locale=saved||detectLang();if(!T[locale])locale='en';\n"
            "  var detLang=detectLang();if(LO.letterLang==='auto'){LO.letterLang=(detLang==='zh-TW'||detLang==='zh-CN'||detLang==='en'||detLang==='ja')?detLang:'en';}\n"
            "  populateLangDropdowns();")
d = d.replace(init_old, init_new, 1)

# ---------- 4. Wire fillLetterOpts into init ----------
init_call_old = "loadTheme();loadCfg();fillF();onToneCh();onPurpCh();updCnt();loadH();applyI18n();applyGuideHTML();"
init_call_new = "loadTheme();loadCfg();loadLetterOpts();fillF();fillLetterOpts();updCnt();loadH();applyI18n();applyGuideHTML();populateLangDropdowns();"
d = d.replace(init_call_old, init_call_new, 1)

io.open(p, 'w', encoding='utf-8').write(d)
print('OK', len(d), 'chars', 'changed' if d != orig else 'NOCHANGE')