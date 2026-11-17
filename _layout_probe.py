# -*- coding: utf-8 -*-
"""Layout probe for the collapsed connection block.

Builds `_layout.html` (a copy of the app with a synchronous probe appended) and
prints the geometry of every row of #provEditBox once it is opened, so the
"optimised, tidy arrangement" of the URL / key / model / temperature rows is
measured instead of eyeballed.

Usage: python _layout_probe.py [src] [out]
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out = sys.argv[2] if len(sys.argv) > 2 else '_layout.html'

PROBE = r"""
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[],fails=0;
  function rec(s){log.push(s);}
  function check(n,c,x){if(!c)fails++;rec((c?'PASS ':'FAIL ')+n+(x?'  '+x:''));}
  function $(i){return document.getElementById(i);}
  function click(el){el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));}
  function R(el){var r=el.getBoundingClientRect();return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height};}
  function f(n){return Math.round(n*10)/10;}
  function show(r){return f(r.l)+','+f(r.t)+','+f(r.r)+','+f(r.b)+' ('+f(r.w)+'x'+f(r.h)+')';}
  function settleAnim(){
    try{
      document.querySelector('#sOv .panel').getAnimations().forEach(function(a){try{a.finish();}catch(e){}});
    }catch(e){}
    void document.body.offsetWidth;
  }
  /* .btn carries `transition:all .18s`, so a computed colour read right after a
     click is the START of the transition - finish the animations first. */
  function settleEl(el){
    try{el.getAnimations({subtree:true}).forEach(function(a){try{a.finish();}catch(e){}});}catch(e){}
    void document.body.offsetWidth;
  }
  window.addEventListener('load',function(){
    try{
      var g=$('guideOv');if(g)g.classList.remove('open');
      $('sOv').classList.add('open');
      var raf=window.requestAnimationFrame;
      window.requestAnimationFrame=function(cb){cb();return 0;};
      settleAnim();
      var box=$('provEditBox');
      if(!box){rec('FAIL no #provEditBox');rec('RESULT fails=1');$('probeOut').textContent=log.join('\n');return;}
      check('block hidden before add/edit',R(box).h===0||getComputedStyle(box).display==='none',
            'display='+getComputedStyle(box).display);
      var eb=$('provEditBtn');
      check('the edit button exists outside the block',!!eb&&!box.contains(eb));
      var bgOff=eb?getComputedStyle(eb).backgroundColor:'';
      var b=eb||document.querySelector('[onclick="newProvider()"]');
      click(b);
      settleAnim();
      check('block visible after the click',getComputedStyle(box).display!=='none','display='+getComputedStyle(box).display);
      if(eb){
        settleEl(eb);
        check('the edit button shows an active state while the block is open',
              eb.classList.contains('on')&&getComputedStyle(eb).backgroundColor!==bgOff,
              'off='+bgOff+' on='+getComputedStyle(eb).backgroundColor);
      }

      var pb=document.querySelector('#sOv .panel-body'),pbr=R(pb),br=R(box);
      check('block fits the panel width horizontally',br.l>=pbr.l-0.5&&br.r<=pbr.r+0.5,
            'block='+show(br)+' panel='+show(pbr));
      check('block has a visible frame',parseFloat(getComputedStyle(box).borderTopWidth)>0&&br.w>200,'w='+f(br.w));

      var rows=[].slice.call(box.children).filter(function(n){return n.classList.contains('prow')||n.classList.contains('btns');});
      check('block has six rows (name, url+key, model, format, temperature, actions)',rows.length===6,'n='+rows.length);
      var head=box.querySelector('.pe-h');
      check('block opens with its section header above the first row',
            !!head&&Math.abs(R(head).l-R(box).l-12)<3&&R(head).b<=R(rows[0]).t+0.5,
            'head='+(head?show(R(head)):'-')+' firstRowTop='+f(R(rows[0]).t));
      var order=rows.map(function(n){var i=n.querySelector('input[id],button');return i?(i.id||i.getAttribute('onclick')||i.textContent.trim().slice(0,10)):'?';});
      rec('(info) row order: '+order.join(' | '));

      /* every row inside the block, no horizontal overflow */
      var over=rows.filter(function(n){var r=R(n);return r.l<br.l-0.5||r.r>br.r+0.5;});
      check('no row overflows the block',over.length===0,'n='+over.length);

      /* the URL / API key row is a real two-column row */
      var urlRow=$('apiUrl').closest('.prow'),keyRow=$('apiKey').closest('.prow');
      check('url and key share one row',urlRow===keyRow);
      var u=R($('apiUrl')),k=R($('apiKey'));
      check('url and key sit side by side',Math.abs(u.t-k.t)<1.5&&k.l>u.r,'url='+show(u)+' key='+show(k));
      check('url and key are balanced widths',Math.abs(u.w-k.w)<=3,'urlW='+f(u.w)+' keyW='+f(k.w));
      check('key field leaves room for the eye button',k.r<br.r-8,'keyRight='+f(k.r)+' blockRight='+f(br.r));

      /* single-column rows fill the width consistently */
      var single=[$('provName'),$('modelName'),$('temperature')].map(function(el){return R(el);});
      single.forEach(function(r,i){
        check('single-column row '+(i+1)+' spans the block interior',r.w>br.w*0.5&&r.r<=br.r-8,
              'w='+f(r.w)+' blockW='+f(br.w));
      });
      check('the single-column rows start at the same left edge',
            Math.abs(single[0].l-single[1].l)<1.5&&Math.abs(single[0].l-single[2].l)<1.5,
            single.map(function(r){return f(r.l);}).join(','));

      /* vertical rhythm: even, positive gaps, actions last */
      var tops=rows.map(function(n){return R(n);});
      var gaps=[];for(var i=1;i<tops.length;i++)gaps.push(f(tops[i].t-tops[i-1].b));
      check('row gaps are positive and even enough',gaps.every(function(g){return g>=-0.5&&g<=16;}),
            'gaps='+gaps.join(','));
      var temp=R($('temperature')),save=R(box.querySelector('[onclick="saveProviderEdit()"]'));
      check('temperature sits above the save/cancel row',temp.b<=save.t+0.5,'tempBottom='+f(temp.b)+' saveTop='+f(save.t));
      var cancel=R(box.querySelector('[onclick="cancelProviderEdit()"]'));
      check('save is left of cancel and they share a line',save.l<cancel.l&&Math.abs(save.t-cancel.t)<1.5);
      check('temperature field is not clipped',temp.b<=br.b+0.5,'tempBottom='+f(temp.b)+' blockBottom='+f(br.b));
      check('block ends below the last row',br.b>save.b,'blockBottom='+f(br.b)+' saveBottom='+f(save.b));

      window.requestAnimationFrame=raf;
    }catch(e){rec('ERR '+e.message+' @ '+(e.stack||'').split('\n')[1]);fails++;}
    rec('RESULT fails='+fails);
    $('probeOut').textContent=log.join('\n');
  });
})();
</script>
</body>"""

s = open(src, encoding='utf-8', newline='').read()
assert '<div id="probeOut"' not in s, 'source already contains a probe'
assert s.count('</body>') == 1
s = s.replace('</body>', PROBE.replace('\n', '\r\n'))
open(out, 'w', encoding='utf-8', newline='').write(s)
print('wrote %s from %s (domlen=%d)' % (out, src, len(s)))
