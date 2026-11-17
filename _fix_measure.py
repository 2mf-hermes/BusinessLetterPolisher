# -*- coding: utf-8 -*-
"""Neutralise the closed-state transform while measuring, so the placement is not
thrown off by the scale(.98)/translateY(-4px) of the closed menu (that shift was
what left the menu a few pixels away from its button)."""
import sys

sys.stdout.reconfigure(encoding='utf-8')
p = 'letter-polisher.html'
raw = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'


def swap(old, new, label):
    global raw
    o, n = old.replace('\n', nl), new.replace('\n', nl)
    if raw.count(o) != 1:
        print('FAIL %s: %d matches' % (label, raw.count(o)))
        sys.exit(1)
    raw = raw.replace(o, n, 1)
    print('ok', label)


swap("""  dd.classList.add('cs-dd-pop');
  dd.style.position='fixed';dd.style.bottom='auto';dd.style.zIndex='1200';""",
     """  dd.classList.add('cs-dd-pop');
  dd.style.position='fixed';dd.style.bottom='auto';dd.style.zIndex='1200';
  /* a closed menu is scaled down / nudged up by CSS; measure without that, or the
     correction below would chase the transform of the previous state. */
  dd.style.transform='none';""", 'reset transform')

swap("""  var h=dd.offsetHeight||0,below=window.innerHeight-pad-r.bottom,above=r.top-pad;
  var top=(h>below&&above>below)?Math.round(r.top)-6-h:Math.round(r.bottom)+6;""",
     """  var h=dd.offsetHeight||0,below=window.innerHeight-pad-r.bottom,above=r.top-pad;
  var top=(h>below&&above>below)?Math.round(r.top)-5-h:Math.round(r.bottom)+5;""", 'gap 5px')

swap("""  var a=dd.getBoundingClientRect(),dx=a.left-left,dy=a.top-top;
  if(Math.abs(dx)>0.5)dd.style.left=(left-dx)+'px';
  if(Math.abs(dy)>0.5)dd.style.top=(top-dy)+'px';
}""",
     """  var a=dd.getBoundingClientRect(),dx=a.left-left,dy=a.top-top;
  if(Math.abs(dx)>0.5)dd.style.left=(left-dx)+'px';
  if(Math.abs(dy)>0.5)dd.style.top=(top-dy)+'px';
  dd.style.transform='';
}""", 'restore transform')

swap("""  dd.style.position='';dd.style.left='';dd.style.top='';dd.style.width='';
  dd.style.bottom='';dd.style.minWidth='';dd.style.zIndex='';dd.style.maxHeight='';""",
     """  dd.style.position='';dd.style.left='';dd.style.top='';dd.style.width='';
  dd.style.bottom='';dd.style.minWidth='';dd.style.zIndex='';dd.style.maxHeight='';
  dd.style.transform='';""", 'restore clears transform')

open(p, 'w', encoding='utf-8', newline='').write(raw)
print('written')
