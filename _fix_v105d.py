# -*- coding: utf-8 -*-
"""csSettleFix: detach its listeners once the re-placement chain is done."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8', newline='')
p = 'letter-polisher.html'
raw = io.open(p, encoding='utf-8', newline='').read()

old = """function csSettleFix(btn,dd,cs){
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
}""".replace('\n', '\r\n')

new = """function csSettleFix(btn,dd,cs){
  var delays=[120,300,520,760],i=0;
  function off(){cs.removeEventListener('animationend',verify);cs.removeEventListener('transitionend',verify);}
  function verify(){
    if(!dd||!dd.classList.contains('open')||!document.body.contains(dd)){off();return;}
    var a=dd.getBoundingClientRect(),b=btn.getBoundingClientRect();
    if(Math.abs(a.left-b.left)>1.5||Math.abs(a.top-b.top)>1.5)csPlaceMenu(btn,dd);
    if(i<delays.length)setTimeout(verify,delays[i++]);else off();
  }
  cs.addEventListener('animationend',verify);
  cs.addEventListener('transitionend',verify);
  verify();
}""".replace('\n', '\r\n')

assert raw.count(old) == 1, raw.count(old)
raw = raw.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8', newline='').write(raw)
print('ok csSettleFix detaches its listeners when done')
