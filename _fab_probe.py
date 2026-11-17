# -*- coding: utf-8 -*-
"""Measure whether the floating buttons cover any interactive control, at two widths."""
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out = sys.argv[2] if len(sys.argv) > 2 else '_fab.html'

PROBE = r"""
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[];
  function rec(s){log.push(s);}
  function $(i){return document.getElementById(i);}
  function R(el){var r=el.getBoundingClientRect();return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height};}
  function f(n){return Math.round(n*10)/10;}
  function show(r){return f(r.l)+','+f(r.t)+','+f(r.r)+','+f(r.b)+' ('+f(r.w)+'x'+f(r.h)+')';}
  function overlaps(a,b){return !(a.r<=b.l+0.5||b.r<=a.l+0.5||a.b<=b.t+0.5||b.b<=a.t+0.5);}
  function visible(el){if(!el)return false;var s=getComputedStyle(el);
    return s.display!=='none'&&s.visibility!=='hidden'&&parseFloat(s.opacity)!==0&&el.getClientRects().length>0;}
  window.addEventListener('load',function(){
    var raf=window.requestAnimationFrame;window.requestAnimationFrame=function(cb){cb();return 0;};
    try{document.querySelectorAll('.cs-dd').forEach(function(d){d.style.display='none';});}catch(e){}
    var fabs=[$('fabH'),$('fabS')].filter(visible);
    rec('viewport '+window.innerWidth+'x'+window.innerHeight+
        '  docScrollH='+document.documentElement.scrollHeight+
        '  bodyScrollH='+document.body.scrollHeight);
    fabs.forEach(function(fb){
      var st=getComputedStyle(fb);
      rec('fab '+fb.id+' '+show(R(fb))+'  position='+st.position+'  z='+st.zIndex+
          '  right='+st.right+' bottom='+st.bottom);
    });
    var ctrls=[].slice.call(document.querySelectorAll(
      'button,input:not([type=hidden]),textarea,select,.chip,.tab,.cs-btn')).filter(visible);
    fabs.forEach(function(fb){
      var hit=ctrls.filter(function(c){return overlaps(R(fb),R(c));});
      rec('fab '+fb.id+' overlaps '+hit.length+' control(s): '+
          hit.map(function(c){return (c.id||c.getAttribute('data-i')||c.className||c.tagName)+'@'+show(R(c));}).join(' | '));
    });
    var wrap=document.querySelector('.wrap');
    rec('wrap '+show(R(wrap))+' paddingBottom='+getComputedStyle(wrap).paddingBottom+
        ' bodyPaddingBottom='+getComputedStyle(document.body).paddingBottom);
    function sweep(tag){
      fabs.forEach(function(fb){
        var hit=ctrls.filter(function(c){return overlaps(R(fb),R(c));});
        rec(tag+' fab '+fb.id+' overlaps '+hit.length+': '+
            hit.map(function(c){return (c.id||c.className||c.tagName)+'@'+show(R(c));}).join(' | '));
      });
    }
    sweep('top');
    window.scrollTo(0,document.documentElement.scrollHeight);
    rec('after scrollTo bottom scrollY='+window.scrollY);
    sweep('bottom');
  });
  document.title='x';
  window.addEventListener('load',function(){setTimeout(function(){$('probeOut').textContent=log.join('\n');},0);});
})();
</script>
</body>"""

s = open(src, encoding='utf-8', newline='').read()
assert s.count('</body>') == 1
s = s.replace('</body>', PROBE.replace('\n', '\r\n'))
open(out, 'w', encoding='utf-8', newline='').write(s)
print('wrote %s (bytes=%d)' % (out, len(s)))
