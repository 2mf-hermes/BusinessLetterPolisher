# -*- coding: utf-8 -*-
"""v2026.10.01.7 part B: the two prompt edits that need literal quotes."""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PATH = 'letter-polisher.html'

OLD_LANG = r"""    langLines.push('- The "--- Suggestions ---" section must also be written in '+outName+'.');"""
NEW_LANG = (
    r"""    langLines.push('- The "--- Suggestions ---" section is ALWAYS written in '+(srcName||"the original letter's language")"""
    r"""+(srcR?', following the language conventions of '+srcR.en:'')+', even when the polished letter itself is in '+outName"""
    r"""+'. The language choice above applies ONLY to the polished letter, never to the suggestions.');"""
)

OLD_TAIL = (
    r"""  var sysPrompt=basePrompt+'\n\n'+langBlock+'\n\nAppend "--- Suggestions ---" section (2-5 points) at the end.';"""
)
NEW_TAIL = (
    "  var outRule=[];\n"
    "  outRule.push('[OUTPUT RULES \\u2014 STRICT]');\n"
    "  outRule.push('- Return ONLY the letter itself: greeting, body, closing and signature. No heading, no label, no title line.');\n"
    "  outRule.push('- Never open with a preamble such as \"Here is the polished version\", \"Below is the revised letter\", "
    "\"\\u4ee5\\u4e0b\\u70ba\\u4fee\\u6539\\u5f8c\\u7684\\u7d50\\u679c\", \"\\u4ee5\\u4e0b\\u4e3a\\u4fee\\u6539\\u540e\\u7684\\u7ed3\\u679c\" or \"\\u4ee5\\u4e0b\\u662f...\".');\n"
    "  outRule.push('- Do NOT explain what you changed, and do NOT add tips, teaching notes, reminders, warnings, alternative versions, translations or questions.');\n"
    "  outRule.push('- Do NOT wrap the letter in code fences or quotation marks.');\n"
    "  outRule.push('- The \\\"--- Suggestions ---\\\" marker must appear exactly once, after the letter as a whole.');\n"
    "  outRule.push('- The \\\"--- Suggestions ---\\\" section (see [LANGUAGE REQUIREMENTS] for its language): 2-5 short points, one per line, each stating only WHAT could still be improved. Never restate the polished letter.');\n"
    "  var sysPrompt=basePrompt+'\\n\\n'+langBlock+'\\n\\n'+outRule.join('\\n');"
)

EDITS = [(OLD_LANG, NEW_LANG), (OLD_TAIL, NEW_TAIL)]

src = open(PATH, encoding='utf-8', newline='').read()
applied = 0
for old, new in EDITS:
    if src.count(old) != 1:
        print('MISS (%d): %s' % (src.count(old), old[:110]))
        continue
    src = src.replace(old, new)
    applied += 1

open(PATH, 'w', encoding='utf-8', newline='').write(src)
print('v107b applied: %d/%d edits' % (applied, len(EDITS)))
