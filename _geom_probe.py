# -*- coding: utf-8 -*-
"""Build _geom.html: dump the real geometry of the settings overlay and the
provider controls, so panel/zoom/overflow effects can be told apart."""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROBE = r'''
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[];
  function rec(s){log.push(s);}
  function $(i){return document.getElementById(i);}
  function r(el){if(!el)return 'null';var b=el.getBoundingClientRect();
    return 'x='+b.left.toFixed(1)+' y='+b.top.toFixed(1)+' w='+b.width.toFixed(1)+' h='+b.height.toFixed(1)+' r='+b.right.toFixed(1);}
  function cs(el,p){return el?getComputedStyle(el)[p]:'-';}
  window.addEventListener('load',function(){
    try{
      var g=$('guideOv');if(g)g.classList.remove('open');
      $('sOv').classList.add('open');
      rec('innerWidth/innerHeight = '+innerWidth+'x'+innerHeight);
      rec('doc.scrollWidth='+document.documentElement.scrollWidth+' body.scrollWidth='+document.body.scrollWidth);
      rec('documentElement '+r(document.documentElement));
      rec('body '+r(document.body)+'  zoom='+cs(document.body,'zoom')+' transform='+cs(document.body,'transform'));
      rec('html zoom='+cs(document.documentElement,'zoom')+'  appZoom var='+getComputedStyle(document.documentElement).getPropertyValue('--zoom'));
      rec('#sOv '+r($('sOv'))+'  display='+cs($('sOv'),'display')+' justify='+cs($('sOv'),'justifyContent')+' zoom='+cs($('sOv'),'zoom'));
      rec('#sOv children = '+[].slice.call($('sOv').children).map(function(n){return n.className||n.tagName;}).join(' | '));
      var p=document.querySelector('#sOv .panel');
      rec('.panel '+r(p)+'  zoom='+cs(p,'zoom')+' transform='+cs(p,'transform')+' anim='+cs(p,'animationName'));
      var pb=document.querySelector('#sOv .panel-body');
      rec('.panel-body '+r(pb)+'  scrollTop='+pb.scrollTop+' scrollW='+pb.scrollWidth+' clientW='+pb.clientWidth);
      rec('.ps (provider) '+r(document.querySelector('#provCS').closest('.ps')));
      rec('#provCS '+r($('provCS')));
      rec('#provCS .cs-btn '+r(document.querySelector('#provCS .cs-btn')));
      rec('#provEditBox '+r($('provEditBox'))+'  display='+cs($('provEditBox'),'display'));
      rec('#apiUrl '+r($('apiUrl')));
      rec('#provCur '+r($('provCur')));
      rec('body font-size='+cs(document.body,'fontSize'));
      $('probeOut').textContent=log.join('\n');
    }catch(e){rec('ERR '+e.message+' @'+e.lineno);$('probeOut').textContent=log.join('\n');}
  });
})();
</script>
'''

src_path = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out_path = sys.argv[2] if len(sys.argv) > 2 else '_geom.html'
src = open(src_path, encoding='utf-8', newline='').read()
i = src.rfind('</body>')
open(out_path, 'w', encoding='utf-8', newline='').write(src[:i] + PROBE + src[i:])
print('wrote %s from %s' % (out_path, src_path))
