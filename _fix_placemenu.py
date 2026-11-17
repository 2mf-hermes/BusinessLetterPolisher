# -*- coding: utf-8 -*-
"""Rewrite csPlaceMenu with correct width clamping (min-width:100% fix)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

P = 'letter-polisher.html'
d = open(P, encoding='utf-8', newline='').read()

old = """function csPlaceMenu(btn,dd){\r
  var r=btn.getBoundingClientRect(),o=fixedCBOrigin(dd),w=Math.max(Math.round(r.width),200);\r
  dd.classList.add('cs-dd-pop');\r
  dd.style.position='fixed';dd.style.bottom='auto';dd.style.width=w+'px';\r
  var h=dd.offsetHeight||0,below=window.innerHeight-r.bottom-8,above=r.top-8;\r
  var up=(h>below&&above>below);\r
  var left=r.left-o.x;\r
  if(left+ w>window.innerWidth-8)left=window.innerWidth-w-8-o.x;\r
  if(left<8-o.x)left=8-o.x;\r
  dd.style.left=Math.round(left)+'px';\r
  dd.style.top=Math.round((up?r.top-5-h:r.bottom+5)-o.y)+'px';\r
}"""

new = """function csPlaceMenu(btn,dd){\r
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
}"""

if old not in d:
    print('FAIL: old csPlaceMenu not found verbatim')
    sys.exit(1)
d = d.replace(old, new, 1)

# reset minWidth wherever the menu styles are cleared
old2 = "dd.classList.remove('cs-dd-pop');dd.style.position='';dd.style.left='';dd.style.top='';dd.style.width='';dd.style.bottom='';"
new2 = "dd.classList.remove('cs-dd-pop');dd.style.position='';dd.style.left='';dd.style.top='';dd.style.width='';dd.style.bottom='';dd.style.minWidth='';"
if old2 not in d:
    print('FAIL: csPick reset line not found')
    sys.exit(1)
d = d.replace(old2, new2, 1)

old3 = "document.querySelectorAll('.cs-dd.open').forEach(function(d){d.classList.remove('open');d.classList.remove('cs-dd-pop');d.style.position='';d.style.left='';d.style.top='';d.style.width='';d.style.bottom='';});"
new3 = "document.querySelectorAll('.cs-dd.open').forEach(function(d){d.classList.remove('open');d.classList.remove('cs-dd-pop');d.style.position='';d.style.left='';d.style.top='';d.style.width='';d.style.bottom='';d.style.minWidth='';});"
if old3 not in d:
    print('FAIL: csCloseAll reset line not found')
    sys.exit(1)
d = d.replace(old3, new3, 1)

open(P, 'w', encoding='utf-8', newline='').write(d)
print('OK: csPlaceMenu rewritten, resets updated')
