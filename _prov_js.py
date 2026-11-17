import io

PATH = 'letter-polisher.html'
with io.open(PATH, 'r', encoding='utf-8', newline='') as f:
    html = f.read()


def sub(old, new, count=1):
    global html
    n = html.count(old)
    assert n == count, 'anchor count %d (expected %d) for: %s' % (n, count, old[:70])
    html = html.replace(old, new, count)


# ---------- 1. provider selection hooks inside csPick ----------
sub(
    "var id=h.id;if(id==='tone'||id==='purpose'||id==='letterLang'||id==='polishMode'||id==='outLang'||id==='srcRegion'||id==='outRegion'){csLetterOptPick(id);}",
    "var id=h.id;if(id==='tone'||id==='purpose'||id==='letterLang'||id==='polishMode'||id==='outLang'||id==='srcRegion'||id==='outRegion'){csLetterOptPick(id);}else if(id==='provider')onProviderPick(opt.dataset.val);else if(id==='modelPick')onModelPick(opt.dataset.val);",
)

# ---------- 2. csSyncAll must skip the dynamic pickers ----------
sub(
    'var h=cs.querySelector(\'input[type="hidden"]\');if(!h)return;',
    'if(cs.classList.contains(\'cs-nosync\'))return;var h=cs.querySelector(\'input[type="hidden"]\');if(!h)return;',
)

# ---------- 3. settings persistence ----------
sub(
    "function saveCfg(){cfg.apiUrl=v('apiUrl');cfg.apiKey=v('apiKey');cfg.modelName=v('modelName');cfg.temperature=parseFloat(v('temperature'))||0.7;cfg.apiFormat=v('apiFormat');cfg.customSystemPrompt=v('sysPrompt');cfg.customTone=v('customToneVal');cfg.customPurpose=v('customPurpVal');localStorage.setItem('bp_cfg',JSON.stringify(cfg));toast(t('save')",
    "function saveCfg(){cfg.temperature=parseFloat(v('temperature'))||0.7;cfg.customSystemPrompt=v('sysPrompt');cfg.customTone=v('customToneVal');cfg.customPurpose=v('customPurpVal');persistActiveProvider();applyActiveProvider();refreshProviderDD();localStorage.setItem('bp_cfg',JSON.stringify(cfg));toast(t('save')",
)

sub(
    "function autoSave(){cfg.apiUrl=v('apiUrl');cfg.apiKey=v('apiKey');cfg.modelName=v('modelName');cfg.temperature=parseFloat(v('temperature'))||0.7;cfg.apiFormat=v('apiFormat');cfg.customSystemPrompt=v('sysPrompt');cfg.customTone=v('customToneVal');cfg.customPurpose=v('customPurpVal');localStorage.setItem('bp_cfg',JSON.stringify(cfg));}",
    "function autoSave(){cfg.temperature=parseFloat(v('temperature'))||0.7;cfg.customSystemPrompt=v('sysPrompt');cfg.customTone=v('customToneVal');cfg.customPurpose=v('customPurpVal');persistActiveProvider();applyActiveProvider();}",
)

sub(
    "function applyPreset(k,el){var p=PR[k];sV('apiUrl',p.u);sV('modelName',p.m);sV('apiFormat',p.f);csSyncAll();document.querySelectorAll('.chip').forEach(function(c){c.classList.remove('on');});if(el)el.classList.add('on');}",
    "function applyPreset(k,el){var p=PR[k];sV('apiUrl',p.u);sV('modelName',p.m);sV('apiFormat',p.f);if(!v('provName'))sV('provName',t(p.k));var ap=activeProv();if(ap)ap.models=[];csSyncAll();refreshModelDD();persistActiveProvider();applyActiveProvider();refreshProviderDD();document.querySelectorAll('.chip').forEach(function(c){c.classList.remove('on');});if(el)el.classList.add('on');}",
)

# ---------- 4. boot sequence ----------
sub(
    '  loadTheme();loadCfg();fillF();',
    '  loadTheme();loadCfg();initProviders();fillF();',
)

# ---------- 5. provider module ----------
MODULE = r"""/* ===== AI Providers ===== */
var providers=[],activeProvId='';
function newProvId(){return 'p'+Date.now().toString(36)+Math.random().toString(36).slice(2,6);}
function activeProv(){for(var i=0;i<providers.length;i++)if(providers[i].id===activeProvId)return providers[i];return providers[0]||null;}
function saveProviders(){try{localStorage.setItem('bp_providers',JSON.stringify(providers));localStorage.setItem('bp_active_provider',activeProvId);}catch(e){}}
function providerNameFor(url,fmt){if(url){for(var k in PR)if(PR[k].u===url)return t(PR[k].k);}return fmt==='anthropic'?'Anthropic':fmt==='gemini'?'Gemini':t('provDefault');}
function loadProviders(){
  var s=localStorage.getItem('bp_providers');
  if(s)try{var a=JSON.parse(s);if(a&&a.length)providers=a;}catch(e){}
  activeProvId=localStorage.getItem('bp_active_provider')||'';
  if(!providers.length){
    var lg={};try{lg=JSON.parse(localStorage.getItem('bp_cfg')||'{}')||{};}catch(e){}
    var url=lg.apiUrl||cfg.apiUrl||'',key=lg.apiKey||cfg.apiKey||'',fmt=lg.apiFormat||cfg.apiFormat||'openai',mdl=lg.modelName||cfg.modelName||'';
    if(url||key)providers.push({id:newProvId(),name:providerNameFor(url,fmt),url:url,key:key,format:fmt,model:mdl,models:[]});
  }
  if(!providers.length)providers.push({id:newProvId(),name:t('provDefault'),url:'',key:'',format:'openai',model:'',models:[]});
  providers.forEach(function(p){if(!p.id)p.id=newProvId();if(!p.format)p.format='openai';if(!p.name)p.name=t('provDefault');if(!(p.models instanceof Array))p.models=[];});
  var hit=false;for(var i=0;i<providers.length;i++)if(providers[i].id===activeProvId)hit=true;
  if(!hit)activeProvId=providers[0].id;
  saveProviders();
}
function persistActiveProvider(){
  var p=activeProv();if(!p||!$('apiUrl')||!$('modelName'))return;
  if($('provName'))p.name=v('provName');
  p.url=v('apiUrl');p.key=v('apiKey');p.format=v('apiFormat');p.model=v('modelName');
  saveProviders();
}
function fillProviderFields(){
  var p=activeProv();if(!p)return;
  sV('provName',p.name||'');sV('apiUrl',p.url||'');sV('apiKey',p.key||'');sV('apiFormat',p.format||'openai');sV('modelName',p.model||'');
  csSyncAll();
}
function applyActiveProvider(){
  var p=activeProv();if(!p)return;
  cfg.apiUrl=p.url||'';cfg.apiKey=p.key||'';cfg.modelName=p.model||'';cfg.apiFormat=p.format||'openai';
  try{localStorage.setItem('bp_cfg',JSON.stringify(cfg));}catch(e){}
}
function refreshProviderDD(){
  var dd=$('provDD');if(!dd)return;
  dd.innerHTML=providers.map(function(p){return '<div class="cs-opt'+(p.id===activeProvId?' sel':'')+'" data-val="'+p.id+'" onclick="csPick(this)"><span>'+esc(p.name||'')+'</span><span class="cs-chk">\u2713</span></div>';}).join('');
  var cs=$('provCS');if(cs){var tx=cs.querySelector('.cs-txt');if(tx)tx.textContent=(activeProv()||{}).name||'';}
  var h=$('provider');if(h)h.value=activeProvId;
}
function onProviderPick(id){
  if(!id||id===activeProvId)return;
  persistActiveProvider();
  activeProvId=id;saveProviders();
  fillProviderFields();refreshProviderDD();refreshModelDD();applyActiveProvider();
}
function initProviders(){loadProviders();refreshProviderDD();fillProviderFields();refreshModelDD();applyActiveProvider();}
function newProvider(){
  persistActiveProvider();
  var p={id:newProvId(),name:t('provDefault')+' '+(providers.length+1),url:'',key:'',format:'openai',model:'',models:[]};
  providers.push(p);activeProvId=p.id;saveProviders();
  fillProviderFields();refreshProviderDD();refreshModelDD();applyActiveProvider();
  toast(t('provAdded'));
  var el=$('provName');if(el){el.focus();el.select();}
}
function deleteProvider(){
  if(providers.length<=1){toast(t('provLastOne'));return;}
  if(!window.confirm(t('provDeleteConfirm')))return;
  providers=providers.filter(function(p){return p.id!==activeProvId;});
  activeProvId=providers[0].id;saveProviders();
  fillProviderFields();refreshProviderDD();refreshModelDD();applyActiveProvider();
  toast(t('provDeleted'));
}
function modelsUrlFor(url,fmt){
  var u=(url||'').trim().replace(/\/+$/,'');if(!u)return '';
  if(fmt==='gemini'){var m=u.match(/^(.*\/models)\/[^\/:]+(?::[A-Za-z]+)?$/);if(m)return m[1];if(/\/models$/.test(u))return u;return u.replace(/\/v1beta\/.*$/,'/v1beta/models');}
  if(fmt==='anthropic'){if(/\/messages$/.test(u))return u.replace(/\/messages$/,'/models');if(/\/models$/.test(u))return u;}
  if(/\/chat\/completions$/.test(u))return u.replace(/\/chat\/completions$/,'/models');
  if(/\/completions$/.test(u))return u.replace(/\/completions$/,'/models');
  if(/\/models$/.test(u))return u;
  return u+'/models';
}
function parseModelList(d,fmt){
  var out=[],seen={};function add(x){x=String(x||'').replace(/^models\//,'');if(!x||seen[x])return;seen[x]=1;out.push(x);}
  if(fmt==='gemini'){((d&&d.models)||[]).forEach(function(m){if(m.supportedGenerationMethods&&m.supportedGenerationMethods.indexOf('generateContent')<0)return;add(m.name);});}
  else{((d&&(d.data||d.models))||[]).forEach(function(m){add(m.id||m.name);});}
  out.sort();return out;
}
function refreshModelDD(){
  var dd=$('modelDD');if(!dd)return;
  var list=(activeProv()||{}).models||[];
  dd.innerHTML=list.map(function(m){return '<div class="cs-opt" data-val="'+esc(m)+'" onclick="csPick(this)"><span>'+esc(m)+'</span><span class="cs-chk">\u2713</span></div>';}).join('');
}
function onModelPick(val){
  if(!val)return;
  var inp=$('modelName');if(inp)inp.value=val;
  var p=activeProv();if(p){p.model=val;saveProviders();}
  applyActiveProvider();
}
async function fetchModelList(){
  var p=activeProv();if(!p)return null;
  persistActiveProvider();
  if(!String(p.url||'').trim()){showTR(t('needUrl'),'err');return null;}
  if(!String(p.key||'').trim()){showTR(t('needKey'),'err');return null;}
  var url=modelsUrlFor(p.url,p.format),btn=$('loadModelsBtn');
  if(btn){btn.disabled=true;var lb=btn.querySelector('.cs-txt');if(lb)lb.textContent=t('loadingModels');}
  showTR(t('loadingModels'),'info');
  try{
    var res;
    if(p.format==='anthropic')res=await fetch(url,{headers:{'x-api-key':p.key,'anthropic-version':'2023-06-01'}});
    else if(p.format==='gemini')res=await fetch(url+(url.indexOf('?')>=0?'&':'?')+'key='+encodeURIComponent(p.key));
    else res=await fetch(url,{headers:{'Authorization':'Bearer '+p.key}});
    if(!res.ok){var b=await res.text();throw new Error(res.status+': '+String(b).substring(0,160));}
    var list=parseModelList(await res.json(),p.format);
    if(!list.length){showTR(t('noModels'),'err');return null;}
    p.models=list;saveProviders();refreshModelDD();
    showTR(t('modelsLoaded')+' '+list.length,'ok');
    return list;
  }catch(e){showTR(t('modelsFail')+' ('+e.message+')','err');return null;}
  finally{if(btn){btn.disabled=false;var lb2=btn.querySelector('.cs-txt');if(lb2)lb2.textContent=t('loadModels');}}
}
async function openModelPicker(btn){
  var p=activeProv();if(!p)return;
  if(!(p.models&&p.models.length)){var list=await fetchModelList();if(!list)return;}
  refreshModelDD();
  var dd=$('modelDD');if(!dd||!dd.children.length)return;
  csCloseAll();
  var r=btn.getBoundingClientRect(),w=Math.max(220,r.width),left=r.left;
  if(left+w>window.innerWidth-10)left=Math.max(8,window.innerWidth-w-10);
  dd.style.position='fixed';dd.style.left=left+'px';dd.style.top=(r.bottom+5)+'px';dd.style.width=w+'px';dd.style.bottom='auto';
  dd.classList.add('open');btn.classList.add('open');
}

/* ===== Presets ===== */"""

sub('/* ===== Presets ===== */', MODULE, 1)

# ---------- 6. i18n strings ----------
TW = ("aiProvider:'AI \u4f9b\u61c9\u5546',provLabel:'\u4f9b\u61c9\u5546',provName:'\u4f9b\u61c9\u5546\u540d\u7a31',"
      "provNew:'\u65b0\u589e\u4f9b\u61c9\u5546',provDel:'\u522a\u9664',provDefault:'AI \u4f9b\u61c9\u5546',"
      "provAdded:'\u5df2\u65b0\u589e\u4f9b\u61c9\u5546',provDeleted:'\u5df2\u522a\u9664\u4f9b\u61c9\u5546',"
      "provDeleteConfirm:'\u78ba\u5b9a\u8981\u522a\u9664\u9019\u500b\u4f9b\u61c9\u5546\u55ce\uff1f\u522a\u9664\u5f8c\u7121\u6cd5\u5fa9\u539f\u3002',"
      "provLastOne:'\u81f3\u5c11\u8981\u4fdd\u7559\u4e00\u500b\u4f9b\u61c9\u5546',"
      "needKey:'\u8acb\u5148\u8f38\u5165 API Key \u518d\u8f09\u5165\u6a21\u578b',"
      "needUrl:'\u8acb\u5148\u8f38\u5165 AI URL \u518d\u8f09\u5165\u6a21\u578b',"
      "loadModels:'\u8f09\u5165\u6a21\u578b',loadingModels:'\u6b63\u5728\u8f09\u5165\u6a21\u578b\u6e05\u55ae\u2026',"
      "modelsLoaded:'\u5df2\u8f09\u5165\u6a21\u578b\u6e05\u55ae\uff0c\u5171',"
      "modelsFail:'\u7121\u6cd5\u8f09\u5165\u6a21\u578b\u6e05\u55ae\uff0c\u8acb\u76f4\u63a5\u8f38\u5165\u6a21\u578b\u540d\u7a31',"
      "noModels:'\u6b64\u4f9b\u61c9\u5546\u6c92\u6709\u56de\u50b3\u53ef\u7528\u7684\u6a21\u578b',")

CN = ("aiProvider:'AI \u4f9b\u5e94\u5546',provLabel:'\u4f9b\u5e94\u5546',provName:'\u4f9b\u5e94\u5546\u540d\u79f0',"
      "provNew:'\u65b0\u589e\u4f9b\u5e94\u5546',provDel:'\u5220\u9664',provDefault:'AI \u4f9b\u5e94\u5546',"
      "provAdded:'\u5df2\u65b0\u589e\u4f9b\u5e94\u5546',provDeleted:'\u5df2\u5220\u9664\u4f9b\u5e94\u5546',"
      "provDeleteConfirm:'\u786e\u5b9a\u8981\u5220\u9664\u8fd9\u4e2a\u4f9b\u5e94\u5546\u5417\uff1f\u5220\u9664\u540e\u65e0\u6cd5\u6062\u590d\u3002',"
      "provLastOne:'\u81f3\u5c11\u8981\u4fdd\u7559\u4e00\u4e2a\u4f9b\u5e94\u5546',"
      "needKey:'\u8bf7\u5148\u8f93\u5165 API Key \u518d\u8f7d\u5165\u6a21\u578b',"
      "needUrl:'\u8bf7\u5148\u8f93\u5165 AI URL \u518d\u8f7d\u5165\u6a21\u578b',"
      "loadModels:'\u8f7d\u5165\u6a21\u578b',loadingModels:'\u6b63\u5728\u8f7d\u5165\u6a21\u578b\u6e05\u5355\u2026',"
      "modelsLoaded:'\u5df2\u8f7d\u5165\u6a21\u578b\u6e05\u5355\uff0c\u5171',"
      "modelsFail:'\u65e0\u6cd5\u8f7d\u5165\u6a21\u578b\u6e05\u5355\uff0c\u8bf7\u76f4\u63a5\u8f93\u5165\u6a21\u578b\u540d\u79f0',"
      "noModels:'\u6b64\u4f9b\u5e94\u5546\u6ca1\u6709\u56de\u4f20\u53ef\u7528\u7684\u6a21\u578b',")

EN = ("aiProvider:'AI Provider',provLabel:'Provider',provName:'Provider Name',"
      "provNew:'Add Provider',provDel:'Delete',provDefault:'AI Provider',"
      "provAdded:'Provider added',provDeleted:'Provider deleted',"
      "provDeleteConfirm:'Delete this provider? This cannot be undone.',"
      "provLastOne:'At least one provider must be kept',"
      "needKey:'Enter an API key before loading models',"
      "needUrl:'Enter the AI URL before loading models',"
      "loadModels:'Load Models',loadingModels:'Loading model list\u2026',"
      "modelsLoaded:'Model list loaded:',"
      "modelsFail:'Could not load the model list; type the model name instead',"
      "noModels:'This provider returned no usable models',")

positions, pos = [], html.find('updErrorTitle:')
while pos >= 0:
    positions.append(pos)
    pos = html.find('updErrorTitle:', pos + 1)
assert len(positions) == 3, 'expected 3 i18n anchor spots, got %d' % len(positions)

# insert back-to-front so earlier offsets stay valid; order = zh-TW, zh-CN, en
for block, idx in reversed(list(zip((TW, CN, EN), positions))):
    html = html[:idx] + block + html[idx:]

with io.open(PATH, 'w', encoding='utf-8', newline='') as f:
    f.write(html)

print('patched; %d chars, %d lines' % (len(html), html.count('\n') + 1))
