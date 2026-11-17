# -*- coding: utf-8 -*-
"""Print the visual order of the input-card fields (label, grid order, position)."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out = sys.argv[2] if len(sys.argv) > 2 else '_order.html'

PROBE = r"""
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[];
  function $(i){return document.getElementById(i);}
  function R(el){var r=el.getBoundingClientRect();return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height};}
  function f(n){return Math.round(n*10)/10;}
  window.addEventListener('load',function(){
    var raf=window.requestAnimationFrame;window.requestAnimationFrame=function(cb){cb();return 0;};
    /* open both custom fields the way the app does */
    function pick(id,val){
      var dd=$(id).parentNode;
      var opt=dd.querySelector('.cs-opt[data-val="'+val+'"]');
      if(opt)csPick(opt);
    }
    pick('toneCS','custom');
    pick('purposeCS','custom-purpose');
    var grid=$('toneCS').closest('.opts-grid')||document.querySelector('.opts-grid');
    log.push('grid columns='+getComputedStyle(grid).gridTemplateColumns);
    log.push('scroller overflowY='+getComputedStyle(document.querySelector('.wrap')).overflowY);
    var kids=[].slice.call(grid.children);
    log.push('DOM order: '+kids.map(function(k){
      var id=k.id||(k.querySelector('[id]')?k.querySelector('[id]').id:'?');
      return id+'(order='+getComputedStyle(k).order+')';
    }).join(' > '));
    var rows=kids.map(function(k){
      var lb=k.querySelector('label,.fg>label,label');
      var txt=(lb?lb.textContent:k.textContent).replace(/\s+/g,'').slice(0,14);
      var r=R(k);
      return {txt:txt,l:r.l,t:r.t,b:r.b,w:r.w,h:r.h,vis:k.offsetParent!==null};
    }).filter(function(o){return o.h>0;});
    rows.sort(function(a,b){return (Math.abs(a.t-b.t)>6)? a.t-b.t : a.l-b.l;});
    rows.forEach(function(o){
      log.push('  '+f(o.l)+','+f(o.t)+'  '+f(o.w)+'x'+f(o.h)+'  '+o.txt+(o.vis?'':'  [hidden]'));
    });
    var tone=R($('toneCS').closest('.fg')), ct=R($('custTone')), pur=R($('purposeCS').closest('.fg'));
    log.push('tone.fg bottom='+f(tone.b)+'  custTone top='+f(ct.t)+'  custTone left='+f(ct.l)+
             ' w='+f(ct.w)+'  purpose top='+f(pur.t));
    log.push('custTone directly under tone: '+(ct.t>=tone.b-1 && ct.t-tone.b<20));
    log.push('custTone above purpose: '+(ct.t<pur.t));
    log.push('same column as tone: '+(Math.abs(ct.l-tone.l)<2));
  });
  window.addEventListener('load',function(){setTimeout(function(){$('probeOut').textContent=log.join('\n');},0);});
})();
</script>
</body>"""

s = io.open(src, encoding='utf-8', newline='').read()
assert s.count('</body>') == 1
s = s.replace('</body>', PROBE.replace('\n', '\r\n'))
io.open(out, 'w', encoding='utf-8', newline='').write(s)
print('wrote %s' % out)
