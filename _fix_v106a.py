# -*- coding: utf-8 -*-
"""v2026.10.02: put each custom field directly under the selector that opens it.

1. #custTone moves inside .opts-grid, right after the tone .fg and before the
   purpose .fg, so it reads: 潤飾風格 -> custom input -> 信件用途.
2. #custPurp moves inside .opts-grid right after the purpose .fg (same idea).
3. Both become full-width sub-panels with the accent tint used for "selected".
4. Picking 自訂風格… focuses the new input and keeps it in view.
"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
P = 'letter-polisher.html'
s = io.open(P, encoding='utf-8', newline='').read()
orig = s
NL = '\r\n'

CUST_TONE = ('        <div class="cust" id="custTone">'
             '<label data-i="customToneLabel"></label>'
             '<input type="text" id="customToneVal" placeholder="">'
             '<div class="cust-h" data-i="customToneHint"></div></div>')
CUST_PURP = ('        <div class="cust" id="custPurp">'
             '<label data-i="customPurpLabel"></label>'
             '<input type="text" id="customPurpVal" placeholder="">'
             '<div class="cust-h" data-i="customPurpHint"></div></div>')

# ---------- 1. grid order + sub-panel styling ----------
old_css = ('.opts-grid>.fg:has(#toneCS){order:5;}' + NL +
           '.opts-grid>.fg:has(#polishModeCS){order:6;}' + NL +
           '.opts-grid>.fg:has(#purposeCS){order:7;grid-column:1/-1;}')
new_css = ('.opts-grid>.fg:has(#toneCS){order:5;}' + NL +
           '.opts-grid>#custTone{order:6;}' + NL +
           '.opts-grid>.fg:has(#polishModeCS){order:7;}' + NL +
           '.opts-grid>.fg:has(#purposeCS){order:8;grid-column:1/-1;}' + NL +
           '.opts-grid>#custPurp{order:9;}' + NL +
           '/* The custom fields sit in the grid so each one opens right under the' + NL +
           '   selector that shows it, as a full-width sub-panel of that field. */' + NL +
           '.opts-grid>.cust{' + NL +
           '  grid-column:1/-1;margin-bottom:0;padding:10px 12px 9px;' + NL +
           '  border:0.5px solid rgba(var(--ac-rg),.22);border-radius:var(--r2);' + NL +
           '  background:rgba(var(--ac-rg),.05);' + NL +
           '}' + NL +
           '.opts-grid>.cust>label{color:var(--ac);margin-bottom:5px;}' + NL +
           '.opts-grid>.cust input{background:var(--sf);border-color:rgba(var(--ac-rg),.18);}' + NL +
           '.opts-grid>.cust .cust-h{color:var(--tx2);}')
assert s.count(old_css) == 1, 'grid order block not found'
s = s.replace(old_css, new_css, 1)

# ---------- 2. move #custTone under the tone field ----------
tone_anchor = ('          <input type="hidden" id="tone">' + NL +
               '        </div>' + NL +
               '      </div>' + NL)
assert s.count(tone_anchor) == 1, 'tone .fg close not found'
s = s.replace(tone_anchor, tone_anchor + CUST_TONE + NL, 1)

# ---------- 3. move #custPurp under the purpose field ----------
purp_anchor = ('          <input type="hidden" id="purpose">' + NL +
               '        </div>' + NL +
               '      </div>' + NL)
assert s.count(purp_anchor) == 1, 'purpose .fg close not found'
s = s.replace(purp_anchor, purp_anchor + CUST_PURP + NL, 1)

# ---------- 4. drop the old stacked copies ----------
old_stack = ('    <!-- Custom inputs (hidden by default) -->' + NL +
             CUST_TONE.replace('        ', '    ', 1) + NL +
             CUST_PURP.replace('        ', '    ', 1) + NL)
assert s.count(old_stack) == 1, 'old stacked custom inputs not found'
s = s.replace(old_stack, '', 1)

# ---------- 5. reveal + focus ----------
old_ch = ("function onToneCh(){v('tone')==='custom'?$('custTone').classList.add('show'):$('custTone').classList.remove('show');}" + NL +
          "function onPurpCh(){v('purpose')==='custom-purpose'?$('custPurp').classList.add('show'):$('custPurp').classList.remove('show');}")
new_ch = ("function custReveal(boxId,inputId,on,focus){" + NL +
          "  var box=$(boxId);if(!box)return;" + NL +
          "  box.classList.toggle('show',on);" + NL +
          "  if(!on||!focus)return;" + NL +
          "  var f=$(inputId);if(f)f.focus({preventScroll:true});" + NL +
          "  if(box.scrollIntoView)box.scrollIntoView({block:'nearest'});" + NL +
          "}" + NL +
          "function onToneCh(focus){custReveal('custTone','customToneVal',v('tone')==='custom',focus);}" + NL +
          "function onPurpCh(focus){custReveal('custPurp','customPurpVal',v('purpose')==='custom-purpose',focus);}")
assert s.count(old_ch) == 1, 'onToneCh/onPurpCh not found'
s = s.replace(old_ch, new_ch, 1)

old_pick = ("  else if(id==='tone'){LO.tone=val;onToneCh();}" + NL +
            "  else if(id==='purpose'){LO.purpose=val;onPurpCh();}")
new_pick = ("  else if(id==='tone'){LO.tone=val;onToneCh(1);}" + NL +
            "  else if(id==='purpose'){LO.purpose=val;onPurpCh(1);}")
assert s.count(old_pick) == 1, 'csLetterOptPick hooks not found'
s = s.replace(old_pick, new_pick, 1)

assert s != orig
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('v106a applied: custom fields now open under their own selector')
