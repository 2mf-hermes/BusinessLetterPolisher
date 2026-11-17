# -*- coding: utf-8 -*-
"""Probe copy: transitions/animations disabled so headless layout is final."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

src = open('letter-polisher.html', encoding='utf-8', newline='').read()

KILL = '<style id="__kill">*{transition:none!important;animation:none!important;}</style>'

PROBE = r"""
<script>
function __m(name,extra){
  var dd=document.getElementById('provDD'), cs=document.getElementById('provCS');
  var out={name:name};
  if(!dd){out.err='no provDD';}
  else{
    var c=getComputedStyle(dd), r=dd.getBoundingClientRect();
    out.opts=dd.querySelectorAll('.cs-opt').length;
    out.cls=dd.className;out.pos=c.position;out.opacity=c.opacity;out.pointer=c.pointerEvents;
    out.rect=[Math.round(r.left),Math.round(r.top),Math.round(r.width),Math.round(r.height)];
    var o=dd.querySelector('.cs-opt');
    if(o){var orr=o.getBoundingClientRect();
      out.opt0=[Math.round(orr.left),Math.round(orr.top),Math.round(orr.width),Math.round(orr.height)];
      out.opt0Text=o.textContent.replace(/\u2713/g,'').trim();
      var cx=Math.round(orr.left+orr.width/2),cy=Math.round(orr.top+orr.height/2);
      var top=document.elementFromPoint(cx,cy);
      out.topAtOpt0=top?(top.id||(typeof top.className==='string'?top.className:top.tagName)):'null';
      out.topInsideDD=!!(top&&dd.contains(top));
    }
    var btn=cs.querySelector('.cs-btn'),br=btn.getBoundingClientRect();
    out.btnRect=[Math.round(br.left),Math.round(br.top),Math.round(br.width),Math.round(br.height)];
    var tx=cs.querySelector('.cs-txt');out.btnLabel=tx?tx.textContent:'';
    out.win=[window.innerWidth,window.innerHeight];
    out.inView=(r.left>0&&r.top>0&&r.right<window.innerWidth&&r.bottom<window.innerHeight);
  }
  if(extra)for(var k in extra)out[k]=extra[k];
  var el=document.getElementById('probeOut');
  if(!el){el=document.createElement('pre');el.id='probeOut';el.style.cssText='position:fixed;left:2px;top:2px;z-index:99999;background:#fff;color:#000;font-size:10px;white-space:pre-wrap;opacity:.01';document.body.appendChild(el);}
  el.textContent+='\n'+JSON.stringify(out);
}
window.addEventListener('DOMContentLoaded',function(){
  function step(fn,d){return new Promise(function(r){setTimeout(function(){try{fn();}catch(e){var p=document.getElementById('probeOut');if(p)p.textContent+='\nERR '+e.message;}r();},d);});}
  step(function(){ var g=document.getElementById('guideOv'); if(g)g.remove(); },400)
  .then(function(){return step(function(){ __m('a.initial'); toggleSP(); },300);})
  .then(function(){return step(function(){ __m('b.settingsOpen'); var b=document.querySelector('#provCS .cs-btn'); __m('b2.btn',{hidden:!!(b.offsetWidth===0&&b.offsetHeight===0)}); csToggle(b); },200);})
  .then(function(){return step(function(){ __m('c.afterToggle'); },200);})
  .then(function(){return step(function(){ newProvider(); __m('d.afterNewProvider'); },200);})
  .then(function(){return step(function(){ var dd=document.getElementById('provDD'); dd.classList.remove('open'); csToggle(document.querySelector('#provCS .cs-btn')); },50);})
  .then(function(){return step(function(){ __m('e.reopen'); window.__probeDone=true; },300);});
});
</script>
"""

out = src.replace('</head>', KILL + '\n</head>') if '</head>' in src else src
out = out.replace('</body>', PROBE + '\n</body>')
open('_probe.html', 'w', encoding='utf-8', newline='').write(out)
print('written _probe.html', len(out))
