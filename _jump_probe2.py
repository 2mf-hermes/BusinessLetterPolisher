# -*- coding: utf-8 -*-
"""Build _jump2.html - the transition-preserving probe, corrected.

Two things the first probe got wrong and that are fixed here:

1. It measured the panel while its 0.28s entrance slide was still at its start
   value (headless never advances it), so every control inside the panel appeared
   500px to the right and the "glued to the button" check could not mean anything.
   The probe now finishes the panel animation before measuring.
2. The model picker lives inside the collapsible connection block, so the block has
   to be opened before that menu can be tested.

CSS transitions are deliberately NOT disabled: `.cs-dd` animating `all` is exactly
what made the menu land in the wrong place, and a probe that switches transitions
off cannot see that (that mistake produced the previous false "all green" run).
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
  function settleAnim(){
    try{
      var p=document.querySelector('#sOv .panel');
      p.getAnimations().forEach(function(a){try{a.finish();}catch(e){}});
    }catch(e){}
    void document.body.offsetWidth;
  }
  function panelBody(){return document.querySelector('#sOv .panel-body');}
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
    if(!el)return;
    var pb=panelBody(),r=el.getBoundingClientRect();
    pb.scrollTop+=(r.top-pb.getBoundingClientRect().top)-60;
  }
  var raf=window.requestAnimationFrame;
  window.requestAnimationFrame=function(f){f();return 0;};   /* headless: no frames before --dump-dom */

  function openCheck(id,label){
    var btn=btnOf(id),cs=$(id);
    check(label+' markup exists',!!btn&&!!cs);
    if(!btn||!cs)return null;
    click(btn);
    var dd=parked(id)||ddOf(id);
    check(label+' menu exists and is open',!!dd&&dd.classList.contains('open'));
    if(!dd)return null;
    var r=rect(dd),br=rect(btn);
    check(label+' glued to button left',Math.abs(r[0]-br[0])<=1.5,'dd='+show(r)+' btn='+show(br));
    check(label+' ~5px away from the button',Math.abs(r[1]-br[3]-5)<=6||Math.abs(br[1]-r[3]-5)<=6,'gap='+(r[1]-br[3]).toFixed(1));
    check(label+' inside viewport',r[0]>=-1&&r[2]<=innerWidth+1&&r[1]>=-1&&r[3]<=innerHeight+1,'dd='+show(r)+' vp='+innerWidth+'x'+innerHeight);
    check(label+' horizontal size sane',(r[2]-r[0])>=30&&(r[2]-r[0])<=innerWidth,'w='+(r[2]-r[0]).toFixed(1));
    var hx=Math.min(Math.max((r[0]+r[2])/2,2),innerWidth-2),hy=Math.min(Math.max((r[1]+r[3])/2,2),innerHeight-2);
    var hit=document.elementFromPoint(hx,hy);
    check(label+' visible at its own centre',!!hit&&(hit===dd||dd.contains(hit)),'hit='+(hit?(hit.className||hit.tagName):'null')+' at='+hx.toFixed(0)+','+hy.toFixed(0));
    var bogus=Math.abs(parseFloat(dd.style.left||'0'))>innerWidth||Math.abs(parseFloat(dd.style.top||'0'))>innerHeight;
    check(label+' inline left/top are viewport coords',!bogus,'left='+dd.style.left+' top='+dd.style.top);
    click(btn);   /* toggle it shut again */
    return {id:id,dd:dd,btn:btn};
  }

  function run(){
    try{
      var g=$('guideOv');if(g)g.classList.remove('open');
      $('sOv').classList.add('open');
      settleAnim();

      var ap=activeProv();if(ap){ap.models=['gpt-4o','gpt-4o-mini'];refreshModelDD();}

      /* ---- dropdown geometry, transitions live ---- */
      var a=openCheck('provCS','provider');
      if(a){   /* a second read of the box must agree with its button too */
        var r2=rect(ddOf('provCS')),br2=rect(btnOf('provCS'));
        check('provider menu still agrees with its button',Math.abs(r2[0]-br2[0])<=1.5||(r2[0]===0&&r2[1]===0),'dd='+show(r2)+' btn='+show(br2));
      }

      /* ---- the connection block: collapsed until Add / Edit ---- */
      function boxOpen(){var b=$('provEditBox');return !!b&&b.classList.contains('open');}
      check('connection block exists',!!$('provEditBox'));
      check('connection block collapsed at boot',!boxOpen());
      check('url/key/model/temperature sit inside the block',
        !!$('provEditBox')&&['apiUrl','apiKey','modelName','temperature','provName'].every(function(i){return !!$(i)&&$('provEditBox').contains($(i));}));
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
        check('temperature visible after add',shown($('temperature')));
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
        /* the model picker is inside the block: now it can be measured */
        var model=openCheck('modelCS','model');
        if(model){reveal($('provEditBox'));}
        var saveBtn=document.querySelector('#provEditBox [onclick="saveProviderEdit()"]');
        if(saveBtn)click(saveBtn);
        check('save collapses the block',!boxOpen());
        check('in-use line is filled',!!$('provCur')&&$('provCur').textContent.trim().length>0,
          $('provCur')?$('provCur').textContent.trim():'missing');
      }

      /* ---- dropdowns outside the panel (never portaled) ---- */
      $('sOv').classList.remove('open');
      openCheck('toneCS','tone');
      $('sOv').classList.add('open');

      /* ---- a menu opened while the panel is still sliding must re-glue itself ---- */
      var p=document.querySelector('#sOv .panel');
      $('sOv').classList.remove('open');void p.offsetWidth;
      $('sOv').classList.add('open');void p.offsetWidth;      /* restart the slide */
      click(btnOf('provCS'));
      var dd=parked('provCS');
      check('menu opened during the slide exists',!!dd&&dd.classList.contains('open'));
      rec('(info) placed during the slide: dd='+(dd?show(rect(dd)):'-')+' btn='+show(rect(btnOf('provCS'))));
      settleAnim();   /* headless never advances the slide: arriving == finish() it */
      setTimeout(function(){
        var d2=parked('provCS'),b2=btnOf('provCS');
        if(d2&&b2){
          var rr=rect(d2),bb=rect(b2);
          check('menu re-glues to its button once the panel settles',Math.abs(rr[0]-bb[0])<=2,'dd='+show(rr)+' btn='+show(bb));
          check('re-glued menu is still on screen',rr[0]>=-1&&rr[2]<=innerWidth+1&&rr[1]>=-1&&rr[3]<=innerHeight+1,'dd='+show(rr));
        }else{check('menu survived the slide',false,'dd='+!!d2);}
        rec('RESULT fails='+fails);
        $('probeOut').textContent=log.join('\n');
      },700);
    }catch(e){rec('ERR '+e.message+' @'+e.lineno);rec('RESULT fails='+fails);$('probeOut').textContent=log.join('\n');}
  }
  window.addEventListener('load',function(){setTimeout(run,0);});
})();
</script>
'''

src_path = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out_path = sys.argv[2] if len(sys.argv) > 2 else '_jump2.html'
src = open(src_path, encoding='utf-8', newline='').read()
i = src.rfind('</body>')
open(out_path, 'w', encoding='utf-8', newline='').write(src[:i] + PROBE + src[i:])
print('wrote %s from %s' % (out_path, src_path))
