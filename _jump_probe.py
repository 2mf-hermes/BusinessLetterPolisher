# -*- coding: utf-8 -*-
"""Build _jump.html: same app, but the probe does NOT switch CSS transitions off.

_portal_probe.py injected `*{transition:none!important}`, which hid a real-browser
bug: .cs-dd uses `transition:all .18s`, so when csPlaceMenu() sets position:fixed +
left/top and then reads getBoundingClientRect() in the SAME task, the rect still
reports the transition's START values (the menu's old absolute coordinates inside
the panel). The "last-resort correction" therefore adds a huge bogus offset and the
menu flies off screen - exactly the "opens, jumps, cannot be seen" report.

This probe keeps transitions enabled so headless Edge sees the same numbers a real
WebView2 sees.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROBE = r'''
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[],fails=0;
  function rec(s){log.push(s);}
  function check(name,cond,extra){if(!cond)fails++;rec((cond?'PASS ':'FAIL ')+name+(extra?'  '+extra:''));}
  function $(i){return document.getElementById(i);}
  function ddOf(id){var cs=$(id);return cs?cs.querySelector('.cs-dd'):null;}
  function btnOf(id){var cs=$(id);return cs?cs.querySelector('.cs-btn'):null;}
  function parked(id){var d=[].slice.call(document.body.children).filter(function(n){return n.classList&&n.classList.contains('cs-dd')&&n.__cs&&n.__cs.id===id;});return d[0]||null;}
  function rect(el){var r=el.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom];}
  function show(a){return a.map(function(x){return x.toFixed(1);}).join(',');}
  function click(el){el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true}));}

  window.addEventListener('load',function(){
    try{
      var g=$('guideOv');if(g)g.classList.remove('open');
      $('sOv').classList.add('open');
      var pb=document.querySelector('#sOv .panel-body');
      var raf=window.requestAnimationFrame;
      window.requestAnimationFrame=function(f){f();return 0;};   /* headless: no frames before --dump-dom */

      function openCheck(id,label,isPanel){
        var btn=btnOf(id),cs=$(id);
        check(label+' markup exists',!!btn&&!!cs);
        if(!btn||!cs)return null;
        if(isPanel&&btn.closest('.panel-body'))pb.scrollTop=Math.max(0,btn.offsetTop-pb.clientHeight/2);
        click(btn);
        var dd=parked(id)||ddOf(id);
        check(label+' menu exists and is open',!!dd&&dd.classList.contains('open'));
        if(!dd)return null;
        var r=rect(dd),br=rect(btn);
        check(label+' glued to button left',Math.abs(r[0]-br[0])<=1.5,'dd='+show(r)+' btn='+show(br));
        check(label+' ~5px away from the button',Math.abs(r[1]-br[3]-5)<=6||Math.abs(br[1]-r[3]-5)<=6,'gap='+(r[1]-br[3]).toFixed(1));
        check(label+' inside viewport',r[0]>=-1&&r[2]<=innerWidth+1&&r[1]>=-1&&r[3]<=innerHeight+1,'dd='+show(r)+' vp='+innerWidth+'x'+innerHeight);
        check(label+' horizontal size sane',(r[2]-r[0])>=30&&(r[2]-r[0])<=innerWidth,'w='+(r[2]-r[0]).toFixed(1));
        var hx=Math.min(Math.max((r[0]+r[2])/2,2),innerWidth-2);
        var hy=Math.min(Math.max((r[1]+r[3])/2,2),innerHeight-2);
        var hit=document.elementFromPoint(hx,hy);
        check(label+' visible at its own centre',!!hit&&(hit===dd||dd.contains(hit)),'hit='+(hit?(hit.className||hit.tagName):'null')+' at='+hx.toFixed(0)+','+hy.toFixed(0));
        check(label+' inline left/top look like viewport coords',parseFloat(dd.style.left||'0')<innerWidth&&parseFloat(dd.style.top||'0')<innerHeight,
              'left='+dd.style.left+' top='+dd.style.top);
        window.requestAnimationFrame=raf;click(btn);window.requestAnimationFrame=function(f){f();return 0;};
        return {id:id,dd:dd,btn:btn};
      }

      var ap=activeProv();if(ap){ap.models=['gpt-4o','gpt-4o-mini'];refreshModelDD();}

      var a=openCheck('provCS','provider',true);
      if(a){   /* after the click that opened it, a re-read of the box must agree */
        var r2=rect(parked('provCS')||ddOf('provCS')),br2=rect(btnOf('provCS'));
        check('provider menu agrees with its button on a second read',Math.abs(r2[0]-br2[0])<=1.5,'dd='+show(r2)+' btn='+show(br2));
      }
      openCheck('modelCS','model',true);
      $('sOv').classList.remove('open');
      openCheck('toneCS','tone',false);
      window.requestAnimationFrame=raf;

      /* ---- the connection block stays hidden until Add / Edit ---- */
      function boxOpen(){var b=$('provEditBox');return !!b&&b.classList.contains('open');}
      function shown(el){
        if(!el)return false;
        var r=el.getBoundingClientRect();
        if(!(r.width>1&&r.height>1))return false;
        var x=Math.min(Math.max((r.left+r.right)/2,1),innerWidth-1);
        var y=Math.min(Math.max((r.top+r.bottom)/2,1),innerHeight-1);
        var hit=document.elementFromPoint(x,y);
        return !!hit&&(el===hit||el.contains(hit)||hit.contains(el));
      }
      function reveal(el){
        var r=el.getBoundingClientRect();
        pb.scrollTop+=(r.top-pb.getBoundingClientRect().top)-50;
      }
      $('sOv').classList.add('open');
      check('connection block exists',!!$('provEditBox'));
      check('connection block collapsed at boot',!boxOpen());
      check('url/key/model fields live inside the block',
        !!$('provEditBox')&&['apiUrl','apiKey','modelName','temperature','provName'].every(function(i){return $('provEditBox').contains($(i));}));
      check('url field hidden while collapsed',!shown($('apiUrl')));
      var nBefore=(typeof providers!=='undefined')?providers.length:-1;
      var newBtn=document.querySelector('[onclick="newProvider()"]');
      check('add button exists',!!newBtn);
      if(newBtn){
        click(newBtn);
        check('add opens the connection block',boxOpen());
        reveal($('provEditBox'));
        check('block visible after add',shown($('provEditBox')));
        check('url field visible after add',shown($('apiUrl')));
        var cancelBtn=document.querySelector('#provEditBox [onclick="cancelProviderEdit()"]');
        check('save + cancel buttons exist',!!document.querySelector('#provEditBox [onclick="saveProviderEdit()"]')&&!!cancelBtn);
        if(cancelBtn){
          click(cancelBtn);
          check('cancel collapses the block',!boxOpen());
          check('cancel drops the untouched provider',
            (typeof providers==='undefined')||providers.length===nBefore,
            'n='+(typeof providers!=='undefined'?providers.length:'?')+' before='+nBefore);
        }
      }
      var editBtn=$('provEditBtn');
      check('edit button exists',!!editBtn);
      if(editBtn){
        click(editBtn);
        check('edit opens the connection block',boxOpen());
        reveal($('provEditBox'));
        check('block visible after edit',shown($('provEditBox')));
        var saveBtn=document.querySelector('#provEditBox [onclick="saveProviderEdit()"]');
        if(saveBtn)click(saveBtn);
        check('save collapses the block',!boxOpen());
        check('in-use line is filled',!!$('provCur')&&$('provCur').textContent.trim().length>0,
          $('provCur')?$('provCur').textContent.trim():'missing');
      }
      $('sOv').classList.remove('open');

      rec('RESULT fails='+fails);
      $('probeOut').textContent=log.join('\n');
    }catch(e){rec('ERR '+e.message);rec('RESULT fails='+fails);$('probeOut').textContent=log.join('\n');}
  });
})();
</script>
'''

src_path = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out_path = sys.argv[2] if len(sys.argv) > 2 else '_jump.html'
src = open(src_path, encoding='utf-8', newline='').read()
i = src.rfind('</body>')
open(out_path, 'w', encoding='utf-8', newline='').write(src[:i] + PROBE + src[i:])
print('wrote %s from %s' % (out_path, src_path))
