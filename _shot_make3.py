# -*- coding: utf-8 -*-
"""Build screenshot pages for the input-card arrangement, before and after.

python _shot_make3.py            -> current letter-polisher.html
python _shot_make3.py _before106.html -> the previous release
"""
import io
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
tag = 'after' if src == 'letter-polisher.html' else 'before'
out = '_shot_%s.html' % tag

INJECT = r"""
<script>
(function(){
  window.addEventListener('load',function(){
    var raf=window.requestAnimationFrame;window.requestAnimationFrame=function(cb){cb();return 0;};
    try{
      var a=document.querySelector('.cs-opt[data-val="custom"]');
      if(a)csPick(a);
      var b=document.querySelector('.cs-opt[data-val="custom-purpose"]');
      if(b)csPick(b);
    }catch(e){document.title='inject err '+e;}
    try{
      var t=document.getElementById('customToneVal');
      if(t)t.value='語氣專業但不失親切，避免過度客套';
      var p=document.getElementById('customPurpVal');
      if(p)p.value='向既有客戶說明本次報價調整的原因';
    }catch(e){}
    try{
      var ein=document.getElementById('letterIn');
      if(ein&&!ein.value)ein.value='Hi John,\n\nI want to talk about the new price for the next order. '+
        'Our cost went up a lot this year so we have to change it.\n\nPlease let me know what you think.\n\nThanks,\nMike';
      if(window.updCount)updCount();
    }catch(e){}
  });
})();
</script>
</body>"""

s = io.open(src, encoding='utf-8', newline='').read()
assert s.count('</body>') == 1
io.open(out, 'w', encoding='utf-8', newline='').write(s.replace('</body>', INJECT.replace('\n', '\r\n')))
print('wrote %s from %s' % (out, src))

for png, size in [('ui-input-%s.png' % tag, '1194,877'), ('ui-input-%s-narrow.png' % tag, '560,900')]:
    subprocess.run([sys.executable, '_shot_run.py', out, png, '6000', size], timeout=300)
