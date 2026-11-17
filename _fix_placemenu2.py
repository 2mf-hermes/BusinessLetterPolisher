# -*- coding: utf-8 -*-
"""Rewrite csPlaceMenu: keep the menu glued to its button (never shift it away),
shrink or right-align when space is tight, and self-correct the final position.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

P = 'letter-polisher.html'
d = open(P, encoding='utf-8', newline='').read()

old = """/* Place a dropdown under (or above, when there is no room below) its button,\r
   always fully inside the window. */\r
function csPlaceMenu(btn,dd){\r
  var r=btn.getBoundingClientRect(),o=fixedCBOrigin(dd),w=Math.max(Math.round(r.width),200);\r
  dd.classList.add('cs-dd-pop');\r
  dd.style.position='fixed';dd.style.bottom='auto';\r
  /* min-width:100% on a fixed element resolves against its containing block,\r
     which here is the whole settings panel - that would overflow the window. */\r
  dd.style.minWidth='0';\r
  dd.style.width=w+'px';\r
  w=dd.offsetWidth||w;\r
  var h=dd.offsetHeight||0,below=window.innerHeight-r.bottom-8,above=r.top-8;\r
  var up=(h>below&&above>below);\r
  var vleft=r.left;\r
  if(vleft+w>window.innerWidth-8)vleft=window.innerWidth-8-w;\r
  if(vleft<8)vleft=8;\r
  var vtop=up?r.top-5-h:r.bottom+5;\r
  if(vtop<8)vtop=8;\r
  dd.style.left=Math.round(vleft-o.x)+'px';\r
  dd.style.top=Math.round(vtop-o.y)+'px';\r
}\r
"""

new = """/* Place a dropdown under (or above, when there is no room below) its button.\r
   The menu must stay glued to the button: it is never shifted away sideways to\r
   make it fit (that reads as a misplaced menu) - it shrinks instead, and for a\r
   button too close to the edge its right edge is aligned with the button. */\r
function csPlaceMenu(btn,dd){\r
  var r=btn.getBoundingClientRect(),o=fixedCBOrigin(dd),pad=8;\r
  dd.classList.add('cs-dd-pop');\r
  dd.style.position='fixed';dd.style.bottom='auto';\r
  /* min-width:100% on a fixed element resolves against its containing block,\r
     which here is the whole settings panel - that would overflow the window. */\r
  dd.style.minWidth='0';\r
  var want=Math.max(Math.round(r.width),200),room=window.innerWidth-pad-r.left;\r
  var w=want,left=r.left;\r
  if(room<want){\r
    if(room>=180)w=Math.round(room);\r
    else{left=r.right-want;}                 /* narrow button: align right edges */\r
    if(left<pad){left=pad;w=Math.min(w,window.innerWidth-2*pad);}\r
  }\r
  if(left+w>window.innerWidth-pad)left=window.innerWidth-pad-w;\r
  if(left<pad)left=pad;\r
  dd.style.width=Math.round(w)+'px';\r
  var h=dd.offsetHeight||0,below=window.innerHeight-r.bottom-pad,above=r.top-pad;\r
  var up=(h>below&&above>below),top=up?r.top-5-h:r.bottom+5;\r
  if(top<pad)top=pad;\r
  dd.style.left=Math.round(left-o.x)+'px';\r
  dd.style.top=Math.round(top-o.y)+'px';\r
  /* the fixed containing block may be an ancestor rather than the viewport, so\r
     correct the result against the box that was really rendered. */\r
  var a=dd.getBoundingClientRect(),dx=a.left-left,dy=a.top-top;\r
  if(Math.abs(dx)>0.5)dd.style.left=(parseFloat(dd.style.left)-dx)+'px';\r
  if(Math.abs(dy)>0.5)dd.style.top=(parseFloat(dd.style.top)-dy)+'px';\r
}\r
"""

if old not in d:
    print('FAIL: csPlaceMenu not found verbatim')
    sys.exit(1)
open(P, 'w', encoding='utf-8', newline='').write(d.replace(old, new, 1))
print('OK: csPlaceMenu rewritten (glued placement + self-correction)')
