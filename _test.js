
/* ===== i18n ===== */
var T={
'zh-TW':{
hdrTitle:'商業信件潤飾工具',inputTitle:'原始信件',outputTitle:'潤飾結果',
lblLang:'信件語言',lblTone:'潤飾風格',lblPurpose:'信件用途',lblMode:'潤飾模式',
modeFullLetter:'完整信件',modeContentOnly:'僅潤飾內容',lblMode:'潤飾模式',
modeFullLetter:'完整信件',modeContentOnly:'僅潤飾內容',
customToneLabel:'自訂風格描述',customToneHint:'描述您希望的語氣風格，AI 將據此調整信件。',
customPurpLabel:'自訂信件用途',customPurpHint:'描述此信件的用途，AI 將據此調整結構與重點。',
startPolish:'開始潤飾',polishing:'潤飾中…',clear:'清空',sample:'載入範例',
tabResult:'潤飾結果',tabDiff:'差異比較',tabSug:'修改建議',
copyResult:'複製結果',download:'下載文字檔',useAsInput:'以此再潤飾',
tipSettings:'API 連線設定',tipHistory:'歷史紀錄',
settingsTitle:'API 連線設定',quickPreset:'快速預設',apiEndpoint:'API 端點',
modelName:'模型名稱',temperature:'溫度',apiFormat:'API 格式',
fmtOpenAI:'OpenAI 相容格式',fmtAnthropic:'Anthropic 格式',fmtGemini:'Google Gemini 格式',
customPrompt:'自訂系統提示詞（可選）',save:'儲存設定',testConn:'測試連線',testing:'測試中…',
testOk:'連線成功',testFail:'連線失敗',testFill:'請先填寫 API 端點與 Key',
historyTitle:'歷史紀錄',clearAll:'清空全部',noHistory:'尚無歷史紀錄',
close:'關閉',original:'原始',polished:'潤飾',suggestions:'建議',detailTitle:'信件詳情',
sending:'正在發送請求…',noInput:'請先輸入信件內容',noApi:'請先設定 API 端點與 Key',
polishDone:'潤飾完成',noResult:'尚無結果',copied:'已複製',copyFail:'複製失敗',
downloaded:'已下載',loadedAsIn:'已放入輸入區',emptyDiff:'無差異',noSug:'無額外建議',
clearConfirm:'確定清空所有歷史紀錄？',cleared:'已清空',deleted:'已刪除',
presetOpenAI:'OpenAI',presetAnthropic:'Anthropic',presetGemini:'Gemini',presetGroq:'Groq',presetDeepSeek:'DeepSeek',presetCompat:'自架',
tonePro:'專業正式',toneFriendly:'親切友善',toneConcise:'簡潔明瞭',tonePersuasive:'具說服力',
toneApologetic:'誠懇致歉',toneGrateful:'感恩感謝',toneAssertive:'堅定果斷',toneAuthoritative:'權威專業',toneCautious:'嚴謹審慎',toneEncouraging:'鼓勵激勵',toneCustom:'自訂風格…',
purpGeneral:'一般商業溝通',purpProposal:'合作提案',purpFollowup:'跟進催辦',purpThankyou:'感謝回覆',
purpComplaint:'投訴建議',purpIntro:'自我介紹',purpNegotiation:'價格談判',purpResignation:'離職通知',purpApology:'道歉致歉',purpAnnouncement:'公告通知',purpInvitation:'邀請合作',purpFeedback:'回饋評估',purpCustom:'自訂用途…',
langZhTW:'繁體中文',langZhCN:'簡體中文',langEn:'English',langJa:'日本語',
themeLight:'淺色模式',themeDark:'暗色模式',
placeholderIn:'在此貼上您的商業信件…',placeholderOut:'潤飾結果將顯示在此處…',
placeholderCustomTone:'例如：語氣溫和但堅定，帶有同理心…',placeholderCustomPurp:'例如：邀請合作夥伴參加技術研討會…',
placeholderPrompt:'例如：你是一位資深商務溝通顧問…',sugPlaceholder:'執行潤飾後，此處將顯示差異比較。',sugPlaceholder2:'執行潤飾後，此處將顯示修改建議。',guideW1Title:'歡迎使用商業信件潤飾工具',guideW1Desc:'本工具可協助您快速潤飾商業信件，提升專業度與溝通品質。',guideW1Sub:'支援 OpenAI、Anthropic、Gemini 等多家 API，無需安裝即可使用。',guideW2Title:'設定 API 連線',guideW2Desc:'使用前需設定 AI API 連線。點擊右下角齒輪按鈕可隨時修改。',guideW2Step1:'<b>選擇服務商</b> — 點擊「快速預設」選取 OpenAI、Anthropic、Gemini 等',guideW2Step2:'<b>填入 API Key</b> — 從服務商官網取得您的專屬金鑰',guideW2Step3:'<b>測試連線</b> — 點擊「測試連線」確認設定正確',guideW3Title:'開始使用',guideW3Desc:'設定完成後，即可開始潤飾您的信件。',guideW3Step1:'<b>選擇設定</b> — 選擇信件語言、潤飾風格、用途與模式',guideW3Step2:'<b>貼上信件</b> — 將原始信件內容貼入下方文字框',guideW3Step3:'<b>點擊潤飾</b> — 按下「開始潤飾」按鈕',guideW3Step4:'<b>查看結果</b> — 潤飾結果將顯示在右側，可複製或下載',guideSkip:'跳過引導',guidePrev:'上一步',guideNext:'下一步',guideDone:'開始使用',guideReopen:'使用引導',checkUpdate:'檢查更新',checking:'檢查中…',newVersion:'有新版本可用',upToDate:'已是最新版本',updateFail:'檢查更新失敗',clickToDownload:'按確定下載'
},
'zh-CN':{
hdrTitle:'商业信件润饰工具',inputTitle:'原始信件',outputTitle:'润饰结果',
lblLang:'信件语言',lblTone:'润饰风格',lblPurpose:'信件用途',
customToneLabel:'自订风格描述',customToneHint:'描述您希望的语气风格，AI 将据此调整信件。',
customPurpLabel:'自订信件用途',customPurpHint:'描述此信件的用途，AI 将据此调整结构与重点。',
startPolish:'开始润饰',polishing:'润饰中…',clear:'清空',sample:'载入范例',
tabResult:'润饰结果',tabDiff:'差异比较',tabSug:'修改建议',
copyResult:'复制结果',download:'下载文字档',useAsInput:'以此再润饰',
tipSettings:'API 连线设定',tipHistory:'历史纪录',
settingsTitle:'API 连线设定',quickPreset:'快速预设',apiEndpoint:'API 端点',
modelName:'模型名称',temperature:'温度',apiFormat:'API 格式',
fmtOpenAI:'OpenAI 兼容格式',fmtAnthropic:'Anthropic 格式',fmtGemini:'Google Gemini 格式',
customPrompt:'自订系统提示词（可选）',save:'储存设定',testConn:'测试连线',testing:'测试中…',
testOk:'连线成功',testFail:'连线失败',testFill:'请先填写 API 端点与 Key',
historyTitle:'历史纪录',clearAll:'清空全部',noHistory:'尚无历史纪录',
close:'关闭',original:'原始',polished:'润饰',suggestions:'建议',detailTitle:'信件详情',
sending:'正在发送请求…',noInput:'请先输入信件内容',noApi:'请先设定 API 端点与 Key',
polishDone:'润饰完成',noResult:'尚无结果',copied:'已复制',copyFail:'复制失败',
downloaded:'已下载',loadedAsIn:'已放入输入区',emptyDiff:'无差异',noSug:'无额外建议',
clearConfirm:'确定清空所有历史纪录？',cleared:'已清空',deleted:'已删除',
presetOpenAI:'OpenAI',presetAnthropic:'Anthropic',presetGemini:'Gemini',presetGroq:'Groq',presetDeepSeek:'DeepSeek',presetCompat:'自架',
tonePro:'专业正式',toneFriendly:'亲切友善',toneConcise:'简洁明了',tonePersuasive:'具说服力',
toneApologetic:'诚恳致歉',toneGrateful:'感恩感谢',toneAssertive:'坚定果断',toneCustom:'自订风格…',
purpGeneral:'一般商业沟通',purpProposal:'合作提案',purpFollowup:'跟进催办',purpThankyou:'感谢回复',
purpComplaint:'投诉建议',purpIntro:'自我介绍',purpNegotiation:'价格谈判',purpResignation:'离职通知',purpCustom:'自订用途…',
langZhTW:'繁體中文',langZhCN:'简体中文',langEn:'English',langJa:'日本語',
themeLight:'浅色模式',themeDark:'暗色模式',
placeholderIn:'在此贴上您的商业信件…',placeholderOut:'润饰结果将显示在此处…',
placeholderCustomTone:'例如：语气温和但坚定，带有同理心…',placeholderCustomPurp:'例如：邀请合作伙伴参加技术研讨会…',
placeholderPrompt:'例如：你是一位资深商务沟通顾问…',sugPlaceholder:'执行润饰后，此处将显示差异比较。',sugPlaceholder2:'执行润饰后，此处将显示修改建议。',guideW1Title:'欢迎使用商业信件润饰工具',guideW1Desc:'本工具可协助您快速润饰商业信件，提升专业度与沟通质量。',guideW1Sub:'支挄 OpenAI、Anthropic、Gemini 等多家 API，无需安裝即可使用。',guideW2Title:'设置 API 连接',guideW2Desc:'使用前需设置 AI API 连接。点击右下角齿轮按钮可随时修改。',guideW2Step1:'<b>选择服务商</b> — 点击「快速预设」选取 OpenAI、Anthropic、Gemini 等',guideW2Step2:'<b>填入 API Key</b> — 从服务商官网获取您的专属金钥',guideW2Step3:'<b>测试连接</b> — 点击「测试连接」确认设置正确',guideW3Title:'开始使用',guideW3Desc:'设置完成后，即可开始润饰您的信件。',guideW3Step1:'<b>选择设置</b> — 选择信件语言、润饰风格、用途与模式',guideW3Step2:'<b>贴上信件</b> — 将原始信件内容贴入下方文本框',guideW3Step3:'<b>点击润饰</b> — 按下「开始润饰」按钮',guideW3Step4:'<b>查看结果</b> — 润饰结果将显示在右侧，可复制或下载',guideSkip:'跳过引导',guidePrev:'上一步',guideNext:'下一步',guideDone:'开始使用',guideReopen:'使用引导',checkUpdate:'检查更新',checking:'检查中…',newVersion:'有新版本可用',upToDate:'已是最新版本',updateFail:'检查更新失败',clickToDownload:'按确定下载'
},
'en':{
hdrTitle:'Letter Polisher',inputTitle:'Original Letter',outputTitle:'Polished Result',
lblLang:'Language',lblTone:'Polish Style',lblPurpose:'Letter Purpose',lblMode:'Polish Mode',
modeFullLetter:'Full Letter',modeContentOnly:'Content Only',
customToneLabel:'Custom Style Description',customToneHint:'Describe the desired tone — AI will adjust accordingly.',
customPurpLabel:'Custom Purpose',customPurpHint:'Describe the purpose — AI will tailor structure and focus.',
startPolish:'Polish',polishing:'Polishing…',clear:'Clear',sample:'Sample',
tabResult:'Result',tabDiff:'Diff',tabSug:'Suggestions',
copyResult:'Copy',download:'Download',useAsInput:'Use as Input',
tipSettings:'API Settings',tipHistory:'History',
settingsTitle:'API Settings',quickPreset:'Quick Presets',apiEndpoint:'API Endpoint',
modelName:'Model',temperature:'Temperature',apiFormat:'API Format',
fmtOpenAI:'OpenAI Compatible',fmtAnthropic:'Anthropic Format',fmtGemini:'Google Gemini',
customPrompt:'Custom System Prompt (optional)',save:'Save',testConn:'Test Connection',testing:'Testing…',
testOk:'Connected',testFail:'Failed',testFill:'Please enter API endpoint and key',
historyTitle:'History',clearAll:'Clear All',noHistory:'No history yet',
close:'Close',original:'Original',polished:'Polished',suggestions:'Suggestions',detailTitle:'Letter Details',
sending:'Sending request…',noInput:'Please enter a letter',noApi:'Please configure API endpoint and key',
polishDone:'Complete',noResult:'No result yet',copied:'Copied',copyFail:'Copy failed',
downloaded:'Downloaded',loadedAsIn:'Loaded into input',emptyDiff:'No differences',noSug:'No suggestions',
clearConfirm:'Clear all history?',cleared:'Cleared',deleted:'Deleted',
presetOpenAI:'OpenAI',presetAnthropic:'Anthropic',presetGemini:'Gemini',presetGroq:'Groq',presetDeepSeek:'DeepSeek',presetCompat:'Self-hosted',
tonePro:'Professional',toneFriendly:'Friendly',toneConcise:'Concise',tonePersuasive:'Persuasive',
toneApologetic:'Apologetic',toneGrateful:'Grateful',toneAssertive:'Assertive',toneAuthoritative:'Authoritative',toneCautious:'Cautious',toneEncouraging:'Encouraging',toneCustom:'Custom…',
purpGeneral:'General',purpProposal:'Proposal',purpFollowup:'Follow-up',purpThankyou:'Thank You',
purpComplaint:'Complaint',purpIntro:'Introduction',purpNegotiation:'Negotiation',purpResignation:'Resignation',purpApology:'Apology',purpAnnouncement:'Announcement',purpInvitation:'Invitation',purpFeedback:'Feedback',purpCustom:'Custom…',
langZhTW:'繁體中文',langZhCN:'简体中文',langEn:'English',langJa:'日本語',
themeLight:'Light Mode',themeDark:'Dark Mode',
placeholderIn:'Paste your business letter here…',placeholderOut:'Polished result will appear here…',
placeholderCustomTone:'e.g. Warm but firm, with empathy…',placeholderCustomPurp:'e.g. Invite partner to annual tech conference…',
placeholderPrompt:'e.g. You are a senior business communication consultant…',sugPlaceholder:'Differences will appear here after polishing.',guideW1Title:'Welcome to Business Letter Polisher',guideW1Desc:'This tool helps you quickly polish business letters to improve professionalism and communication quality.',guideW1Sub:'Supports OpenAI, Anthropic, Gemini, and more. No installation required.',guideW2Title:'Set Up API Connection',guideW2Desc:'You need to configure an AI API connection before use. Click the gear button to modify anytime.',guideW2Step1:'<b>Choose Provider</b> — Click Quick Preset to select OpenAI, Anthropic, Gemini, etc.',guideW2Step2:'<b>Enter API Key</b> — Get your secret key from the provider\'s website',guideW2Step3:'<b>Test Connection</b> — Click Test Connection to verify settings',guideW3Title:'Start Using',guideW3Desc:'Once configured, you can start polishing your letters.',guideW3Step1:'<b>Select Settings</b> — Choose language, tone, purpose, and mode',guideW3Step2:'<b>Paste Letter</b> — Paste your original letter content into the text box',guideW3Step3:'<b>Click Polish</b> — Press the Start Polish button',guideW3Step4:'<b>View Results</b> — Results appear on the right, ready to copy or download',guideSkip:'Skip',guidePrev:'Back',guideNext:'Next',guideDone:'Get Started',guideReopen:'User Guide',checkUpdate:'Check for Update',checking:'Checking...',newVersion:'New version available',upToDate:'Up to date',updateFail:'Update check failed',clickToDownload:'Click OK to download',sugPlaceholder2:'Suggestions will appear here after polishing.'
}
};

/* ===== Config ===== */
var TL_KEY={professional:'tonePro',friendly:'toneFriendly',concise:'toneConcise',persuasive:'tonePersuasive',apologetic:'toneApologetic',grateful:'toneGrateful',assertive:'toneAssertive',authoritative:'toneAuthoritative',cautious:'toneCautious',encouraging:'toneEncouraging',custom:'toneCustom'};
var PL_KEY={general:'purpGeneral',proposal:'purpProposal',followup:'purpFollowup',thankyou:'purpThankyou',complaint:'purpComplaint',introduction:'purpIntro',negotiation:'purpNegotiation',resignation:'purpResignation',apology:'purpApology',announcement:'purpAnnouncement',invitation:'purpInvitation',feedback:'purpFeedback','custom-purpose':'purpCustom'};
var LANG_KEY={'zh-TW':'langZhTW','zh-CN':'langZhCN','en':'langEn','ja':'langJa'};
var locale='en',DF={apiUrl:'',apiKey:'',modelName:'gpt-4o',temperature:0.7,apiFormat:'openai',customSystemPrompt:'',customTone:'',customPurpose:''},cfg=Object.assign({},DF),lastRes=null,H=[],tt=null;
var PR={openai:{u:'https://api.openai.com/v1/chat/completions',m:'gpt-4o',f:'openai',k:'presetOpenAI'},anthropic:{u:'https://api.anthropic.com/v1/messages',m:'claude-sonnet-4-20250514',f:'anthropic',k:'presetAnthropic'},gemini:{u:'https://generativelanguage.googleapis.com/v1beta/models/GEMINI_MODEL:generateContent',m:'gemini-2.0-flash',f:'gemini',k:'presetGemini'},groq:{u:'https://api.groq.com/openai/v1/chat/completions',m:'llama-3.3-70b-versatile',f:'openai',k:'presetGroq'},deepseek:{u:'https://api.deepseek.com/chat/completions',m:'deepseek-chat',f:'openai',k:'presetDeepSeek'},'openai-compat':{u:'http://localhost:11434/v1/chat/completions',m:'llama3',f:'openai',k:'presetCompat'}};

function t(k){return(T[locale]&&T[locale][k])||T.en[k]||k;}
function detectLang(){var l=(navigator.language||navigator.userLanguage||'').toLowerCase();if(l==='zh-tw'||l==='zh-hant'||l==='zh-mo')return'zh-TW';if(l.indexOf('zh')===0)return'zh-CN';return'en';}

/* ===== Custom Select ===== */
function csToggle(btn){
  var dd=btn.nextElementSibling,wasOpen=dd.classList.contains('open');
  csCloseAll();
  if(!wasOpen){
    if(btn.closest('.panel-body')){
      var r=btn.getBoundingClientRect();
      dd.style.position='fixed';dd.style.left=r.left+'px';dd.style.top=(r.bottom+5)+'px';dd.style.width=r.width+'px';dd.style.bottom='auto';
    }
    dd.classList.add('open');btn.classList.add('open');
  }
}
function csPick(opt){
  var cs=opt.closest('.cs'),h=cs.querySelector('input[type="hidden"]'),btn=cs.querySelector('.cs-btn');
  cs.querySelectorAll('.cs-opt').forEach(function(o){o.classList.remove('sel');});
  opt.classList.add('sel');h.value=opt.dataset.val;
  var lbl=t(opt.getAttribute('data-i'))||opt.textContent;
  btn.querySelector('.cs-txt').textContent=lbl;
  cs.querySelector('.cs-dd').classList.remove('open');btn.classList.remove('open');
  var dd=cs.querySelector('.cs-dd');dd.style.position='';dd.style.left='';dd.style.top='';dd.style.width='';dd.style.bottom='';
  var id=h.id;if(id==='tone')onToneCh();if(id==='purpose')onPurpCh();
}
function csLangPick(opt){csPick(opt);locale=opt.dataset.val;localStorage.setItem('bp_lang',locale);applyI18n();}
function csCloseAll(){
  document.querySelectorAll('.cs-dd.open').forEach(function(d){d.classList.remove('open');d.style.position='';d.style.left='';d.style.top='';d.style.width='';d.style.bottom='';});
  document.querySelectorAll('.cs-btn.open').forEach(function(b){b.classList.remove('open');});
}
function csSyncAll(){
  document.querySelectorAll('.cs').forEach(function(cs){
    var h=cs.querySelector('input[type="hidden"]');if(!h)return;
    var val=h.value,txt=cs.querySelector('.cs-txt'),found=false;
    cs.querySelectorAll('.cs-opt').forEach(function(o){
      o.classList.remove('sel');
      if(o.dataset.val===val){o.classList.add('sel');txt.textContent=t(o.getAttribute('data-i'))||o.textContent;found=true;}
    });
    if(!found){var first=cs.querySelector('.cs-opt');if(first){first.classList.add('sel');txt.textContent=t(first.getAttribute('data-i'))||first.textContent;h.value=first.dataset.val;}}
  });
}
document.addEventListener('click',function(e){if(!e.target.closest('.cs'))csCloseAll();});

/* ===== i18n ===== */
function applyI18n(){
  document.querySelectorAll('[data-i]').forEach(function(el){if(!el.classList.contains('cs-opt'))el.textContent=t(el.getAttribute('data-i'));});
  document.querySelectorAll('.cs-opt[data-i]').forEach(function(el){
    var chk=el.querySelector('.cs-chk'),lbl=t(el.getAttribute('data-i'))||el.textContent;
    el.textContent='';el.appendChild(document.createTextNode(lbl));
    if(chk)el.appendChild(chk);
  });
  csSyncAll();
  document.getElementById('themeBtn').title=t(document.documentElement.getAttribute('data-theme')==='dark'?'themeLight':'themeDark');
  $('letterIn').placeholder=t('placeholderIn');$('letterOut').placeholder=t('placeholderOut');
  $('diffV').innerHTML='<span style="color:var(--tx3)">'+esc(t('sugPlaceholder'))+'</span>';
  $('sugV').innerHTML='<span style="color:var(--tx3)">'+esc(t('sugPlaceholder2'))+'</span>';
  $('customToneVal').placeholder=t('placeholderCustomTone');
  $('customPurpVal').placeholder=t('placeholderCustomPurp');
  $('sysPrompt').placeholder=t('placeholderPrompt');
  renderPresetChips();renderH();
  if(typeof applyGuideHTML==='function')applyGuideHTML();
}

/* ===== Theme ===== */
function toggleTheme(){
  var h=document.documentElement,cur=h.getAttribute('data-theme'),n=cur==='dark'?'light':'dark';
  h.setAttribute('data-theme',n);localStorage.setItem('bp_theme',n);
  document.getElementById('themeBtn').title=t(n==='dark'?'themeLight':'themeDark');updateThemeIcon();
}
function loadTheme(){var s=localStorage.getItem('bp_theme');if(s)document.documentElement.setAttribute('data-theme',s);updateThemeIcon();}
function updateThemeIcon(){
  var d=document.documentElement.getAttribute('data-theme'),ic=document.getElementById('themeIc');
  ic.innerHTML=d==='dark'?'<circle cx="10" cy="10" r="4"/><path d="M10 2v2M10 16v2M2 10h2M16 10h2M4.93 4.93l1.41 1.41M13.66 13.66l1.41 1.41M4.93 15.07l1.41-1.41M13.66 6.34l1.41-1.41"/>':'<path d="M17 10.5A7.5 7.5 0 019.5 3 7 7 0 1017 10.5z"/>';
}

/* ===== Presets ===== */
function renderPresetChips(){var el=$('presetChips'),keys=['openai','anthropic','gemini','groq','deepseek','openai-compat'];el.innerHTML=keys.map(function(k){return'<span class="chip" onclick="applyPreset(\''+k+'\',this)">'+t(PR[k].k)+'</span>';}).join('');}

/* ===== Settings ===== */
function loadCfg(){var s=localStorage.getItem('bp_cfg');if(s)try{cfg=Object.assign({},cfg,JSON.parse(s));}catch(e){}}
function saveCfg(){cfg.apiUrl=v('apiUrl');cfg.apiKey=v('apiKey');cfg.modelName=v('modelName');cfg.temperature=parseFloat(v('temperature'))||0.7;cfg.apiFormat=v('apiFormat');cfg.customSystemPrompt=v('sysPrompt');cfg.customTone=v('customToneVal');cfg.customPurpose=v('customPurpVal');localStorage.setItem('bp_cfg',JSON.stringify(cfg));toast(t('save')+' ✓');}
function autoSave(){cfg.apiUrl=v('apiUrl');cfg.apiKey=v('apiKey');cfg.modelName=v('modelName');cfg.temperature=parseFloat(v('temperature'))||0.7;cfg.apiFormat=v('apiFormat');cfg.customSystemPrompt=v('sysPrompt');cfg.customTone=v('customToneVal');cfg.customPurpose=v('customPurpVal');localStorage.setItem('bp_cfg',JSON.stringify(cfg));}
function fillF(){sV('apiUrl',cfg.apiUrl);sV('apiKey',cfg.apiKey);sV('modelName',cfg.modelName);sV('temperature',cfg.temperature);sV('apiFormat',cfg.apiFormat);sV('sysPrompt',cfg.customSystemPrompt);sV('customToneVal',cfg.customTone||'');sV('customPurpVal',cfg.customPurpose||'');csSyncAll();}
function v(id){return document.getElementById(id).value.trim();}
function sV(id,val){document.getElementById(id).value=val;}
function $(id){return document.getElementById(id);}
function applyPreset(k,el){var p=PR[k];sV('apiUrl',p.u);sV('modelName',p.m);sV('apiFormat',p.f);csSyncAll();document.querySelectorAll('.chip').forEach(function(c){c.classList.remove('on');});if(el)el.classList.add('on');}
function onToneCh(){v('tone')==='custom'?$('custTone').classList.add('show'):$('custTone').classList.remove('show');}
function onPurpCh(){v('purpose')==='custom-purpose'?$('custPurp').classList.add('show'):$('custPurp').classList.remove('show');}
function updCnt(){$('charCnt').textContent=$('letterIn').value.length;}

/* ===== Panels ===== */
function toggleSP(){var o=$('sOv'),b=$('fabS');o.classList.contains('open')?(o.classList.remove('open'),b.classList.remove('on')):(o.classList.add('open'),b.classList.add('on'));}
function toggleHP(){var o=$('hOv'),b=$('fabH');o.classList.contains('open')?(o.classList.remove('open'),b.classList.remove('on')):(o.classList.add('open'),b.classList.add('on'));}

/* ===== Tabs ===== */
function swTab(n,el){document.querySelectorAll('.tab').forEach(function(x){x.classList.remove('on');});document.querySelectorAll('.tp').forEach(function(x){x.classList.remove('on');});el.classList.add('on');$('tp-'+n).classList.add('on');}
function resetTabs(){var tabs=document.querySelectorAll('.tab'),ps=document.querySelectorAll('.tp');tabs.forEach(function(x){x.classList.remove('on');});ps.forEach(function(x){x.classList.remove('on');});if(tabs[0])tabs[0].classList.add('on');if(ps[0])ps[0].classList.add('on');}

/* ===== Polish ===== */
async function go(){
  var input=$('letterIn').value.trim();
  if(!input){showSts(t('noInput'),'err');return;}
  autoSave();
  if(!cfg.apiUrl||!cfg.apiKey){showSts(t('noApi'),'err');return;}
  var btn=$('goBtn'),txt=$('goTxt');
  btn.disabled=true;txt.innerHTML='<span class="sp"></span> '+t('polishing');
  showSts(t('sending'),'info');
  var lang=v('letterLang'),tone=v('tone'),purp=v('purpose');
  var tK=TL_KEY[tone]||'tonePro';if(tone==='custom'){var ct=v('customToneVal');tK=ct?'custom: '+ct:'Custom';}
  var pK=PL_KEY[purp]||'purpGeneral';if(purp==='custom-purpose'){var cp=v('customPurpVal');pK=cp?'custom: '+cp:'Custom';}
  var lL=LANG_KEY[lang]||lang;
  var tI=tone==='custom'?(v('customToneVal')||'Adjust tone as appropriate.'):'Style: '+t(tK);
  var pI=purp==='custom-purpose'?(v('customPurpVal')||'Determine appropriate purpose.'):'Purpose: '+t(pK);
  var pm=v('polishMode');
  var modeRule=pm==='content'?'Only polish and refine the provided text as-is. Do NOT add greetings, closings, signatures, subject lines, or any content not in the original. Do NOT restructure into a letter format. Return ONLY the polished version of the provided text.':'Output a complete polished letter including appropriate greeting and closing.';
  var sysPrompt=cfg.customSystemPrompt||('You are a senior business communication consultant. Polish the letter professionally.\nRules: preserve intent, improve clarity, maintain business etiquette, fix grammar, '+modeRule+' Match original language.\n'+tI+'\n'+pI+'\nLanguage: '+lL+'\n\nAppend "--- Suggestions ---" section (2-5 points) at the end.');

  var st=Date.now();
  try{var r;if(cfg.apiFormat==='anthropic')r=await callAnthropic(input,sysPrompt);else if(cfg.apiFormat==='gemini')r=await callGemini(input,sysPrompt);else r=await callOpenAI(input,sysPrompt);
  var el2=((Date.now()-st)/1000).toFixed(1);var pt=r.split('--- Suggestions ---');var polished=pt[0].trim();var sug=pt.length>1?pt[1].trim():'';
  $('letterOut').value=polished;$('diffV').innerHTML=diffHTML(input,polished);
  $('sugV').innerHTML=sug?sug.replace(/\n/g,'<br>'):'<span style="color:var(--tx3)">'+esc(t('noSug'))+'</span>';
  lastRes={original:input,polished:polished,suggestions:sug};
  var pb=$('pfB');pb.textContent=el2+'s';pb.className='pf show '+(el2<3?'fast':el2<10?'med':'slow');
  showSts(t('polishDone')+' ('+el2+'s)','ok');addH(input,polished,sug,t(tK),t(pK));
  }catch(err){showSts('Error: '+err.message,'err');}
  finally{btn.disabled=false;txt.textContent=t('startPolish');}
}
async function callOpenAI(t2,sp){var r=await fetch(cfg.apiUrl,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+cfg.apiKey},body:JSON.stringify({model:cfg.modelName,temperature:cfg.temperature,messages:[{role:'system',content:sp},{role:'user',content:t2}]})});if(!r.ok){var b=await r.text();throw new Error(r.status+': '+b.substring(0,200));}var d=await r.json();if(d.choices&&d.choices[0]&&d.choices[0].message)return d.choices[0].message.content||'';throw new Error('Unexpected response');}
async function callAnthropic(t2,sp){var r=await fetch(cfg.apiUrl,{method:'POST',headers:{'Content-Type':'application/json','x-api-key':cfg.apiKey,'anthropic-version':'2023-06-01'},body:JSON.stringify({model:cfg.modelName,max_tokens:4096,temperature:cfg.temperature,system:sp,messages:[{role:'user',content:t2}]})});if(!r.ok){var b=await r.text();throw new Error(r.status+': '+b.substring(0,200));}var d=await r.json();if(d.content&&d.content[0])return d.content[0].text||'';throw new Error('Unexpected response');}
async function callGemini(t2,sp){var url=cfg.apiUrl.replace('GEMINI_MODEL',cfg.modelName);var r=await fetch(url+'?key='+cfg.apiKey,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({contents:[{parts:[{text:sp+'\n\n---\n\n'+t2}]}],generationConfig:{temperature:cfg.temperature}})});if(!r.ok){var b=await r.text();throw new Error(r.status+': '+b.substring(0,200));}var d=await r.json();if(d.candidates&&d.candidates[0]&&d.candidates[0].content&&d.candidates[0].content.parts)return d.candidates[0].content.parts[0].text||'';throw new Error('Unexpected response');}
function showSts(m,tp){var el=$('sts');el.textContent=m;el.className='sts show '+tp;}

/* ===== Test ===== */
async function testConn(){
  autoSave();if(!cfg.apiUrl||!cfg.apiKey){showTR(t('testFill'),'err');return;}
  var btn=$('testBtn'),ot=btn.textContent;btn.disabled=true;btn.innerHTML='<span class="sp" style="border-color:rgba(255,255,255,.15);border-top-color:var(--ac)"></span> '+t('testing');
  showTR(t('testing'),'info');
  try{var r;if(cfg.apiFormat==='anthropic')r=await callAnthropic('Hello.','Reply OK');else if(cfg.apiFormat==='gemini')r=await callGemini('Hello.','Reply OK');else r=await callOpenAI('Hello.','Reply OK');showTR(t('testOk')+': '+r.substring(0,60),'ok');}
  catch(e){showTR(t('testFail')+': '+e.message,'err');}
  finally{btn.disabled=false;btn.textContent=ot;}
}
function showTR(m,tp){var el=$('testR');el.innerHTML=m;el.style.display='block';el.style.background=tp==='ok'?'rgba(48,209,88,.08)':tp==='info'?'var(--acg)':'rgba(255,69,58,.08)';el.style.color=tp==='ok'?'var(--ok)':tp==='info'?'var(--ac)':'var(--er)';el.style.border='0.5px solid '+(tp==='ok'?'rgba(48,209,88,.12)':tp==='info'?'rgba(var(--ac-rg),.12)':'rgba(255,69,58,.12)');el.style.borderRadius='var(--r3)';el.style.padding='8px 10px';}

/* ===== Diff ===== */
function diffHTML(a,b){var al=a.split('\n'),bl=b.split('\n'),h='',mx=Math.max(al.length,bl.length);for(var i=0;i<mx;i++){var o=al[i]||'',n=bl[i]||'';if(o===n)h+='<div style="padding:1px 6px;color:var(--tx3)">'+esc(o)+'</div>';else{if(o)h+='<div class="df-o">- '+esc(o)+'</div>';if(n)h+='<div class="df-n">+ '+esc(n)+'</div>';}}return h||'<span style="color:var(--tx3)">'+esc(t('emptyDiff'))+'</span>';}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}

/* ===== History ===== */
function loadH(){var s=localStorage.getItem('bp_h');if(s)try{H=JSON.parse(s);}catch(e){}renderH();}
function addH(o,p,s,tone,purp){H.unshift({id:Date.now(),date:new Date().toLocaleString(),original:o,polished:p,suggestions:s,tone:tone,purpose:purp});if(H.length>50)H=H.slice(0,50);localStorage.setItem('bp_h',JSON.stringify(H));renderH();}
function renderH(){var el=$('hList'),ct=$('hCnt'),bd=$('hBdg');ct.textContent=H.length?'('+H.length+')':'';bd.textContent=H.length;H.length?bd.classList.remove('off'):bd.classList.add('off');if(!H.length){el.innerHTML='<div style="text-align:center;color:var(--tx3);padding:20px;font-size:13px;">'+t('noHistory')+'</div>';return;}el.innerHTML=H.map(function(h){return '<div class="hi" onclick="showDetail('+h.id+')"><div class="hm"><span>'+esc(h.date)+'</span><span style="cursor:pointer;color:var(--er);opacity:.5" onclick="event.stopPropagation();delH('+h.id+')">✕</span></div><div class="hp">'+esc(h.original.substring(0,80))+'…</div><div class="ht"><span class="tg">'+esc(h.tone)+'</span><span class="tg">'+esc(h.purpose)+'</span></div></div>';}).join('');}
function showDetail(id){var f=null;for(var i=0;i<H.length;i++)if(H[i].id===id){f=H[i];break;}if(!f)return;$('dCont').innerHTML='<strong>【'+t('original')+'】</strong>\n'+esc(f.original)+'\n\n<strong>【'+t('polished')+'】</strong>\n'+esc(f.polished)+'\n\n<strong>【'+t('suggestions')+'】</strong>\n'+esc(f.suggestions||'—');$('dMo').classList.add('show');window._dp=f.polished;}
function delH(id){H=H.filter(function(x){return x.id!==id;});localStorage.setItem('bp_h',JSON.stringify(H));renderH();toast(t('deleted'));}
function clrH(){if(!confirm(t('clearConfirm')))return;H=[];localStorage.removeItem('bp_h');renderH();toast(t('cleared'));}

/* ===== Modal ===== */
function closeMo(){$('dMo').classList.remove('show');}
function cpDetail(){cpTxt(window._dp||'');}

/* ===== Clipboard ===== */
function copyOut(){var tx=$('letterOut').value;if(!tx){toast(t('noResult'));return;}cpTxt(tx);}
function cpTxt(tx){if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(tx).then(function(){toast(t('copied'));}).catch(function(){fbCp(tx);});}else fbCp(tx);}
function fbCp(tx){var a=document.createElement('textarea');a.value=tx;a.style.cssText='position:fixed;left:-9999px';document.body.appendChild(a);a.select();try{document.execCommand('copy');toast(t('copied'));}catch(e){toast(t('copyFail'));}document.body.removeChild(a);}
function dlResult(){var tx=$('letterOut').value;if(!tx){toast(t('noResult'));return;}var b=new Blob(['\uFEFF'+tx],{type:'text/plain;charset=utf-8'});var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='polished_'+new Date().toISOString().slice(0,10)+'.txt';a.click();URL.revokeObjectURL(a.href);toast(t('downloaded'));}

/* ===== Actions ===== */
function useAsIn(){var tx=$('letterOut').value;if(!tx)return;$('letterIn').value=tx;updCnt();window.scrollTo({top:0,behavior:'smooth'});toast(t('loadedAsIn'));}
function clearAll(){$('letterIn').value='';$('letterOut').value='';updCnt();$('diffV').innerHTML='<span style="color:var(--tx3)">'+esc(t('sugPlaceholder'))+'</span>';$('sugV').innerHTML='<span style="color:var(--tx3)">'+esc(t('sugPlaceholder2'))+'</span>';$('sts').classList.remove('show');$('pfB').classList.remove('show');resetTabs();}
function loadSample(){$('letterIn').value='王經理您好：\n\n感謝您上週撥冗與我們團隊進行會議，討論關於貴公司數位轉型專案的合作可能性。\n\n經過內部討論後，我們對於這個合作方向感到相當有興趣。我們認為我們的技術能力與貴公司的產業經驗可以產生很好的協同效應。\n\n關於合作方式，我們有以下初步想法：\n1. 第一階段：需求訪談與系統規劃（預計2週）\n2. 第二階段：原型開發與測試（預計6週）\n3. 第三階段：正式上線與後續維護\n\n預算方面，我們會在本週五前提供一份詳細的報價單給您參考。\n\n如果有任何問題，歡迎隨時與我聯繫。\n\n順頌商祺\n李小明\n業務經理\nXX 科技有限公司';updCnt();}

/* ===== Onboarding Guide ===== */
var guideStep=1,guideTotal=3;
function openGuide(){guideStep=1;updGuideUI();$('guideOv').classList.add('open');}
function closeGuide(){$('guideOv').classList.remove('open');localStorage.setItem('bp_guide_done','1');}
function skipGuide(){closeGuide();}
function guideNav(d){
  var ns=guideStep+d;
  if(ns>guideTotal){closeGuide();return;}
  if(ns<1)return;
  guideStep=ns;updGuideUI();
}
function updGuideUI(){
  document.querySelectorAll('.guide-step').forEach(function(el){el.classList.toggle('on',parseInt(el.getAttribute('data-guide'))===guideStep);});
  document.querySelectorAll('.guide-dot').forEach(function(el){el.classList.toggle('on',parseInt(el.getAttribute('data-gdot'))===guideStep);});
  $('guidePrev').style.display=guideStep===1?'none':'';
  var isLast=guideStep===guideTotal;
  document.getElementById('guideNextTxt').textContent=isLast?t('guideDone'):t('guideNext');
}

/* ===== Toast ===== */
function toast(m){var el=$('toast');el.textContent=m;el.classList.add('show');if(tt)clearTimeout(tt);tt=setTimeout(function(){el.classList.remove('show');},2200);}

/* ===== Keyboard ===== */
document.addEventListener('keydown',function(e){if(e.key==='Escape'){if($('guideOv').classList.contains('open')){closeGuide();return;}closeMo();csCloseAll();if($('sOv').classList.contains('open'))toggleSP();if($('hOv').classList.contains('open'))toggleHP();}if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){var a=document.activeElement;if(a&&a.id==='letterIn'){e.preventDefault();go();}}});

/* ===== Online Update ===== */
var APP_VERSION='2026.08.18';
var UPDATE_URL='https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/version.json';
function checkForUpdate(){
  var btn=$('updBtn'),txt=$('updTxt');
  if(btn){btn.disabled=true;if(txt)txt.textContent=t('checking');}
  fetch(UPDATE_URL+'?_t='+Date.now()).then(function(r){return r.json();}).then(function(d){
    if(btn){btn.disabled=false;if(txt)txt.textContent=t('checkUpdate');}
    if(!d.version)return;
    var remote=d.version.split('.').map(Number),local=APP_VERSION.split('.').map(Number);
    var newer=false;
    for(var i=0;i<Math.max(remote.length,local.length);i++){
      var r=remote[i]||0,l=local[i]||0;
      if(r>l){newer=true;break;}if(r<l)break;
    }
    if(newer){
      var notes='';
      if(d.release_notes){
        notes=d.release_notes[locale]||d.release_notes.en||'';
      }
      var msg=t('newVersion')+': '+d.version;
      if(notes)msg+='\n'+notes;
      if(d.download_url){
        msg+='\n\n'+t('clickToDownload');
        if(confirm(msg)){
          window.open(d.release_notes_url||d.download_url,'_blank');
        }
      }else{
        alert(msg);
      }
    }else{
      toast(t('upToDate'));
    }
  }).catch(function(e){
    if(btn){btn.disabled=false;if(txt)txt.textContent=t('checkUpdate');}
    toast(t('updateFail'));
  });
}
/* ===== Init ===== */
function applyGuideHTML(){
  var keys=['guideW2Step1','guideW2Step2','guideW2Step3','guideW3Step1','guideW3Step2','guideW3Step3','guideW3Step4'];
  var lis=document.querySelectorAll('.guide-list li[data-i]');
  lis.forEach(function(li){
    var k=li.getAttribute('data-i');var v=t(k);
    if(v&&v.indexOf('<')>=0)li.innerHTML=v;
  });
}
window.addEventListener('DOMContentLoaded',function(){
  var saved=localStorage.getItem('bp_lang');locale=saved||detectLang();if(!T[locale])locale='en';
  loadTheme();loadCfg();fillF();onToneCh();onPurpCh();updCnt();loadH();applyI18n();applyGuideHTML();
  if(!localStorage.getItem('bp_guide_done'))openGuide();
});
