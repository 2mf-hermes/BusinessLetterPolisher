# -*- coding: utf-8 -*-
"""Reproduce the 'quick preset does nothing' report.

Builds `_preset.html` and, in a real browser, clicks the Groq quick-preset chip
and records every observable side effect (fields, provider store, cfg, the
'current provider' summary line and whether the connection block is visible).

Run: python _preset_probe.py && python _run_probe.py _preset.html 5000 1194,877
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

PROBE = r"""
<div id="probeOut" style="display:none"></div>
<script>
(function(){
  var log=[];
  function rec(s){log.push(s);}
  function v(id){var e=document.getElementById(id);return e?e.value:'<missing '+id+'>';}
  function txt(sel){var e=document.querySelector(sel);return e?e.textContent.replace(/\s+/g,' ').trim():'<missing '+sel+'>';}
  window.addEventListener('load',function(){
    var raf=window.requestAnimationFrame;window.requestAnimationFrame=function(cb){cb();return 0;};
    try{
      var st=localStorage.getItem('bp_providers');
      rec('stored providers before: '+(st||'(none)'));
      initProviders();
      toggleSP();
      var chips=document.querySelectorAll('#presetChips .chip');
      rec('chips rendered: '+chips.length+' -> '+Array.prototype.map.call(chips,function(c){return c.textContent.trim();}).join('|'));
      var chip=null;
      Array.prototype.forEach.call(chips,function(c){if(c.textContent.trim()==='Groq')chip=c;});
      if(!chip){rec('ERR no Groq chip');}
      else{
        rec('BEFORE click: url='+v('apiUrl')+' model='+v('modelName')+' fmt='+v('apiFormat')+' provName='+v('provName'));
        rec('BEFORE block open='+document.getElementById('provEditBox').classList.contains('open')+' cur=['+txt('.prov-cur')+']');
        rec('BEFORE cfg: url='+(cfg.apiUrl||'')+' model='+(cfg.modelName||''));
        chip.click();
        rec('AFTER click: url='+v('apiUrl')+' model='+v('modelName')+' fmt='+v('apiFormat')+' provName='+v('provName'));
        rec('AFTER click block open='+document.getElementById('provEditBox').classList.contains('open')+' cur=['+txt('.prov-cur')+']');
        rec('AFTER click cfg: url='+(cfg.apiUrl||'')+' model='+(cfg.modelName||''));
        rec('AFTER click chip.on='+(chip.classList.contains('on')));
        /* what did the provider store get? */
        var ps=[];try{ps=JSON.parse(localStorage.getItem('bp_providers')||'[]');}catch(e){}
        rec('stored providers after click: '+JSON.stringify(ps));
        /* now press save, then reopen the panel from storage */
        var sb=document.querySelector('.btn[onclick="saveCfg()"]');
        if(sb)sb.click();else rec('ERR no save button');
        try{ps=JSON.parse(localStorage.getItem('bp_providers')||'[]');}catch(e){}
        rec('stored providers after save: '+JSON.stringify(ps));
        rec('bp_cfg after save: '+(localStorage.getItem('bp_cfg')||'(none)').substring(0,300));
        /* reload the provider state the way a fresh app start would */
        providers=[];activeProvId='';initProviders();
        rec('AFTER reload: block open='+document.getElementById('provEditBox').classList.contains('open')+
            ' name='+v('provName')+' url='+v('apiUrl')+' model='+v('modelName')+' fmt='+v('apiFormat')+
            ' cur=['+txt('.prov-cur')+']');
        rec('AFTER reload cfg: url='+(cfg.apiUrl||'')+' fmt='+(cfg.apiFormat||'')+' model='+(cfg.modelName||''));
      }
    }catch(e){rec('ERR '+e.message+' @ '+(e.stack||'').split('\n')[1]);}
    window.requestAnimationFrame=raf;
    document.getElementById('probeOut').textContent=log.join('\n');
  });
})();
</script>
</body>"""

src = sys.argv[1] if len(sys.argv) > 1 else 'letter-polisher.html'
out = '_preset.html'

s = open(src, encoding='utf-8', newline='').read()
assert '<div id="probeOut"' not in s, 'source already contains a probe'
assert s.count('</body>') == 1
open(out, 'w', encoding='utf-8', newline='').write(s.replace('</body>', PROBE.replace('\n', '\r\n')))
print('wrote %s from %s' % (out, src))
