# -*- coding: utf-8 -*-
"""v2026.10.01.5 patch, part 3: make the settle re-placement self-verifying.

A single re-placement is not enough: `animationend` can fire before the final frame
is laid out, and the button keeps moving while the panel slides. Check whether the
menu is still glued to its button a few times and re-place it whenever it is not;
once it matches, nothing is written, so a settled open never jitters.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PATH = 'letter-polisher.html'
NL = '\r\n'
src = open(PATH, encoding='utf-8', newline='').read()

OLD = """function csSettleFix(btn,dd,cs){
  var done=function(){
    cs.removeEventListener('animationend',done);
    cs.removeEventListener('transitionend',done);
    if(dd&&dd.classList.contains('open')&&document.body.contains(dd))csPlaceMenu(btn,dd);
  };
  cs.addEventListener('animationend',done);
  cs.addEventListener('transitionend',done);
  setTimeout(done,420);
}"""

NEW = """function csSettleFix(btn,dd,cs){
  var delays=[120,300,520,760],i=0;
  function verify(){
    if(!dd||!dd.classList.contains('open')||!document.body.contains(dd))return;
    var a=dd.getBoundingClientRect(),b=btn.getBoundingClientRect();
    if(Math.abs(a.left-b.left)>1.5||Math.abs(a.top-b.top)>1.5)csPlaceMenu(btn,dd);
    if(i<delays.length)setTimeout(verify,delays[i++]);
  }
  cs.addEventListener('animationend',verify);
  cs.addEventListener('transitionend',verify);
  verify();
}"""

old = OLD.replace('\n', NL)
new = NEW.replace('\n', NL)
assert src.count(old) == 1, 'csSettleFix body not found'
src = src.replace(old, new)
open(PATH, 'w', encoding='utf-8', newline='').write(src)
print('ok csSettleFix is self-verifying; bytes=%d' % len(src.encode('utf-8')))
