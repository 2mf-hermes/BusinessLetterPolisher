# -*- coding: utf-8 -*-
"""Humane-layout audit probe for the input card.

Builds `_ui_audit.html` (a copy of the app with a synchronous probe appended) and
measures, in a real browser with CSS transitions left ON, whether the option
fields read in a sane order and whether each custom field opens right under the
selector that reveals it.

Usage: python _ui_audit.py [src] [out]
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out = sys.argv[2] if len(sys.argv) > 2 else '_ui_audit.html'

PROBE = r"""
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[],fails=0;
  function rec(s){log.push(s);}
  function check(n,c,x){if(!c)fails++;rec((c?'PASS ':'FAIL ')+n+(x?'  '+x:''));}
  function info(s){rec('(info) '+s);}
  function $(i){return document.getElementById(i);}
  function R(el){var r=el.getBoundingClientRect();return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height};}
  function f(n){return Math.round(n*10)/10;}
  function show(r){return f(r.l)+','+f(r.t)+','+f(r.r)+','+f(r.b)+' ('+f(r.w)+'x'+f(r.h)+')';}
  function settle(el){
    try{(el||document.body).getAnimations({subtree:true}).forEach(function(a){try{a.finish();}catch(e){}});}catch(e){}
    void document.body.offsetWidth;
  }
  function pick(scope,val){
    var o=document.querySelector(scope+' .cs-opt[data-val="'+val+'"]');
    if(!o){rec('ERR no option '+val+' in '+scope);fails++;return false;}
    o.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
    return true;
  }
  function overlaps(a,b){return !(a.r<=b.l+0.5||b.r<=a.l+0.5||a.b<=b.t+0.5||b.b<=a.t+0.5);}
  function focusables(root){
    return [].slice.call(root.querySelectorAll('button,input:not([type=hidden]),textarea,[tabindex]:not([tabindex="-1"])'))
      .filter(function(el){var s=getComputedStyle(el);return s.display!=='none'&&s.visibility!=='hidden'&&el.offsetParent!==null&&!el.disabled;});
  }
  var GRID=['letterLangCS','outLangCS','srcRegionCS','outRegionCS','toneCS','polishModeCS','custTone','purposeCS','custPurp'];
  function gridNode(id){return id.indexOf('cust')===0?$(id):$(id).closest('.fg');}
  function gapAfter(a,b){return f(R(b).t-Math.max(R(a).b,0));}

  window.addEventListener('load',function(){
    try{
      var g=$('guideOv');if(g)g.classList.remove('open');
      var raf=window.requestAnimationFrame;
      window.requestAnimationFrame=function(cb){cb();return 0;};
      settle();
      var grid=document.querySelector('.opts-grid');
      var card=document.querySelector('.card-inp');
      var narrow=window.innerWidth<620;
      var box=$('custTone'),pbox=$('custPurp'),ta=$('letterIn');
      var toneFg=gridNode('toneCS'),modeFg=gridNode('polishModeCS'),purposeFg=gridNode('purposeCS');
      info('viewport '+window.innerWidth+'x'+window.innerHeight+'  singleColumn='+narrow);

      /* ---- 1. restore path: a saved custom choice reopens its field, without
              stealing focus (the app must not hijack the caret on start) ---- */
      LO.tone='custom';LO.purpose='custom-purpose';
      fillLetterOpts();settle(box);settle(pbox);
      check('a saved custom style reopens its field on start',getComputedStyle(box).display!=='none',
            'display='+getComputedStyle(box).display);
      check('a saved custom purpose reopens its field on start',getComputedStyle(pbox).display!=='none',
            'display='+getComputedStyle(pbox).display);
      check('restoring on start does not steal the caret',
            !document.activeElement||document.activeElement===document.body,
            'active='+(document.activeElement?(document.activeElement.id||document.activeElement.tagName):'-'));

      /* ---- 1b. baseline: closed custom fields take no space ---- */
      pick('#toneCS','professional');pick('#purposeCS','general');settle();
      check('a preset style keeps the custom field closed',getComputedStyle(box).display==='none',
            'display='+getComputedStyle(box).display);
      check('a preset purpose keeps the custom field closed',getComputedStyle(pbox).display==='none',
            'display='+getComputedStyle(pbox).display);
      var closedGap=f(R(purposeFg).t-Math.max(R(toneFg).b,R(modeFg).b));
      check('closed custom fields leave only the normal row gap',
            closedGap>=-0.5&&closedGap<=18,'gap='+closedGap);

      /* ---- 2. reveal the style field: it opens under 潤飾風格, above 信件用途 ---- */
      pick('#toneCS','custom');
      settle(box);
      var rb=R(box),tb=R(toneFg),mb=R(modeFg),pb=R(purposeFg);
      check('custom style field opens below the style row',rb.t>=Math.max(tb.b,mb.b)-1,
            'boxTop='+f(rb.t)+' styleRowBottom='+f(Math.max(tb.b,mb.b)));
      check('custom style field sits above the purpose field',rb.b<=pb.t+1,
            'boxBottom='+f(rb.b)+' purposeTop='+f(pb.t));
      check('custom style field spans the whole row',Math.abs(rb.w-pb.w)<2,
            'boxW='+f(rb.w)+' purposeW='+f(pb.w));
      check('custom style field is a framed sub-panel',
            parseFloat(getComputedStyle(box).borderTopWidth)>0,
            'border='+getComputedStyle(box).borderTopWidth);
      check('opening the field puts the caret in it',
            document.activeElement&&document.activeElement.id==='customToneVal',
            'active='+(document.activeElement?(document.activeElement.id||document.activeElement.tagName):'-'));
      var cinput=$('customToneVal'),ci=R(cinput);
      check('the custom input fills the panel and is not clipped',
            ci.r<=rb.r-8&&ci.l>=rb.l+8,'input='+show(ci)+' panel='+show(rb));
      check('the custom input is inside the viewport',ci.t>=0&&ci.b<=window.innerHeight,
            'inputTop='+f(ci.t)+' viewportH='+window.innerHeight);
      check('the open field does not overlap the purpose field',!overlaps(rb,pb));

      /* ---- 3. reveal the purpose field the same way ---- */
      pick('#purposeCS','custom-purpose');
      settle(pbox);
      var qb=R(pbox),qpg=R(purposeFg);
      check('custom purpose field opens below the purpose field',qb.t>=qpg.b-1,
            'boxTop='+f(qb.t)+' purposeBottom='+f(qpg.b));
      check('custom purpose field sits above the letter textarea',qb.b<=R(ta).t+1,
            'boxBottom='+f(qb.b)+' taTop='+f(R(ta).t));
      check('custom purpose field spans the whole row',Math.abs(qb.w-qpg.w)<2,
            'boxW='+f(qb.w)+' purposeW='+f(qpg.w));

      /* ---- 4. structure with everything visible ---- */
      var nodes=GRID.map(gridNode);
      var rects=nodes.map(R);
      info('visual order: '+GRID.map(function(id,i){return id+'@'+f(rects[i].t)+','+f(rects[i].l);}).join(' | '));
      var sorted=rects.slice().sort(function(a,b){return (a.t-b.t)||(a.l-b.l);});
      var sameOrder=rects.every(function(r,i){return Math.abs(r.t-sorted[i].t)<1.5&&Math.abs(r.l-sorted[i].l)<1.5;});
      check('DOM order equals visual order (reading order = tab order)',sameOrder,
            'domTops='+rects.map(function(r){return f(r.t);}).join(','));
      var fos=focusables(grid),fseq=fos.map(R),monotone=true;
      for(var q=1;q<fseq.length;q++){
        var prev=fseq[q-1],cur=fseq[q];
        if(cur.t<prev.t-1.5)monotone=false;
        if(Math.abs(cur.t-prev.t)<1.5&&cur.l<prev.l-1.5)monotone=false;
      }
      check('tab order inside the grid matches the visual order',monotone,'focusables='+fos.length);
      check('the style row stays directly above the custom field',
            rb.t-Math.max(tb.b,mb.b)<=18&&rb.t>=Math.max(tb.b,mb.b)-1,'gap='+f(rb.t-Math.max(tb.b,mb.b)));
      check('the custom field stays directly above the purpose field',
            pb.t-rb.b<=18&&pb.t>=rb.b-1,'gap='+f(pb.t-rb.b));
      check('the purpose custom field stays directly below the purpose field',
            qb.t-qpg.b<=18&&qb.t>=qpg.b-1,'gap='+f(qb.t-qpg.b));

      var badLabel=[],badLeft=[];
      [].slice.call(grid.querySelectorAll('.fg')).forEach(function(fg){
        var lb=fg.querySelector('label');if(!lb)return;
        var ctrl=fg.querySelector('.cs-btn,input,select,textarea');if(!ctrl)return;
        var a=R(lb),b=R(ctrl);
        if(a.b>b.t+1)badLabel.push(lb.textContent||lb.getAttribute('data-i'));
        if(Math.abs(a.l-b.l)>1.5)badLeft.push(f(a.l)+'/'+f(b.l));
      });
      check('every label sits above its control',badLabel.length===0,badLabel.join(','));
      check('every label is left aligned with its control',badLeft.length===0,badLeft.join(' '));
      [['customToneLabel','customToneVal'],['customPurpLabel','customPurpVal']].forEach(function(pair){
        var lb=document.querySelector('label[data-i="'+pair[0]+'"]');
        if(!lb){rec('FAIL missing label '+pair[0]);fails++;return;}
        var a=R(lb),b=R($(pair[1]));
        check('the ' + pair[1] + ' label sits above its input',a.b<=b.t+1&&Math.abs(a.l-b.l)<1.5,
              'label='+show(a)+' input='+show(b));
      });

      if(!narrow){
        var pairs=[[0,1],[2,3],[4,5]];
        var mis=pairs.filter(function(p){return Math.abs(rects[p[0]].t-rects[p[1]].t)>1.5;});
        check('the three two-column rows are top aligned',mis.length===0,
              mis.map(function(p){return f(rects[p[0]].t)+'/'+f(rects[p[1]].t);}).join(' '));
        check('full-width blocks span both columns',
              Math.abs(rects[6].w-rects[7].w)<2&&Math.abs(rects[6].w-rects[8].w)<2&&rects[6].w>rects[4].w,
              'custTone='+f(rects[6].w)+' purpose='+f(rects[7].w)+' custPurp='+f(rects[8].w)+' toneCol='+f(rects[4].w));
      } else {
        var lefts=rects.map(function(r){return r.l;});
        check('single column: every block starts at the same left edge',
              lefts.every(function(l){return Math.abs(l-lefts[0])<1.5;}),lefts.map(f).join(','));
      }
      var gbox=R(grid);
      var over=nodes.filter(function(n){var r=R(n);return r.l<gbox.l-1||r.r>gbox.r+1;});
      check('no option block overflows the grid',over.length===0,'n='+over.length);
      check('the letter textarea is below the grid and as wide as the rows',
            R(ta).t>=gbox.b-1&&Math.abs(R(ta).w-rects[7].w)<3,
            'ta='+show(R(ta))+' gridBottom='+f(gbox.b));

      /* ---- 5. closing them again removes the rows ---- */
      pick('#toneCS','professional');
      pick('#purposeCS','general');
      settle();
      check('a preset choice hides the custom style field',getComputedStyle(box).display==='none',
            'display='+getComputedStyle(box).display);
      check('a preset choice hides the custom purpose field',getComputedStyle(pbox).display==='none',
            'display='+getComputedStyle(pbox).display);
      check('the rows collapse back to the normal gap',
            f(R(purposeFg).t-Math.max(R(toneFg).b,R(modeFg).b))<=18,
            'gap='+f(R(purposeFg).t-Math.max(R(toneFg).b,R(modeFg).b)));

      /* ---- 6. target sizes, action row, counter, no side scroll ---- */
      var fs=focusables(card).map(function(el){return {id:el.id||el.getAttribute('onclick')||el.tagName,h:R(el).h};});
      check('every control in the card is at least 28px tall',
            fs.every(function(o){return o.h>=28;}),
            'min='+f(Math.min.apply(null,fs.map(function(o){return o.h;})))+
            ' small='+JSON.stringify(fs.filter(function(o){return o.h<28;})));
      var go=$('goBtn'),cl=card.querySelector('[onclick="clearAll()"]');
      check('the primary action comes first and on the same line as clear/sample',
            R(go).l<R(cl).l&&Math.abs(R(go).t-R(cl).t)<1.5,'go='+show(R(go))+' clear='+show(R(cl)));
      check('the primary action is the widest button',R(go).w>R(cl).w,
            'goW='+f(R(go).w)+' clearW='+f(R(cl).w));
      check('the action row sits below the letter textarea',R(go).t>=R(ta).b-1,
            'goTop='+f(R(go).t)+' taBottom='+f(R(ta).b));
      check('the character counter sits under the textarea',R($('charCnt')).t>=R(ta).b-1,
            'cnt='+show(R($('charCnt'))));
      check('the page does not scroll sideways',
            document.documentElement.scrollWidth<=document.documentElement.clientWidth+1,
            'scrollW='+document.documentElement.scrollWidth+' clientW='+document.documentElement.clientWidth);

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
print('wrote %s from %s (bytes=%d)' % (out, src, len(s)))
