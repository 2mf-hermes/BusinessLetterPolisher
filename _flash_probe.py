# -*- coding: utf-8 -*-
"""Build _flash.html: the current app plus an instrumented probe that opens the
settings sheet, clicks the AI provider dropdown and records who closes it, plus
where the menu actually renders over the following second."""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROBE = r'''
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[];
  function rec(s){log.push(s);}
  window.addEventListener('load',function(){
    setTimeout(function(){
      try{
        document.getElementById('sOv').classList.add('open');
        var pb=document.querySelector('#sOv .panel-body');
        var btn=document.querySelector('#provCS .cs-btn');
        var dd=document.getElementById('provDD');
        pb.scrollTop=Math.max(0,btn.offsetTop-pb.clientHeight/2);
        rec('panel-body scrollTop='+Math.round(pb.scrollTop)+' clientH='+pb.clientHeight+' scrollH='+pb.scrollHeight);
        pb.addEventListener('scroll',function(){rec('EV scroll on panel-body');},true);
        document.addEventListener('scroll',function(e){rec('EV scroll target='+(e.target===document?'document':(e.target.className||e.target.tagName)));},true);
        window.addEventListener('resize',function(){rec('EV resize');});
        var oc=window.csCloseAll;
        window.csCloseAll=function(){rec('CLOSE: '+((new Error()).stack||'').split('\n').slice(1,5).join(' | '));return oc.apply(window,arguments);};
        var op=window.csPlaceMenu;
        window.csPlaceMenu=function(b,d){op.apply(window,arguments);rec('PLACE btn='+(b.id||b.className)+' dd='+(d.id||d.className));};
        btn.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
        rec('right after click: open='+dd.classList.contains('open')+' inlinePos='+dd.style.position+' left='+dd.style.left+' top='+dd.style.top+' w='+dd.style.width);
        var shots=[0,60,200,600,1200];
        shots.forEach(function(ms){
          setTimeout(function(){
            var pr=document.querySelector('#sOv .panel').getBoundingClientRect();
            var r=dd.getBoundingClientRect(),st=getComputedStyle(dd);
            var clipped=(r.bottom<pr.top||r.top>pr.bottom||r.left>pr.right||r.right<pr.left);
            rec('t+'+ms+'ms open='+dd.classList.contains('open')+' rect='+[r.left,r.top,r.width,r.height].map(Math.round).join(',')
                +' opacity='+st.opacity+' pos='+st.position+' visible='+st.visibility+' clippedByPanel='+clipped
                +' panel='+[pr.left,pr.top,pr.right,pr.bottom].map(Math.round).join(','));
          },ms);
        });
        setTimeout(function(){document.getElementById('probeOut').textContent=log.join('\n');},1700);
      }catch(e){document.getElementById('probeOut').textContent='ERR '+e.message+'\n'+e.stack;}
    },300);
  });
})();
</script>
'''

src = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = src.rfind('</body>')
if i < 0:
    print('FAIL: no </body>')
    sys.exit(1)
out = src[:i] + PROBE + src[i:]
open('_flash.html', 'w', encoding='utf-8', newline='').write(out)
print('wrote _flash.html (%d chars)' % len(out))
