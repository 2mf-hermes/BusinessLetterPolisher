# -*- coding: utf-8 -*-
"""Build _portal2.html: same app + probe for the panel dropdowns.

Panel menus are portaled into <body> (never clipped by the panel); menus in the
main window keep their plain absolute placement. The probe checks: stays open,
glued to the button, on top (hit test), survives panel scrolling, and returns to
its .cs wrapper after a pick.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROBE = r'''
<style id="probeStyle">*{transition:none !important;animation:none !important;}</style>
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[],fails=0;
  function rec(s){log.push(s);}
  function check(name,cond,extra){if(!cond)fails++;rec((cond?'PASS ':'FAIL ')+name+(extra?'  '+extra:''));}
  window.addEventListener('load',function(){
    setTimeout(function(){
      try{
        var g=document.getElementById('guideOv');if(g)g.classList.remove('open');
        document.getElementById('sOv').classList.add('open');
        var pb=document.querySelector('#sOv .panel-body');
        function ddOf(id){return document.querySelector('#'+id+' .cs-dd');}
        function btnOf(id){return document.querySelector('#'+id+' .cs-btn');}
        function opts(id){return document.querySelectorAll('#'+id+' .cs-dd .cs-opt');}
        function rect(el){var r=el.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom];}
        function show(a){return a.map(Math.round).join(',');}
        function inPanel(id){return !!btnOf(id).closest('.panel-body');}

        if(opts('provCS').length<1&&window.newProvider)window.newProvider();
        var p=activeProv();if(p){p.models=['gpt-4o','gpt-4o-mini'];refreshModelDD();}
        rec('provider options='+opts('provCS').length+' model options='+opts('modelCS').length);

        function openAndCheck(id,label,expectPortal){
          var dd=ddOf(id),btn=btnOf(id);
          if(inPanel(id))pb.scrollTop=Math.max(0,btn.offsetTop-pb.clientHeight/2);
          btn.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
          var r=rect(dd),br=rect(btn);
          check(label+' open',dd.classList.contains('open'),'inlineTop='+dd.style.top+' parent='+dd.parentElement.tagName);
          check(label+' parent as expected',expectPortal?(dd.parentElement===document.body):(dd.parentElement===document.getElementById(id)),'parent='+dd.parentElement.tagName);
          check(label+' glued left',Math.abs(r[0]-br[0])<=1.5,'dd='+show(r)+' btn='+show(br));
          check(label+' below button',Math.abs(r[1]-br[3]-5)<=1.5,'gap='+(r[1]-br[3]).toFixed(1));
          check(label+' width matches button',Math.abs((r[2]-r[0])-(br[2]-br[0]))<=1.5,'w='+(r[2]-r[0]).toFixed(1)+' btnW='+(br[2]-br[0]).toFixed(1));
          check(label+' inside viewport',r[0]>=0&&r[2]<=innerWidth&&r[1]>=0&&r[3]<=innerHeight,'dd='+show(r)+' vp='+innerWidth+'x'+innerHeight);
          var cx=(r[0]+r[2])/2,cy=(r[1]+r[3])/2,hit=document.elementFromPoint(cx,cy);
          check(label+' on top at its centre',!!hit&&(hit===dd||dd.contains(hit)),'hit='+(hit?(hit.className||hit.tagName):'null'));
          return {dd:dd,btn:btn,cs:document.getElementById(id)};
        }

        var a=openAndCheck('provCS','provider',true);
        setTimeout(function(){
          check('provider stays open after 400ms',a.dd.classList.contains('open'));
          var before=rect(a.dd);
          pb.scrollTop=Math.max(0,pb.scrollTop-50);
          setTimeout(function(){
            var after=rect(a.dd),bafter=rect(a.btn);
            check('menu survives panel scroll',a.dd.classList.contains('open'));
            check('menu re-glued after scroll',Math.abs(after[0]-bafter[0])<=1.5&&Math.abs(after[1]-bafter[3]-5)<=1.5,
                  'dd='+show(after)+' btn='+show(bafter)+' moved='+(before[1]!==after[1]));
            var first=opts('provCS')[0];
            if(first){
              first.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              check('menu closed after pick',!a.dd.classList.contains('open'));
              check('menu re-parented to #provCS',a.dd.parentElement===document.getElementById('provCS'),'parent='+(a.dd.parentElement&&a.dd.parentElement.id));
              check('menu is the button sibling again',a.btn.nextElementSibling===a.dd);
              check('picked value stored',!!document.getElementById('provider').value);
            }
            /* second click on a panel button toggles it shut */
            var b=openAndCheck('provCS','provider(2)',true);
            b.btn.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
            check('panel menu toggles shut on second click',!b.dd.classList.contains('open')&&b.dd.parentElement===document.getElementById('provCS'));
            /* model picker (panel, async) */
            var m=openAndCheck('modelCS','model',true);
            setTimeout(function(){
              check('model menu open',m.dd.classList.contains('open'));
              check('model menu parked in body',m.dd.parentElement===document.body);
              var r=rect(m.dd),br=rect(m.btn);
              check('model menu glued left',Math.abs(r[0]-br[0])<=1.5,'dd='+show(r)+' btn='+show(br));
              var hit=document.elementFromPoint((r[0]+r[2])/2,(r[1]+r[3])/2);
              check('model menu on top',!!hit&&(hit===m.dd||m.dd.contains(hit)),'hit='+(hit?(hit.className||hit.tagName):'null'));
              m.btn.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              check('model menu toggles shut',!m.dd.classList.contains('open')&&m.dd.parentElement===document.getElementById('modelCS'));
              /* main-window menu keeps its plain placement */
              var t=openAndCheck('toneCS','tone',false);
              t.btn.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));
              check('main-window menu toggles shut',!t.dd.classList.contains('open')&&t.dd.parentElement===document.getElementById('toneCS'));
              rec('RESULT fails='+fails);
              document.getElementById('probeOut').textContent=log.join('\n');
            },250);
          },150);
        },400);
      }catch(e){document.getElementById('probeOut').textContent='ERR '+e.message+'\n'+(e.stack||'');}
    },250);
  });
})();
</script>
'''

src = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = src.rfind('</body>')
open('_portal2.html', 'w', encoding='utf-8', newline='').write(src[:i] + PROBE + src[i:])
print('wrote _portal2.html')

