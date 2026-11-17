# -*- coding: utf-8 -*-
"""Humane-layout audit for the rest of the shell: the two cards, the output card,
the history panel and the settings panel.

Builds `_ui_audit2.html` and measures layout / target sizes / reading order in a
real browser with CSS transitions left ON.

Usage: python _ui_audit2.py [src] [out]
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out = sys.argv[2] if len(sys.argv) > 2 else '_ui_audit2.html'

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
  function settle(root){
    try{(root||document.body).getAnimations({subtree:true}).forEach(function(a){try{a.finish();}catch(e){}});}catch(e){}
    void document.body.offsetWidth;
  }
  function overlaps(a,b){return !(a.r<=b.l+0.5||b.r<=a.l+0.5||a.b<=b.t+0.5||b.b<=a.t+0.5);}
  function visible(el){
    if(!el)return false;
    var s=getComputedStyle(el);
    if(s.display==='none'||s.visibility==='hidden'||parseFloat(s.opacity)===0)return false;
    return el.getClientRects().length>0;
  }
  function targets(root){
    return [].slice.call(root.querySelectorAll('button,input:not([type=hidden]),textarea,[tabindex]:not([tabindex="-1"])'))
      .filter(function(el){return visible(el)&&!el.disabled;});
  }
  /* A control that lives inside a <label> (a switch, a chip) is hit through the
     label, so the label's box is the real target size. */
  function smallTargets(root,min){
    return targets(root).map(function(el){
      var lb=el.closest('label');
      var box=R(lb&&lb!==el?lb:el);
      return {name:(el.id||el.getAttribute('data-i')||el.className||el.tagName),
              size:f(box.w)+'x'+f(box.h),h:box.h};
    }).filter(function(o){return o.h<min;}).map(function(o){return o.name+':'+o.size;});
  }
  function labelIssues(root){
    var bad=[];
    [].slice.call(root.querySelectorAll('.fg,.pfld,.sect')).forEach(function(fg){
      var lb=fg.querySelector('label,dt,.lbl');if(!lb)return;
      var ctrl=fg.querySelector('input,textarea,.cs-btn,select');if(!ctrl)return;
      if(!visible(lb)||!visible(ctrl))return;
      var a=R(lb),b=R(ctrl);
      if(a.b>b.t+1||Math.abs(a.l-b.l)>1.5)bad.push((lb.textContent||lb.getAttribute('data-i')||'?').trim());
    });
    return bad;
  }
  function overflowX(root){
    var rb=R(root);
    return [].slice.call(root.querySelectorAll('*')).filter(function(el){
      if(!visible(el))return false;
      var r=R(el);
      return r.w>0&&(r.l<rb.l-1||r.r>rb.r+1);
    }).map(function(el){return (el.tagName+'.'+(el.className||'')).substring(0,40);});
  }

  window.addEventListener('load',function(){
    try{
      var g=$('guideOv');if(g)g.classList.remove('open');
      var raf=window.requestAnimationFrame;
      window.requestAnimationFrame=function(cb){cb();return 0;};
      settle();
      var narrow=window.innerWidth<620;
      /* The two cards sit side by side down to 860px; below that they stack. */
      var stacked=window.innerWidth<=860;
      var inCard=document.querySelector('.card-inp'),outCard=document.querySelector('.card-out');
      var ta=$('letterIn'),taOut=$('letterOut'),go=$('goBtn');
      info('viewport '+window.innerWidth+'x'+window.innerHeight+'  singleColumn='+narrow);

      /* ---- 1. the two cards read left-to-right, then top-to-bottom ---- */
      var a=R(inCard),b=R(outCard);
      if(!stacked){
        check('the input card sits left of the output card',a.r<=b.l+1,'in='+show(a)+' out='+show(b));
        check('both cards start on the same line',Math.abs(a.t-b.t)<1.5,'inTop='+f(a.t)+' outTop='+f(b.t));
        check('both cards use the same content width',Math.abs(a.w-b.w)<2,'inW='+f(a.w)+' outW='+f(b.w));
        check('the two letter areas line up',Math.abs(R(ta).w-R(taOut).w)<3,
              'inTaW='+f(R(ta).w)+' outTaW='+f(R(taOut).w));
      } else {
        check('stacked layout: the input card comes first, the output card below it',
              a.t<b.t-1&&a.l<=b.l+1,'inTop='+f(a.t)+' outTop='+f(b.t));
        check('stacked layout: both cards keep the same width',Math.abs(a.w-b.w)<2,
              'inW='+f(a.w)+' outW='+f(b.w));
        check('stacked layout: the two letter areas line up',Math.abs(R(ta).w-R(taOut).w)<3,
              'inTaW='+f(R(ta).w)+' outTaW='+f(R(taOut).w));
      }
      check('the cards do not overlap',!overlaps(a,b));
      var sc=document.querySelector('.wrap')||document.documentElement;
      var overY=getComputedStyle(sc).overflowY;
      info('scroller='+(sc.className||sc.tagName)+' overflowY='+overY+
           ' clientH='+sc.clientHeight+' scrollH='+sc.scrollHeight);
      info('primary action bottom='+f(R(go).b)+' scroll area top='+f(R(sc).t)+' height='+f(R(sc).h));
      check('the primary action is visible without scrolling',
            R(go).b<=R(sc).b+1,'goBottom='+f(R(go).b)+' scrollerBottom='+f(R(sc).b));

      /* ---- 2. floating buttons never cover a control ---- */
      var fabs=[$('fabH'),$('fabS')].filter(visible);
      check('both floating buttons are visible',fabs.length===2,'n='+fabs.length);
      check('floating buttons are big enough to hit',
            fabs.every(function(el){return R(el).w>=36&&R(el).h>=36;}),
            fabs.map(function(el){return f(R(el).w)+'x'+f(R(el).h);}).join(' '));
      function scanCovered(){
        var out=[];
        var ctrls=[].slice.call(document.querySelectorAll(
          'button,input:not([type=hidden]),textarea,.chip,.tab,.cs-btn')).filter(visible);
        fabs.forEach(function(fb){
          ctrls.forEach(function(t){
            if(overlaps(R(fb),R(t)))out.push(fb.id+'>'+(t.id||t.className||t.tagName));
          });
        });
        return out;
      }
      var scrolls=document.documentElement.scrollHeight>window.innerHeight+1;
      var covered=scanCovered();
      if(scrolls){
        /* A fixed button may pass over content while the page scrolls; what
           matters is that the page can be scrolled clear of it. */
        info('page scrolls '+document.documentElement.scrollHeight+' > '+window.innerHeight+
             '  covered at current position: '+(covered.join(',')||'none'));
        window.scrollTo(0,document.documentElement.scrollHeight);
        check('floating buttons cover no control once scrolled to the end',
              scanCovered().length===0,scanCovered().join(','));
        var lastCard=R(document.querySelector('.card-out'));
        var fabTop=Math.min.apply(null,fabs.map(function(el){return R(el).t;}));
        check('content can be scrolled clear of the floating buttons',lastCard.b<=fabTop,
              'cardOutBottom='+f(lastCard.b)+' fabTop='+f(fabTop));
        window.scrollTo(0,0);
      } else {
        check('floating buttons cover no control',covered.length===0,covered.join(','));
      }

      /* ---- 3. output card: tabs above the panes, one pane at a time ---- */
      var tabs=[].slice.call(outCard.querySelectorAll('.tab')),panes=[].slice.call(outCard.querySelectorAll('.tp'));
      check('the output card has three tabs',tabs.length===3,'n='+tabs.length);
      var tabsR=R(tabs[0]),firstPane=R(panes[0]);
      check('the tab row sits above the result area',R(tabs[0]).b<=firstPane.t+1,
            'tabsBottom='+f(R(tabs[0]).b)+' paneTop='+f(firstPane.t));
      check('the tabs are all on one line and equal width',
            Math.abs(R(tabs[0]).t-R(tabs[2]).t)<1.5,'w='+tabs.map(function(t){return f(R(t).w);}).join(','));
      check('the tabs are tall enough to hit',
            tabs.every(function(t){return R(t).h>=28;}),'h='+tabs.map(function(t){return f(R(t).h);}).join(','));
      var onTabs=tabs.filter(function(t){return t.classList.contains('on');});
      check('exactly one tab is active',onTabs.length===1,'n='+onTabs.length);
      var onStyle=onTabs.length?getComputedStyle(onTabs[0]):null,offStyle=getComputedStyle(tabs[1]);
      check('the active tab is visually distinct',
            onStyle&&(onStyle.color!==offStyle.color||onStyle.borderBottomColor!==offStyle.borderBottomColor),
            'on='+(onStyle?onStyle.color:'-')+' off='+offStyle.color);
      check('only the active pane is displayed',
            panes.filter(visible).length===1,'visible='+panes.filter(visible).map(function(p){return p.id;}).join(','));
      var ob=R(outCard).b,pb2=panes.map(R);
      check('the panes do not spill out of the card',pb2.every(function(r){return r.b<=ob+1;}),
            'cardBottom='+f(ob)+' paneBottom='+f(Math.max.apply(null,pb2.map(function(r){return r.b;}))) );
      var obtns=[].slice.call(outCard.querySelectorAll('.btns .btn'));
      check('the output card has three actions on one line',
            obtns.length===3&&Math.abs(R(obtns[0]).t-R(obtns[2]).t)<1.5,'n='+obtns.length);
      check('the output actions are tall enough to hit',
            obtns.every(function(x){return R(x).h>=28;}),
            obtns.map(function(x){return f(R(x).h);}).join(','));
      check('the copy action is first (leftmost)',R(obtns[0]).l<R(obtns[1]).l&&R(obtns[0]).l<R(obtns[2]).l);
      check('the output actions sit below the result area',
            R(obtns[0]).t>=panes.reduce(function(m,p){return Math.max(m,R(p).b);},0)-1);

      /* ---- 4. history panel ---- */
      toggleHP();settle($('hOv'));
      var hOv=$('hOv'),hp=hOv.querySelector('.panel'),hb=hp.querySelector('.panel-body')||$('hList');
      check('the history panel opens',hOv.classList.contains('open')&&visible(hp));
      check('the history panel has a scrollable body',hb&&getComputedStyle(hb).overflowY==='auto',
            hb?getComputedStyle(hb).overflowY:'no body');
      var hx=hp.querySelector('.ph').getBoundingClientRect();
      if(hb){hb.scrollTop=9999;settle();}
      var hx2=hp.querySelector('.ph').getBoundingClientRect();
      check('the history header stays put while the list scrolls',Math.abs(hx2.top-hx.top)<1.5,
            'before='+f(hx.top)+' after='+f(hx2.top));
      check('the history panel does not scroll sideways',hb?hb.scrollWidth<=hb.clientWidth+1:false,
            hb?'scrollW='+hb.scrollWidth+' clientW='+hb.clientWidth:'-');
      check('history rows are tall enough to hit',
            [].slice.call($('hList').children).every(function(c){return R(c).h>=36;}),
            'n='+$('hList').children.length);
      toggleHP();settle($('hOv'));
      check('the history panel closes again',!hOv.classList.contains('open'));

      /* ---- 5. settings panel: reading order ---- */
      toggleSP();settle($('sOv'));
      var sOv=$('sOv'),sp=sOv.querySelector('.panel'),sb=sp.querySelector('.panel-body');
      check('the settings panel opens',sOv.classList.contains('open')&&visible(sp));
      info('settings buttons: '+[].slice.call(sp.querySelectorAll('.btn')).map(function(x){
        return (x.getAttribute('data-i')||x.id||x.className.replace('btn ',''))+':'+f(R(x).w)+'x'+f(R(x).h);
      }).join(' | '));
      info('pref switch: '+show(R($('letterPrefEnabled').closest('label')))+
           '  pref row: '+show(R(document.querySelector('.pref-row'))));
      var guideReopen=document.querySelector('[data-i="guideReopen"]');
      var order=[['quick presets',R($('presetChips'))],['AI provider',R($('provCS'))],
                 ['system prompt',R($('sysPrompt'))],['save / test',R($('testBtn'))],
                 ['letter prefs',R($('letterPrefEnabled'))],['guide',R(guideReopen.closest('button')||guideReopen)]];
      var bad=[];
      for(var i=1;i<order.length;i++){if(order[i][1].t<order[i-1][1].t-1)bad.push(order[i-1][0]+' > '+order[i][0]);}
      check('the settings sections follow a top-down order',bad.length===0,bad.join('; '));
      var saveBtn=sp.querySelector('.btn[onclick="saveCfg()"]'),testBtn=$('testBtn');
      check('save and test sit side by side',Math.abs(R(saveBtn).t-R(testBtn).t)<1.5,
            'save='+f(R(saveBtn).t)+' test='+f(R(testBtn).t));
      check('save comes before test in reading order',R(saveBtn).l<R(testBtn).l,
            'saveL='+f(R(saveBtn).l)+' testL='+f(R(testBtn).l));
      check('save is the emphasised action',saveBtn.classList.contains('btn-p')&&testBtn.classList.contains('btn-s'),
            'save='+saveBtn.className+' test='+testBtn.className);
      check('the provider row sits above the connection panel',
            R($('provCS')).b<=R($('provEditBox')).t+1||!visible($('provEditBox')));
      check('the system prompt field is usable',
            R($('sysPrompt')).h>=60,'h='+f(R($('sysPrompt')).h));
      var sbad=smallTargets(sp,28);
      check('every settings control is at least 28px tall',sbad.length===0,'small='+sbad.join(','));
      var sx=sp.querySelector('.ph').getBoundingClientRect();
      if(sb){sb.scrollTop=9999;settle();}
      var sx2=sp.querySelector('.ph').getBoundingClientRect();
      check('the settings header stays put while the body scrolls',Math.abs(sx2.top-sx.top)<1.5,
            'before='+f(sx.top)+' after='+f(sx2.top));
      check('the settings close button is on screen',R(sp.querySelector('.ph')).t>=-1,
            'headTop='+f(R(sp.querySelector('.ph')).t));
      if(sb){sb.scrollTop=0;settle();}
      var ovf=overflowX(sb||sp);
      check('nothing overflows the settings panel sideways',ovf.length===0,'n='+ovf.length+' '+ovf.slice(0,4).join(' '));
      var lbad=labelIssues(sp);
      check('settings labels sit above their own control',lbad.length===0,'bad='+lbad.join(','));
      check('the settings body scrolls rather than the page',
            document.documentElement.scrollWidth<=document.documentElement.clientWidth+1,
            'scrollW='+document.documentElement.scrollWidth+' clientW='+document.documentElement.clientWidth);
      check('the page behind the panel does not scroll sideways',document.body.scrollWidth<=document.body.clientWidth+1);

      /* provider buttons row: new / delete / edit must read in that order */
      var pb=[document.querySelector('.btn[onclick="newProvider()"]'),
              document.querySelector('.btn[onclick="deleteProvider()"]'),
              document.querySelector('.btn[onclick="editProvider()"]')].filter(Boolean);
      check('the provider buttons read new, delete, edit',pb.length===3&&R(pb[0]).l<R(pb[1]).l&&R(pb[1]).l<R(pb[2]).l,
            pb.map(function(x){return f(R(x).l);}).join(','));
      check('the provider buttons are on one line',pb.every(function(x){return Math.abs(R(x).t-R(pb[0]).t)<1.5;}));

      toggleSP();settle($('sOv'));
      check('the settings panel closes again',!sOv.classList.contains('open'));

      /* ---- 6. guide overlay opens and closes ---- */
      openGuide();settle($('guideOv'));
      check('the guide overlay opens',visible($('guideOv').firstElementChild||$('guideOv')));
      closeGuide();settle($('guideOv'));
      check('the guide overlay closes',!$('guideOv').classList.contains('open'));

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
