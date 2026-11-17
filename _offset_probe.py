# -*- coding: utf-8 -*-
"""Diagnostic: how far is each dropdown offset from its button?

Runs headless Edge at the real application window size (1194x877, the size the
host app fits to) and reports the rendered geometry of button / menu / first
option for every custom select, including the ones inside the settings sheet.
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

HTML = 'letter-polisher.html'
PROBE_PAGE = '_offset_probe.html'
PORT = 8971
URL = 'http://127.0.0.1:%d/%s' % (PORT, PROBE_PAGE)
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

KILL = '<style id="__kill">*{transition:none!important;animation:none!important;}</style>'

PROBE = r"""
<script>
window.__out=[];
function __m(name,btnSel,ddSel){
  var btn=document.querySelector(btnSel),dd=document.querySelector(ddSel),rec={name:name};
  if(!btn||!dd){rec.err='missing';window.__out.push(rec);return;}
  btn.click();
  var cs=getComputedStyle(dd),r=dd.getBoundingClientRect(),br=btn.getBoundingClientRect();
  rec.open=dd.classList.contains('open');
  rec.opacity=cs.opacity;
  rec.btn=[+br.left.toFixed(1),+br.top.toFixed(1),+br.width.toFixed(1),+br.bottom.toFixed(1)];
  rec.dd=[+r.left.toFixed(1),+r.top.toFixed(1),+r.width.toFixed(1),+r.bottom.toFixed(1)];
  rec.dx=+(r.left-br.left).toFixed(1);
  rec.dy=+(r.top-br.bottom).toFixed(1);
  rec.dright=+(r.right-br.right).toFixed(1);
  rec.inlineLeft=dd.style.left;rec.inlineTop=dd.style.top;rec.inlineW=dd.style.width;
  rec.win=[window.innerWidth,window.innerHeight];
  rec.panelOrigin=(function(){try{return fixedCBOrigin(dd);}catch(e){return String(e);}})();
  csCloseAll();
  window.__out.push(rec);
}
window.addEventListener('DOMContentLoaded',function(){
  function step(fn,d){return new Promise(function(res){setTimeout(function(){try{fn();}catch(e){window.__out.push({name:'EX',err:String(e&&e.message||e)});}res();},d);});}
  step(function(){var g=document.getElementById('guideOv');if(g)g.remove();},350)
  .then(function(){return step(function(){toggleSP();},250);})
  .then(function(){return step(function(){__m('provCS','#provCS .cs-btn','#provDD');},150);})
  .then(function(){return step(function(){__m('apiFormatCS','#apiFormatCS .cs-btn','#apiFormatCS .cs-dd');},150);})
  .then(function(){return step(function(){
      var p=(typeof activeProv==='function')?activeProv():null;
      if(p){p.models=['gpt-4o','gpt-4o-mini','claude-sonnet-4-20250514','gemini-2.0-flash'];refreshModelDD();}
      __m('modelCS','#modelCS .cs-btn','#modelDD');},150);})
  .then(function(){return step(function(){newProvider();},150);})
  .then(function(){return step(function(){__m('provCS-after-add','#provCS .cs-btn','#provDD');},150);})
  .then(function(){return step(function(){
      var el=document.createElement('pre');el.id='probeOut';el.style.display='none';
      el.textContent=JSON.stringify(window.__out);document.body.appendChild(el);},60);});
});
</script>
"""


def build():
    src = open(HTML, encoding='utf-8', newline='').read()
    out = src.replace('</head>', KILL + '\n</head>')
    out = out.replace('</body>', PROBE + '\n</body>')
    open(PROBE_PAGE, 'w', encoding='utf-8', newline='').write(out)


def run(size):
    dom = os.path.join(os.environ.get('TEMP', '.'), 'offset_dom_%s.html' % size.replace(',', 'x'))
    profile = os.path.join(os.environ.get('TEMP', '.'), 'edge_offset_probe')
    shutil.rmtree(profile, ignore_errors=True)
    args = ['--headless=new', '--disable-gpu', '--no-first-run', '--window-size=' + size,
            '--user-data-dir=' + profile, '--virtual-time-budget=9000', '--dump-dom', URL]
    with open(dom, 'w', encoding='utf-8', errors='replace') as fh:
        subprocess.run([EDGE] + args, stdout=fh, stderr=subprocess.DEVNULL, timeout=120)
    d = open(dom, encoding='utf-8', errors='replace').read()
    m = re.search(r'<pre id="probeOut"[^>]*>(.*?)</pre>', d, re.S)
    if not m:
        print('  no probe output'); return
    txt = m.group(1).replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    for rec in json.loads(txt):
        print('  %-20s win=%s btn=%s dd=%s dx=%s dy=%s dright=%s inline=%s,%s,%s'
              % (rec.get('name'), rec.get('win'), rec.get('btn'), rec.get('dd'), rec.get('dx'),
                 rec.get('dy'), rec.get('dright'), rec.get('inlineLeft'), rec.get('inlineTop'),
                 rec.get('inlineW')), rec.get('err') or '')


if __name__ == '__main__':
    build()
    for size in ['1194,877', '1400,1000']:
        print('=== window %s ===' % size)
        run(size)
