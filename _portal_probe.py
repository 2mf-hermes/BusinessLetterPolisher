# -*- coding: utf-8 -*-
"""Build _portal.html: the app + a fully synchronous dropdown probe.

Panel menus are portaled into <body> (so the panel's overflow/backdrop-filter can
never clip them); menus in the main window keep their plain absolute placement.
Everything runs inside the load handler because Edge's --dump-dom snapshots the
page there (the app's own update fetch would otherwise stall virtual time).
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROBE = r'''
<style id="probeStyle">*{animation:none !important;}</style>
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[],fails=0;
  function rec(s){log.push(s);}
  function check(name,cond,extra){if(!cond)fails++;rec((cond?'PASS ':'FAIL ')+name+(extra?'  '+extra:''));}
  function $(i){return document.getElementById(i);}
  function ddOf(id){var cs=$(id);return cs?cs.querySelector('.cs-dd'):null;}
  function btnOf(id){var cs=$(id);return cs?cs.querySelector('.cs-btn'):null;}
  function opts(id){var dd=ddOf(id)||parked(id);return dd?dd.querySelectorAll('.cs-opt'):[];}
  function parked(id){var d=[].slice.call(document.body.children).filter(function(n){return n.classList&&n.classList.contains('cs-dd')&&n.__cs&&n.__cs.id===id;});return d[0]||null;}
  function rect(el){var r=el.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom];}
  function show(a){return a.map(Math.round).join(',');}
  function click(el){el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));}
  function finish(){rec('RESULT fails='+fails);$('probeOut').textContent=log.join('\n');}

  window.addEventListener('load',function(){
    try{
      var g=$('guideOv');if(g)g.classList.remove('open');
      $('sOv').classList.add('open');
      var pb=document.querySelector('#sOv .panel-body');

      var ap=activeProv();if(ap){ap.models=['gpt-4o','gpt-4o-mini'];refreshModelDD();}
      rec('diag provCS='+!!$('provCS')+' provOpts='+opts('provCS').length+' modelCS='+!!$('modelCS')+' modelOpts='+opts('modelCS').length+' toneCS='+!!$('toneCS'));

      /* the URL / key / model / temperature rows ship collapsed and only appear after
         新增 or 修改: open them the way a user does, so they take part in the checks
         below (and so the panel is tall enough to actually scroll). */
      var boxBoot=$('provEditBox');
      check('connection block collapsed at boot',
            !!boxBoot&&!boxBoot.classList.contains('open'),
            'display='+(boxBoot?getComputedStyle(boxBoot).display:'-'));
      (function(){
        var b=document.querySelector('[onclick="editProvider()"]');
        if(b)click(b);
      })();
      check('connection block opens for the edit flow',
            !!$('provEditBox')&&$('provEditBox').classList.contains('open'),
            'display='+($('provEditBox')?getComputedStyle($('provEditBox')).display:'-'));

      /* open a dropdown and check the geometry of the menu it produced */
      function openMenu(id,label,expectPortal){
        var btn=btnOf(id),cs=$(id);
        if(!btn||!cs){check(label+' markup exists',false,'btn='+!!btn+' cs='+!!cs);return null;}
        if(btn.closest('.panel-body'))pb.scrollTop=Math.max(0,btn.offsetTop-pb.clientHeight/2);
        click(btn);
        var dd=ddOf(id)||parked(id);
        if(!dd){check(label+' menu exists',false);return null;}
        var r=rect(dd),br=rect(btn);
        check(label+' menu open',dd.classList.contains('open'),'inlineTop='+dd.style.top);
        if(expectPortal)check(label+' parked in body while open',dd.parentElement===document.body,'parent='+(dd.parentElement?(dd.parentElement.id||dd.parentElement.tagName):'null'));
        check(label+' glued to button left',Math.abs(r[0]-br[0])<=1.5,'dd='+show(r)+' btn='+show(br));
        check(label+' 5px below button',Math.abs(r[1]-br[3]-5)<=1.5,'gap='+(r[1]-br[3]).toFixed(1));
        check(label+' at least as wide as the button',(r[2]-r[0])>=(br[2]-br[0])-0.5&&(r[2]-r[0])<=(br[2]-br[0])+140,'w='+(r[2]-r[0]).toFixed(1)+' btnW='+(br[2]-br[0]).toFixed(1));
        check(label+' inside viewport',r[0]>=-0.5&&r[2]<=innerWidth+0.5&&r[1]>=-0.5&&r[3]<=innerHeight+0.5,'dd='+show(r)+' vp='+innerWidth+'x'+innerHeight);
        var hit=document.elementFromPoint((r[0]+r[2])/2,(r[1]+r[3])/2);
        check(label+' not covered at its centre',!!hit&&(hit===dd||dd.contains(hit)),'hit='+(hit?(hit.className||hit.tagName):'null'));
        return {id:id,dd:dd,btn:btn,cs:cs,r:r,portal:expectPortal};
      }

      /* ---------- 1. the provider menu in the settings panel ---------- */
      var a=openMenu('provCS','provider',true);
      if(a){
        check('provider menu still open (nothing closed it)',a.dd.classList.contains('open'));
        /* ---------- 2. scrolling the settings panel must not close it ---------- */
        var b0=rect(btnOf('provCS')),d0=rect(a.dd);
        var raf=window.requestAnimationFrame;
        window.requestAnimationFrame=function(f){f();return 0;};   /* headless: no frames before --dump-dom */
        pb.scrollTop=pb.scrollTop+40;
        pb.dispatchEvent(new Event('scroll'));
        var cur=parked('provCS')||ddOf('provCS');
        var b1=rect(btnOf('provCS')),d1=rect(cur);
        check('settings panel really scrolled',b1[1]!==b0[1],'btnBefore='+show(b0)+' btnAfter='+show(b1));
        check('provider menu survives the panel scroll',!!cur&&cur.classList.contains('open'));
        check('provider menu moved with its button',d1[1]!==d0[1],'ddBefore='+show(d0)+' ddAfter='+show(d1));
        check('provider menu stays glued during the scroll',Math.abs(d1[0]-b1[0])<=1.5&&Math.abs(d1[1]-b1[3]-5)<=1.5,
              'dd='+show(d1)+' btn='+show(b1));
        window.requestAnimationFrame=raf;
        /* ---------- 3. picking an item closes it and puts it back ---------- */
        var first=opts('provCS')[0];
        if(first){
          var beforeVal=$('provider').value;
          click(first);
          var csNow=$('provCS'),ddNow=ddOf('provCS'),btnNow=btnOf('provCS');
          check('provider menu closed after the pick',!ddNow.classList.contains('open'));
          check('provider menu back inside #provCS',ddNow.parentElement===csNow,'parent='+(ddNow.parentElement?(ddNow.parentElement.id||ddNow.parentElement.tagName):'null'));
          check('provider menu is the button sibling again',btnNow.nextElementSibling===ddNow);
          check('no menu left behind in <body>',!parked('provCS'));
          check('picked provider stored',!!$('provider').value||!!beforeVal,'value='+$('provider').value);
        }
        /* ---------- 4. click again: opens, second click closes ---------- */
        var b=openMenu('provCS','provider(re-open)',true);
        if(b){
          click(btnOf('provCS'));
          var d3=ddOf('provCS');
          check('second click closes the provider menu',!d3.classList.contains('open')&&d3.parentElement===$('provCS')&&!parked('provCS'));
        }
      }

      /* ---------- 5. the model picker in the same panel ---------- */
      var m=openMenu('modelCS','model',true);
      if(m){
        click(btnOf('modelCS'));
        var dm=ddOf('modelCS');
        check('second click closes the model menu',!!dm&&!dm.classList.contains('open')&&dm.parentElement===$('modelCS')&&!parked('modelCS'));
      }

      /* ---------- 6. a main-window dropdown keeps its own placement ---------- */
      $('sOv').classList.remove('open');   /* with the panel closed the main window is reachable again */
      var t=openMenu('toneCS','tone',false);
      if(t){
        check('tone menu stays inside its .cs wrapper',t.dd.parentElement===t.cs,'parent='+(t.dd.parentElement?(t.dd.parentElement.id||t.dd.parentElement.tagName):'null'));
        check('tone menu opens on top of the main window',
              (function(){var r=rect(t.dd),h=document.elementFromPoint((r[0]+r[2])/2,(r[1]+r[3])/2);return !!h&&(h===t.dd||t.dd.contains(h));})());
        click(btnOf('toneCS'));
        check('second click closes the tone menu',!ddOf('toneCS').classList.contains('open'));
      }

      finish();
    }catch(e){rec('ERR '+e.message);finish();}
  });
})();
</script>
'''

src_path = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out_path = sys.argv[2] if len(sys.argv) > 2 else '_portal.html'
src = open(src_path, encoding='utf-8', newline='').read()
i = src.rfind('</body>')
open(out_path, 'w', encoding='utf-8', newline='').write(src[:i] + PROBE + src[i:])
print('wrote %s from %s' % (out_path, src_path))
