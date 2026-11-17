# -*- coding: utf-8 -*-
"""v2026.10.01.5 patch.

1. The real cause of "the dropdown jumps and disappears": .cs-dd animated `all`,
   so the geometry moved while csPlaceMenu() was measuring it (a transition reports
   its START value on the first synchronous getBoundingClientRect()), and the
   self-correction then pushed the menu far off screen. Menus now animate opacity
   only, geometry is frozen (`.cs-dd-fx`) while they are placed, and the correction
   is bounded.
2. The URL / API key / model block is hidden until you press Add or Edit, with a
   tidier two-column arrangement.
"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')

PATH = 'letter-polisher.html'
NL = '\r\n'
src = open(PATH, encoding='utf-8', newline='').read()


def sub(old, new, label, count=1):
    global src
    o = old.replace('\n', NL)
    n = new.replace('\n', NL)
    found = src.count(o)
    assert found == count, '%s: found %d, expected %d' % (label, found, count)
    src = src.replace(o, n)
    print('ok %s' % label)


# ---------------------------------------------------------------- 1. dropdown --
sub(
    """  opacity:0;transform:translateY(-4px) scale(.98);pointer-events:none;
  transition:all .18s var(--spring);
}
.cs-dd.open{opacity:1;transform:translateY(0) scale(1);pointer-events:auto;}
.cs-dd-up{top:auto;bottom:calc(100% + 5px);transform:translateY(4px) scale(.98);}
.cs-dd-up.open{transform:translateY(0) scale(1);}""",
    """  opacity:0;pointer-events:none;
  /* Only opacity may animate here. A menu is moved to <body> and positioned with
     inline left/top, and a live transition makes the first getBoundingClientRect()
     report the START of the animation (the old coordinates inside the panel) - the
     self-correction in csPlaceMenu() then shoved the menu off screen. Transform is
     never animated either, so no measurement can ever be polluted by one. */
  transition:opacity .16s var(--ease);
}
.cs-dd.open{opacity:1;pointer-events:auto;animation:csFadeIn .16s var(--ease) both;}
.cs-dd-fx{transition:none!important;animation:none!important;}
.cs-dd-up{top:auto;bottom:calc(100% + 5px);}
@keyframes csFadeIn{from{opacity:0;}to{opacity:1;}}""",
    'cs-dd animates opacity only')

sub(
    """  dd.classList.add('cs-dd-pop');
  dd.style.position='fixed';dd.style.bottom='auto';dd.style.zIndex='1200';
  /* a closed menu is scaled down / nudged up by CSS; measure without that, or the
     correction below would chase the transform of the previous state. */
  dd.style.transform='none';""",
    """  dd.classList.add('cs-dd-pop');
  /* Freeze every transition while we place and measure the menu: a transition
     reports its start value to the first synchronous getBoundingClientRect(), so
     measuring mid-flight is what made the menu land in the wrong place. */
  dd.classList.add('cs-dd-fx');
  dd.style.position='fixed';dd.style.bottom='auto';dd.style.zIndex='1200';
  dd.style.transform='none';""",
    'csPlaceMenu freezes transitions')

sub(
    """  /* last-resort correction against the box that was really rendered. */
  var a=dd.getBoundingClientRect(),dx=a.left-left,dy=a.top-top;
  if(Math.abs(dx)>0.5)dd.style.left=(left-dx)+'px';
  if(Math.abs(dy)>0.5)dd.style.top=(top-dy)+'px';
  dd.style.transform='';
}""",
    """  /* Last-resort correction against the box that was really rendered. With the
     transitions frozen this reads the settled geometry; a large delta means
     something else moved us, so the inline left/top are kept in that case. */
  var a=dd.getBoundingClientRect(),dx=a.left-left,dy=a.top-top;
  if(Math.abs(dx)>0.5&&Math.abs(dx)<=24)dd.style.left=(left-dx)+'px';
  if(Math.abs(dy)>0.5&&Math.abs(dy)<=24)dd.style.top=(top-dy)+'px';
  dd.style.transform='';
  void dd.offsetWidth;                /* commit the placement ... */
  dd.classList.remove('cs-dd-fx');    /* ... before the fade-in is allowed back */
}""",
    'csPlaceMenu bounded correction')

# ------------------------------------------------- 2. provider settings block --
sub(
    ".ps-t{font-size:10px;font-weight:600;color:var(--tx3);margin-bottom:8px;letter-spacing:.5px;text-transform:uppercase;}",
    """.ps-t{font-size:10px;font-weight:600;color:var(--tx3);margin-bottom:8px;letter-spacing:.5px;text-transform:uppercase;}

/* ===== AI provider: in-use line + collapsible connection block ===== */
.prov-cur{
  display:flex;align-items:center;gap:6px;flex-wrap:wrap;
  margin-top:9px;font-size:11px;color:var(--tx3);line-height:1.5;
}
.prov-cur b{color:var(--tx2);font-weight:600;}
.prov-cur code{
  font-family:"SF Mono","Cascadia Code","Fira Code",monospace;font-size:11px;
  color:var(--ac);background:rgba(var(--ac-rg),.09);padding:1px 6px;border-radius:5px;
}
.prov-cur .prov-sep{opacity:.45;}
.prov-cur .prov-off{color:var(--tx3);font-style:italic;}
.prov-edit{
  display:none;margin-top:12px;padding:12px 12px 2px;
  border:0.5px solid var(--bd);border-radius:var(--r2);background:var(--sfi);
}
.prov-edit.open{display:block;animation:csFadeIn .18s var(--ease) both;}
.prov-edit>.pe-h{
  display:flex;align-items:center;gap:7px;margin-bottom:12px;
  font-size:10px;font-weight:600;color:var(--tx3);letter-spacing:.5px;text-transform:uppercase;
}
.prov-edit>.pe-h::before{content:'';width:3px;height:11px;border-radius:2px;background:var(--ac);opacity:.75;}
.prov-edit>.prow:last-of-type{margin-bottom:2px;}
.prov-edit .btns{margin-top:2px;margin-bottom:12px;}
.prow{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;}
.prow.one{grid-template-columns:1fr;}
@media(max-width:560px){.prow{grid-template-columns:1fr;}}""",
    'provider block CSS')

# header row: provider picker only, the name moves into the connection block
sub(
    '<div class="fr"><div class="fg"><label data-i="provLabel"></label><div class="cs cs-nosync" id="provCS">',
    '<div class="prow one"><div class="fg"><label data-i="provLabel"></label><div class="cs cs-nosync" id="provCS">',
    'provider picker row')

sub(
    '<input type="hidden" id="provider" value=""></div></div><div class="fg"><label data-i="provName"></label><input id="provName" placeholder="OpenAI"></div></div>',
    '<input type="hidden" id="provider" value=""></div></div></div>',
    'provider name out of the header row')

EDIT_ICON = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M11.6 2.4l2 2-7.4 7.4-2.6.6.6-2.6 7.4-7.4z"/></svg>')
CHECK_ICON = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" '
              'stroke-linecap="round" stroke-linejoin="round"><path d="M3.2 8.6l3.1 3.1L12.8 5"/></svg>')

sub(
    '<span data-i="provDel"></span></button></div>',
    ('<span data-i="provDel"></span></button>'
     '<button class="btn btn-s btn-sm" type="button" id="provEditBtn" onclick="editProvider()">' + EDIT_ICON +
     '<span data-i="provEdit"></span></button></div>'
     '<div class="prov-cur" id="provCur"></div>'
     '<div class="prov-edit" id="provEditBox"><div class="pe-h"><span data-i="provDetails"></span></div>'
     '<div class="prow one"><div class="fg"><label data-i="provName"></label>'
     '<input id="provName" placeholder="OpenAI"></div></div>'),
    'add/edit buttons + connection block opening')

sub(
    '<div class="fr"><div class="fg"><label>URL</label>',
    '<div class="prow"><div class="fg"><label>URL</label>',
    'URL / API key row')

sub(
    '<div class="fr"><div class="fg"><label data-i="modelName"></label>',
    '<div class="prow one"><div class="fg"><label data-i="modelName"></label>',
    'model name row')

sub(
    '<div class="fg"><label data-i="temperature"></label><input type="number" id="temperature" value="0.7" min="0" max="2" step="0.1"></div></div>',
    '</div>',
    'temperature out of the model row')

sub(
    '<div class="fr f1"><div class="fg"><label data-i="apiFormat"></label>',
    '<div class="prow one"><div class="fg"><label data-i="apiFormat"></label>',
    'api format row')

sub(
    '<input type="hidden" id="apiFormat" value="openai"></div></div></div></div>',
    ('<input type="hidden" id="apiFormat" value="openai"></div></div></div>'
     '<div class="btns"><button class="btn btn-p btn-sm" type="button" onclick="saveProviderEdit()">' + CHECK_ICON +
     '<span data-i="provSave"></span></button>'
     '<button class="btn btn-s btn-sm" type="button" onclick="cancelProviderEdit()">'
     '<span data-i="provCancel"></span></button></div></div>'
     '<div class="prow one"><div class="fg"><label data-i="temperature"></label>'
     '<input type="number" id="temperature" value="0.7" min="0" max="2" step="0.1"></div></div></div>'),
    'save/cancel buttons + temperature row after the block')

# a title that follows the language
sub('title="Show/Hide API Key"', 'data-i-title="apiKeyEye"', 'api key eye label')

sub(
    "  document.querySelectorAll('.cs-opt[data-i]').forEach(function(el){",
    """  document.querySelectorAll('[data-i-title]').forEach(function(el){el.title=t(el.getAttribute('data-i-title'));});
  document.querySelectorAll('.cs-opt[data-i]').forEach(function(el){""",
    'applyI18n handles data-i-title')

# ------------------------------------------------------------------ provider JS --
sub(
    """  csSyncAll();
}
function applyActiveProvider(){""",
    """  csSyncAll();refreshProvCur();
}
function applyActiveProvider(){""",
    'fillProviderFields refreshes the in-use line')

sub(
    """function initProviders(){loadProviders();refreshProviderDD();fillProviderFields();refreshModelDD();applyActiveProvider();}""",
    """function initProviders(){loadProviders();refreshProviderDD();fillProviderFields();refreshModelDD();applyActiveProvider();provEditNewId=null;setProvEdit(false);refreshProvCur();}""",
    'initProviders closes the edit block')

sub(
    """  providers.push(p);activeProvId=p.id;saveProviders();
  fillProviderFields();refreshProviderDD();refreshModelDD();applyActiveProvider();
  toast(t('provAdded'));""",
    """  providers.push(p);activeProvId=p.id;saveProviders();
  fillProviderFields();refreshProviderDD();refreshModelDD();applyActiveProvider();
  provEditNewId=p.id;setProvEdit(true);refreshProvCur();
  toast(t('provAdded'));""",
    'newProvider opens the connection block')

sub(
    """  persistActiveProvider();
  activeProvId=id;saveProviders();""",
    """  persistActiveProvider();
  activeProvId=id;saveProviders();
  provEditNewId=null;setProvEdit(false);""",
    'picking a provider closes the edit block')

sub(
    """  providers=providers.filter(function(p){return p.id!==activeProvId;});
  activeProvId=providers[0].id;saveProviders();
  fillProviderFields();refreshProviderDD();refreshModelDD();applyActiveProvider();
  toast(t('provDeleted'));
}""",
    """  providers=providers.filter(function(p){return p.id!==activeProvId;});
  activeProvId=providers[0].id;saveProviders();
  fillProviderFields();refreshProviderDD();refreshModelDD();applyActiveProvider();
  provEditNewId=null;setProvEdit(false);refreshProvCur();
  toast(t('provDeleted'));
}
/* ---- the connection block is hidden until you add or edit a provider ---- */
var provEditNewId=null;
function provEditOpen(){var b=$('provEditBox');return !!b&&b.classList.contains('open');}
function setProvEdit(on){
  var b=$('provEditBox');if(!b)return;
  var btn=$('provEditBtn');if(btn)btn.classList.toggle('on',!!on);
  if(on)b.classList.add('open');else b.classList.remove('open');
}
function refreshProvCur(){
  var el=$('provCur');if(!el)return;
  var p=activeProv()||{};
  el.innerHTML='<span>'+esc(t('provCur'))+'</span><b>'+esc(p.name||t('provDefault'))+'</b>'+
    '<span class="prov-sep">\\u00b7</span><span>'+esc(t('modelName'))+'</span>'+
    (p.model?'<code>'+esc(p.model)+'</code>':'<span class="prov-off">'+esc(t('provNoModel'))+'</span>');
}
function editProvider(){
  if(provEditOpen()){cancelProviderEdit();return;}   /* 修改 toggles the block */
  provEditNewId=null;
  fillProviderFields();setProvEdit(true);refreshProvCur();
  var el=$('provName');if(el){el.focus();el.select();}
}
function saveProviderEdit(){
  persistActiveProvider();applyActiveProvider();refreshProviderDD();refreshModelDD();refreshProvCur();
  provEditNewId=null;setProvEdit(false);toast(t('provSaved'));
}
function cancelProviderEdit(){
  /* cancelling a provider that was just added and left empty takes it away again */
  var p=activeProv();
  if(provEditNewId&&p&&p.id===provEditNewId&&!(p.url||p.key||p.model)&&providers.length>1){
    providers=providers.filter(function(x){return x.id!==p.id;});
    activeProvId=providers[0].id;saveProviders();
  }
  provEditNewId=null;
  fillProviderFields();refreshProviderDD();refreshModelDD();applyActiveProvider();
  setProvEdit(false);refreshProvCur();
}""",
    'provider edit helpers')

# ------------------------------------------------------------------ i18n -------
LOCALES = [
    ("provDeleted:'已刪除供應商',",
     "provDeleted:'已刪除供應商',provEdit:'修改',provSave:'儲存',provCancel:'取消',provDetails:'連線設定',"
     "provCur:'目前使用',provNoModel:'尚未設定模型',provSaved:'已儲存供應商設定',apiKeyEye:'顯示或隱藏 API Key',",
     'zh-TW'),
    ("provDeleted:'已删除供应商',",
     "provDeleted:'已删除供应商',provEdit:'修改',provSave:'保存',provCancel:'取消',provDetails:'连接设置',"
     "provCur:'当前使用',provNoModel:'未设置模型',provSaved:'已保存供应商设置',apiKeyEye:'显示或隐藏 API Key',",
     'zh-CN'),
    ("provDeleted:'Provider deleted',",
     "provDeleted:'Provider deleted',provEdit:'Edit',provSave:'Save',provCancel:'Cancel',provDetails:'Connection',"
     "provCur:'In use',provNoModel:'No model set',provSaved:'Provider settings saved',apiKeyEye:'Show or hide the API key',",
     'en'),
]
for old, new, name in LOCALES:
    sub(old, new, 'i18n %s' % name)

open(PATH, 'w', encoding='utf-8', newline='').write(src)
print('written; bytes=%d' % len(src.encode('utf-8')))
