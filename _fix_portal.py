# -*- coding: utf-8 -*-
"""Fix the flickering provider dropdown.

Root cause: an open menu inside the settings panel was only moved to
position:fixed. The panel has backdrop-filter, so the panel - not the viewport -
is its containing block, and the panel also has overflow:hidden: a menu that the
placement code opened downwards past the panel's bottom edge was clipped away
(hence "flashes, then gone"). Moving the panel content also fired a scroll event
on .panel-body, and the scroll listener closed every open menu.

Fix: portal the open menu into <body> (viewport-anchored, never clipped), keep a
reference to its .cs owner so picking/restoring still works, and reposition on
scroll/resize instead of closing.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

p = 'letter-polisher.html'
raw = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'


def q(s):
    return s.replace('\n', nl)


def swap(old, new, label):
    global raw
    o, n = q(old), q(new)
    if raw.count(o) != 1:
        print('FAIL %s: %d matches' % (label, raw.count(o)))
        sys.exit(1)
    raw = raw.replace(o, n, 1)
    print('ok', label)


swap("""function csToggle(btn){
  var dd=btn.nextElementSibling,wasOpen=dd.classList.contains('open');
  csCloseAll();
  if(!wasOpen){
    dd.classList.add('open');btn.classList.add('open');
    if(btn.closest('.panel-body'))csPlaceMenu(btn,dd);
  }
}""", """function csToggle(btn){
  /* Close the others first: an open menu is parked in <body> (see csPlaceMenu),
     so the button's real sibling only comes back once csCloseAll() has run. */
  var wasOpen=btn.classList.contains('open');
  csCloseAll();
  if(wasOpen)return;
  var dd=btn.nextElementSibling;
  if(!dd||!dd.classList.contains('cs-dd'))return;
  if(btn.closest('.panel-body'))csPlaceMenu(btn,dd);
  dd.classList.add('open');btn.classList.add('open');
}""", 'csToggle')

swap("""/* popover menus are placed with fixed coordinates, so any scroll or resize
   would leave them detached from their button - close them instead. */
document.addEventListener('scroll',function(e){if(e.target===document||(e.target.classList&&e.target.classList.contains('panel-body')))csCloseAll();},true);
window.addEventListener('resize',function(){csCloseAll();});""",
"""/* An open menu is fixed to the viewport, so scrolling or resizing would leave it
   detached from its button - keep it glued instead of closing it (closing a menu
   moments after the click is what made it flicker and vanish). */
var csRaf=0;
function csReposition(){
  if(csRaf)return;
  csRaf=(window.requestAnimationFrame||function(f){return setTimeout(f,16);})(function(){
    csRaf=0;
    var dd=document.querySelector('.cs-dd.open');
    if(!dd)return;
    var cs=dd.__cs,btn=cs&&cs.querySelector('.cs-btn');
    if(!btn){csCloseAll();return;}
    var r=btn.getBoundingClientRect();
    if(r.bottom<0||r.top>window.innerHeight){csCloseAll();return;}
    csPlaceMenu(btn,dd);
  });
}
document.addEventListener('scroll',csReposition,true);
window.addEventListener('resize',csReposition);""", 'scroll listeners')

swap("""/* Place a dropdown under (or above, when there is no room below) its button.
   The menu must stay glued to the button: it is never shifted away sideways to
   make it fit (that reads as a misplaced menu) - it shrinks instead, and for a
   button too close to the edge its right edge is aligned with the button. */
function csPlaceMenu(btn,dd){
  var r=btn.getBoundingClientRect(),o=fixedCBOrigin(dd),pad=8;
  dd.classList.add('cs-dd-pop');
  dd.style.position='fixed';dd.style.bottom='auto';
  /* min-width:100% on a fixed element resolves against its containing block,
     which here is the whole settings panel - that would overflow the window. */
  dd.style.minWidth='0';
  var want=Math.max(Math.round(r.width),200),room=window.innerWidth-pad-r.left;
  var w=want,left=r.left;
  if(room<want){
    if(room>=180)w=Math.round(room);
    else{left=r.right-want;}                 /* narrow button: align right edges */
    if(left<pad){left=pad;w=Math.min(w,window.innerWidth-2*pad);}
  }
  if(left+w>window.innerWidth-pad)left=window.innerWidth-pad-w;
  if(left<pad)left=pad;
  dd.style.width=Math.round(w)+'px';
  var h=dd.offsetHeight||0,below=window.innerHeight-r.bottom-pad,above=r.top-pad;
  var up=(h>below&&above>below),top=up?r.top-5-h:r.bottom+5;
  if(top<pad)top=pad;
  dd.style.left=Math.round(left-o.x)+'px';
  dd.style.top=Math.round(top-o.y)+'px';
  /* the fixed containing block may be an ancestor rather than the viewport, so
     correct the result against the box that was really rendered. */
  var a=dd.getBoundingClientRect(),dx=a.left-left,dy=a.top-top;
  if(Math.abs(dx)>0.5)dd.style.left=(parseFloat(dd.style.left)-dx)+'px';
  if(Math.abs(dy)>0.5)dd.style.top=(parseFloat(dd.style.top)-dy)+'px';
}""",
"""/* Put an open menu back inside its .cs wrapper (as it is while closed). */
function csRestore(dd){
  dd.classList.remove('open');dd.classList.remove('cs-dd-pop');
  dd.style.position='';dd.style.left='';dd.style.top='';dd.style.width='';
  dd.style.bottom='';dd.style.minWidth='';dd.style.zIndex='';dd.style.maxHeight='';
  var cs=dd.__cs;
  if(cs&&dd.parentElement!==cs){
    var b=cs.querySelector('.cs-btn');
    if(b&&b.parentElement===cs)cs.insertBefore(dd,b.nextSibling);else cs.appendChild(dd);
  }
}
/* Place a menu under (or above, when there is no room below) its button.
   An open menu is moved to <body> and positioned against the viewport: inside the
   settings panel it would otherwise be laid out against the panel (the panel has
   backdrop-filter, so it is the containing block of position:fixed children) and
   clipped away by the panel's overflow:hidden. The menu always stays glued to the
   button - it shrinks or right-aligns instead of being shifted sideways - and is
   clamped only as a last resort. */
function csPlaceMenu(btn,dd){
  var cs=dd.__cs||dd.parentElement;
  if(cs&&cs.classList&&cs.classList.contains('cs'))dd.__cs=cs;else cs=dd.__cs;
  if(dd.parentElement!==document.body)document.body.appendChild(dd);
  dd.classList.add('cs-dd-pop');
  dd.style.position='fixed';dd.style.bottom='auto';dd.style.zIndex='1200';
  /* min-width:100% would resolve against the whole viewport now. */
  dd.style.minWidth='0';
  var pad=8,r=btn.getBoundingClientRect();
  var want=Math.max(Math.round(r.width),200),room=window.innerWidth-pad-r.left;
  var w=want,left=Math.round(r.left);
  if(room<want){
    if(room>=180)w=Math.round(room);
    else{left=Math.round(r.right)-want;}     /* narrow button: align right edges */
    if(left<pad){left=pad;w=Math.min(w,window.innerWidth-2*pad);}
  }
  if(left+w>window.innerWidth-pad)left=Math.max(pad,window.innerWidth-pad-w);
  if(left<pad)left=pad;
  dd.style.width=Math.round(w)+'px';
  var h=dd.offsetHeight||0,below=window.innerHeight-pad-r.bottom,above=r.top-pad;
  var top=(h>below&&above>below)?Math.round(r.top)-6-h:Math.round(r.bottom)+6;
  if(top+h>window.innerHeight-pad)top=window.innerHeight-pad-h;
  if(top<pad)top=pad;
  dd.style.left=left+'px';
  dd.style.top=top+'px';
  /* last-resort correction against the box that was really rendered. */
  var a=dd.getBoundingClientRect(),dx=a.left-left,dy=a.top-top;
  if(Math.abs(dx)>0.5)dd.style.left=(left-dx)+'px';
  if(Math.abs(dy)>0.5)dd.style.top=(top-dy)+'px';
}""", 'csPlaceMenu')

swap("""function csPick(opt){
  var cs=opt.closest('.cs'),h=cs.querySelector('input[type="hidden"]'),btn=cs.querySelector('.cs-btn');
  cs.querySelectorAll('.cs-opt').forEach(function(o){o.classList.remove('sel');});
  opt.classList.add('sel');h.value=opt.dataset.val;
  btn.querySelector('.cs-txt').textContent=csLabel(opt);
  cs.querySelector('.cs-dd').classList.remove('open');btn.classList.remove('open');
  var dd=cs.querySelector('.cs-dd');dd.classList.remove('cs-dd-pop');dd.style.position='';dd.style.left='';dd.style.top='';dd.style.width='';dd.style.bottom='';dd.style.minWidth='';""",
"""function csPick(opt){
  var openDD=opt.closest('.cs-dd');   /* an open menu is parked in <body> */
  var cs=opt.closest('.cs')||(openDD&&openDD.__cs),h=cs.querySelector('input[type="hidden"]'),btn=cs.querySelector('.cs-btn');
  cs.querySelectorAll('.cs-opt').forEach(function(o){o.classList.remove('sel');});
  opt.classList.add('sel');h.value=opt.dataset.val;
  btn.querySelector('.cs-txt').textContent=csLabel(opt);
  var dd=openDD||cs.querySelector('.cs-dd');
  csRestore(dd);btn.classList.remove('open');""", 'csPick')

swap("""function csCloseAll(){
  document.querySelectorAll('.cs-dd.open').forEach(function(d){d.classList.remove('open');d.classList.remove('cs-dd-pop');d.style.position='';d.style.left='';d.style.top='';d.style.width='';d.style.bottom='';d.style.minWidth='';});""",
"""function csCloseAll(){
  document.querySelectorAll('.cs-dd.open,.cs-dd.cs-dd-pop').forEach(function(d){csRestore(d);});""",
     'csCloseAll')

swap("""document.addEventListener('click',function(e){if(!e.target.closest('.cs'))csCloseAll();});""",
     """document.addEventListener('click',function(e){if(!e.target.closest('.cs')&&!e.target.closest('.cs-dd'))csCloseAll();});""",
     'outside click')

open(p, 'w', encoding='utf-8', newline='').write(raw)
print('written')
