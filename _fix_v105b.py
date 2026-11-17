# -*- coding: utf-8 -*-
"""v2026.10.01.5 patch, part 2: temperature belongs to the connection block, and a
menu opened while the settings panel is still sliding must be re-placed once the
slide has settled - otherwise it keeps the offset of the moving button."""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PATH = 'letter-polisher.html'
NL = '\r\n'
src = open(PATH, encoding='utf-8', newline='').read()


def sub(old, new, label, count=1):
    global src
    o = old.replace('\n', NL)
    n = new.replace('\n', NL)
    found = src.count(o)
    assert found == count, '%s: found %d, expected %d' % (label, found, count)
    src = src.replace(o, n)
    print('ok %s' % label)


CHECK_SVG = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
             'stroke-linejoin="round"><path d="M3.2 8.6l3.1 3.1L12.8 5"/></svg>')
SAVE_BTN = ('<button class="btn btn-p btn-sm" type="button" onclick="saveProviderEdit()">' + CHECK_SVG +
            '<span data-i="provSave"></span></button>')
CANCEL_BTN = ('<button class="btn btn-s btn-sm" type="button" onclick="cancelProviderEdit()">'
              '<span data-i="provCancel"></span></button>')
TEMP_ROW = ('<div class="prow one"><div class="fg"><label data-i="temperature"></label>'
            '<input type="number" id="temperature" value="0.7" min="0" max="2" step="0.1"></div></div>')

# temperature moves inside the block, ABOVE the save / cancel buttons, so one
# block = one connection setting (it is stored per provider).
sub(
    '<div class="btns">' + SAVE_BTN + CANCEL_BTN + '</div></div>' + TEMP_ROW + '</div>',
    TEMP_ROW + '<div class="btns">' + SAVE_BTN + CANCEL_BTN + '</div></div></div>',
    'temperature inside the block')

# a menu opened while the panel slides in is re-placed once the slide has settled
sub(
    'function csPlaceMenu(btn,dd){',
    """/* The settings panel slides in for .28s (transform:translateX(500px) -> 0) and
   every control inside travels with it. A menu opened during the slide is placed
   from the button's *moving* rectangle and keeps that offset once the panel has
   arrived - the classic "opens, jumps, cannot be seen". Re-place it the moment the
   slide / fade settles, and once more defensively after a short delay. */
function csSettleFix(btn,dd,cs){
  var done=function(){
    cs.removeEventListener('animationend',done);
    cs.removeEventListener('transitionend',done);
    if(dd&&dd.classList.contains('open')&&document.body.contains(dd))csPlaceMenu(btn,dd);
  };
  cs.addEventListener('animationend',done);
  cs.addEventListener('transitionend',done);
  setTimeout(done,420);
}
function csPlaceMenu(btn,dd){""",
    'csSettleFix helper')

sub(
    "  if(btn.closest('.panel-body'))csPlaceMenu(btn,dd);\n"
    "  dd.classList.add('open');btn.classList.add('open');",
    "  if(btn.closest('.panel-body')){csPlaceMenu(btn,dd);csSettleFix(btn,dd,btn.closest('.cs')||dd.parentElement);}\n"
    "  dd.classList.add('open');btn.classList.add('open');",
    'csToggle wires csSettleFix')

open(PATH, 'w', encoding='utf-8', newline='').write(src)
print('written; bytes=%d' % len(src.encode('utf-8')))
