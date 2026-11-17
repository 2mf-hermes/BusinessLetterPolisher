# -*- coding: utf-8 -*-
"""v2026.10.01.7 fixes.

1) Quick presets: applying a preset now really takes effect — the provider is
   named after the preset, the connection block opens so the change is visible,
   the summary line refreshes, and a toast confirms it.
2) The '--- Suggestions ---' section may change the letter language only; the
   suggestions must be written in the ORIGINAL letter's language.
3) The polished result must contain nothing but the letter: no preamble like
   "Here is the revised version", no advice, no explanations, no warnings.

Each anchor is matched as an exact substring of the current file.  Line endings
are left untouched (the file stays CRLF); run _check_nl.py afterwards.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PATH = 'letter-polisher.html'

EDITS = []

# ---------------------------------------------------------------- 1. presets
EDITS.append((
    "function applyPreset(k,el){var p=PR[k];sV('apiUrl',p.u);sV('modelName',p.m);sV('apiFormat',p.f);"
    "if(!v('provName'))sV('provName',t(p.k));var ap=activeProv();if(ap)ap.models=[];csSyncAll();"
    "refreshModelDD();persistActiveProvider();applyActiveProvider();refreshProviderDD();",
    "function applyPreset(k,el){var p=PR[k],nm=t(p.k);"
    "var ap=activeProv(),prev=null;try{prev=JSON.parse(localStorage.getItem('bp_providers')||'[]');}catch(e){}"
    "var fresh=!ap||(!String(ap.url||'').trim()&&!String(ap.key||'').trim()&&!String(ap.model||'').trim());"
    "sV('apiUrl',p.u);sV('modelName',p.m);sV('apiFormat',p.f);"
    "if(fresh||!v('provName')||/^AI |^AI$/.test(v('provName')))sV('provName',nm);"
    "if(ap)ap.models=[];csSyncAll();refreshModelDD();persistActiveProvider();applyActiveProvider();refreshProviderDD();"
    "provEditNewId=null;setProvEdit(true);refreshProvCur();csSyncAll();"
))
EDITS.append((
    "if(el)el.classList.add('on');}",
    "if(el)el.classList.add('on');"
    "try{toast(nm+' \\u00b7 '+t('modelName')+': '+p.m);}catch(e){}}",
))

# ------------------------------------------- 2/3. prompt + result extraction
OLD_LANG = ("    langLines.push('- The \\\"--- Suggestions ---\\\" section must also be written in '+outName+'.');")
NEW_LANG = (
    "    langLines.push('- The \\\"--- Suggestions ---\\\" section is ALWAYS written in '+(srcName||'the original letter\\'s language')+"
    "+(srcR?', following the language conventions of '+srcR.en:'')+', even when the polished letter itself is in '+outName+"
    "+'. The language choice above applies ONLY to the polished letter, never to the suggestions.');"
)
EDITS.append((OLD_LANG, NEW_LANG))

OLD_TAIL = "  var sysPrompt=basePrompt+'\\n\\n'+langBlock+'\\n\\nAppend \\\"--- Suggestions ---\\\" section (2-5 points) at the end.';"
NEW_TAIL = (
    "  var outRule=null;\n"
    "  outRule.push('[OUTPUT RULES \\u2014 STRICT]');\n"
    "  outRule.push('- Return ONLY the letter itself: greeting, body, closing and signature. No headings, no labels, no commentary.');\n"
    "  outRule.push('- Never begin with a preamble such as \"Here is the polished version\", \"Below is the revised letter\", \"\\u4ee5\\u4e0b\\u70ba\\u4fee\\u6539\\u5f8c\\u7684\\u7d50\\u679c\", \"\\u4ee5\\u4e0b\\u4e3a\\u4fee\\u6539\\u540e\\u7684\\u7ed3\\u679c\" or \"\\u4f60\\u597d\\uff0c\\u4ee5\\u4e0b\\u662f...\".');\n"
    "  outRule.push('- Do NOT explain what you changed, do NOT add tips, teaching notes, reminders, warnings, options, translations or questions. Do NOT wrap the letter in code fences or quotation marks.');\n"
    "  outRule.push('- The \\\"--- Suggestions ---\\\" marker must appear exactly once, after the letter and its closing.');\n"
    "  outRule.push('- The \\\"--- Suggestions ---\\\" section: 2-5 short points, one per line, each stating only WHAT could be improved. It is written in the original letter\\'s language (see [LANGUAGE REQUIREMENTS]) and never restates the polished letter.');\n"
    "  var sysPrompt=basePrompt+'\\n\\n'+langBlock+'\\n\\n'+outRule.join('\\n');"
)
EDITS.append((OLD_TAIL, NEW_TAIL))

OLD_RES = ("  var el2=((Date.now()-st)/1000).toFixed(1);var pt=r.split('--- Suggestions ---');"
           "var polished=pt[0].trim();var sug=pt.length>1?pt[1].trim():'';")
NEW_RES = ("  var el2=((Date.now()-st)/1000).toFixed(1);var pt=splitResult(r);"
           "var polished=pt.polished;var sug=pt.suggestions;")
EDITS.append((OLD_RES, NEW_RES))

OLD_HELPER_ANCHOR = "function showSts(m,tp){"
NEW_HELPER = r"""/* ---- result clean-up: keep the letter only, keep the suggestions apart ---- */
var LEAD_RE=/^\s*(?:(?:#{1,6}\s*|\*\*)?(?:polished|revised|rewritten|final|improved|edited|updated)\s*(?:letter|version|e-?mail|text)?(?:\*\*)?\s*:?\s*$|[-=*\u2500\u2501]{3,}|(?:here(?:'s| is)|below is|following is)\b[^\n]*|(?:sure|certainly|of course|absolutely)\b[^\n]*|(?:\u4ee5\u4e0b|\u4e0b\u9762|\u4e0b\u65b9)[^\n]{0,40}(?:\u7d50\u679c|\u7ed3\u679c|\u4fee\u6539|\u4fee\u6b63|\u6f64\u98fe|\u6da6\u9970|\u4fe1\u4ef6)\s*[:\uff1a]?|[\u7e41\u7b26][\u9ad4\u4f53][\u5b57\u4f53]\s*[\uff1a:])\s*$/i;
function stripFence(s){
  var m=String(s||'').trim().match(/^```[a-zA-Z]*\s*\n([\s\S]*?)\n?```\s*$/);
  return m?m[1]:String(s||'');
}
function cleanResult(out){
  var body=stripFence(out).replace(/\r\n/g,'\n').replace(/\r/g,'\n').trim();
  if(!body)return '';
  var ls=body.split('\n'),i=0;
  while(i<ls.length&&(!ls[i].trim()||LEAD_RE.test(ls[i])))i++;
  body=ls.slice(i).join('\n').trim();
  body=body.replace(/^\*\*(.+?)\*\*$/, '$1').trim();
  return body;
}
function splitResult(raw){
  var s=String(raw||'').replace(/\r\n/g,'\n').replace(/\r/g,'\n');
  var marker='--- Suggestions ---',idx=-1,m;
  var re=/-{2,}\s*suggestions\s*-{2,}/i;
  m=re.exec(s);
  if(m)idx=m.index;
  else{var low=s.toLowerCase(),k=low.indexOf(marker.toLowerCase());if(k>=0)idx=k;}
  var letterPart=idx>=0?s.slice(0,idx):s;
  var sugPart=idx>=0?s.slice(idx).replace(/^[\s\S]*?suggestions[^\n]*\n?/i,''):'';
  return {polished:cleanResult(letterPart),suggestions:cleanSuggestions(sugPart)};
}
function cleanSuggestions(s){
  var lines=String(s||'').replace(/\r\n/g,'\n').split('\n'),out=[];
  for(var i=0;i<lines.length;i++){
    var l=lines[i].replace(/^\s*(?:[-*\u2022\u00b7]|\d+[.)])\s*/,'').trim();
    if(!l)continue;
    if(/^```/.test(l))continue;
    if(/^(?:hope|let me know|feel free|if you (?:want|need|would like)|would you like|note:)/i.test(l))continue;
    if(/^(?:\u5e0c\u671b|\u5982\u679c\u4f60\u9700\u8981|\u5982\u9700|\u6b61\u8fce\u544a\u77e5|\u6b22\u8fce\u544a\u77e5)/.test(l))continue;
    out.push(l);
  }
  return out.join('\n');
}
"""
EDITS.append((OLD_HELPER_ANCHOR, NEW_HELPER + OLD_HELPER_ANCHOR))

# suggestions need line breaks when rendered
EDITS.append((
    "  $('sugV').innerHTML=sug?sug.replace(/\\n/g,'<br>'):'<span style=\"color:var(--tx3)\">'+esc(t('noSug'))+'</span>';",
    "  $('sugV').innerHTML=sug?esc(sug).replace(/\\n/g,'<br>'):'<span style=\"color:var(--tx3)\">'+esc(t('noSug'))+'</span>';",
))

# ---------------------------------------------------------------- apply
src = open(PATH, encoding='utf-8', newline='').read()
applied = 0
for old, new in EDITS:
    if src.count(old) != 1:
        print('MISS (%d): %s' % (src.count(old), old[:110]))
        continue
    src = src.replace(old, new)
    applied += 1

open(PATH, 'w', encoding='utf-8', newline='').write(src)
print('v107 applied: %d/%d edits' % (applied, len(EDITS)))
