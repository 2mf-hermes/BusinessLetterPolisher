// Headless test for the AI-provider feature: multi-provider storage, dropdown
// switching, legacy single-endpoint migration and the model-list loader.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { JSDOM } from 'jsdom';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(__dirname, 'letter-polisher.html'), 'utf8');

let pass = 0, fail = 0;
function check(name, cond, extra) {
  if (cond) { pass++; console.log('  ok   ' + name); }
  else { fail++; console.log('  FAIL ' + name + (extra !== undefined ? '  -> ' + JSON.stringify(extra) : '')); }
}

console.log('AI provider mode');

// --- static checks -------------------------------------------------------
const KEYS = ['aiProvider', 'provLabel', 'provName', 'provNew', 'provDel', 'provDefault',
  'provAdded', 'provDeleted', 'provDeleteConfirm', 'provLastOne', 'needKey', 'needUrl',
  'loadModels', 'loadingModels', 'modelsLoaded', 'modelsFail', 'noModels'];
KEYS.forEach(k => {
  const n = (html.match(new RegExp('\\b' + k + ':', 'g')) || []).length;
  check('i18n ' + k + ' in all 3 locales', n === 3, 'found ' + n);
});
check('provider picker markup present',
  /id="provCS"/.test(html) && /id="provDD"/.test(html) && /id="provider"/.test(html));
check('model picker markup present',
  /id="loadModelsBtn"/.test(html) && /id="modelDD"/.test(html) && /id="modelPick"/.test(html));
check('provider name field present', /id="provName"/.test(html));
check('two dynamic pickers flagged cs-nosync', (html.match(/cs cs-nosync/g) || []).length === 2);
check('no leftover single-endpoint section', !/data-i="apiEndpoint"/.test(html));
check('initProviders wired into boot', /loadCfg\(\);initProviders\(\);fillF\(\);/.test(html));
check('csPick routes provider/model picks',
  /id==='provider'\)onProviderPick\(/.test(html) && /id==='modelPick'\)onModelPick\(/.test(html));
check('csSyncAll skips dynamic pickers', /cs-nosync'\)\)return;/.test(html));

// --- URL / key / model block + menu-placement regressions ------------------
// The connection block ships collapsed; its labels must exist in every locale.
['provEdit', 'provDetails', 'provSave', 'provCancel'].forEach(k => {
  const n = (html.match(new RegExp('\\b' + k + ':', 'g')) || []).length;
  check('i18n ' + k + ' in all 3 locales', n === 3, 'found ' + n);
});
check('connection block markup present',
  /id="provEditBox"/.test(html) && /id="provEditBtn"/.test(html) && /class="pe-h"/.test(html));
check('connection block is hidden until add/edit',
  /\.prov-edit\{[\s\S]{0,160}?display:none/.test(html) && /\.prov-edit\.open\{[\s\S]{0,80}?display:block/.test(html));
const ddAt = html.indexOf('.cs-dd{');
const ddRule = html.slice(ddAt, html.indexOf('}', ddAt));
check('menu rule animates opacity only',
  /transition:opacity/.test(ddRule) && !/transition:\s*(all|transform)/.test(ddRule), ddRule.slice(-60));
check('menu placement freezes transitions while measuring',
  /\.cs-dd-fx\{[^}]*transition:none/.test(html) && /dd\.classList\.add\('cs-dd-fx'\)/.test(html)
  && /dd\.classList\.remove\('cs-dd-fx'\)/.test(html));
check('menu placement self-correction is bounded', /Math\.abs\(dx\)<=24/.test(html) && /Math\.abs\(dy\)<=24/.test(html));
check('menus opened during the slide are re-placed once it settles',
  /function csSettleFix/.test(html) && /\[120,300,520,760\]/.test(html)
  && /if\(btn\.closest\('\.panel-body'\)\)\{csPlaceMenu\(btn,dd\);csSettleFix\(/.test(html));

// --- behaviour ------------------------------------------------------------
const LEGACY = {
  apiUrl: 'https://api.openai.com/v1/chat/completions',
  apiKey: 'sk-legacy', modelName: 'gpt-4o', apiFormat: 'openai', temperature: 0.7,
};

const dom = new JSDOM(html, {
  runScripts: 'dangerously',
  url: 'http://localhost/',
  pretendToBeVisual: true,
  beforeParse(window) {
    window.localStorage.setItem('bp_cfg', JSON.stringify(LEGACY));
  },
});
const { window } = dom;
const doc = window.document;

window.confirm = () => true;
window.fetch = () => Promise.resolve({ ok: true, json: () => Promise.resolve({ data: [] }), text: () => Promise.resolve('') });

const ready = new Promise(res => {
  if (doc.readyState === 'complete') res();
  else window.addEventListener('load', res);
});

await ready;

const val = id => doc.getElementById(id).value;
const provText = () => doc.querySelector('#provCS .cs-txt').textContent;
const modelOpts = () => [...doc.querySelectorAll('#modelDD .cs-opt')].map(o => o.dataset.val);
const provOpts = () => [...doc.querySelectorAll('#provDD .cs-opt')].map(o => o.dataset.val);

// 1. legacy single-endpoint config is migrated into a named provider
check('legacy config migrated to one provider', window.providers.length === 1, window.providers.length);
check('migrated provider named after the OpenAI preset', provText() === 'OpenAI', provText());
check('migrated provider keeps url/key/model',
  val('apiUrl') === LEGACY.apiUrl && val('apiKey') === LEGACY.apiKey && val('modelName') === 'gpt-4o');
check('active provider drives cfg', window.cfg.apiUrl === LEGACY.apiUrl && window.cfg.modelName === 'gpt-4o');
check('provider dropdown lists the provider', provOpts().length === 1);

// 1b. the URL/key/model/temperature block is collapsed until add or edit
const cbox = doc.getElementById('provEditBox');
check('connection block holds url/key/model/temperature',
  ['apiUrl', 'apiKey', 'modelName', 'modelCS', 'temperature'].every(id => cbox.contains(doc.getElementById(id))));
check('add and edit buttons stay outside the block',
  !cbox.contains(doc.querySelector('[onclick="newProvider()"]')) && !cbox.contains(doc.getElementById('provEditBtn')));
check('connection block starts collapsed', !cbox.classList.contains('open'));
window.editProvider();
check('edit opens the connection block', cbox.classList.contains('open'));
window.cancelProviderEdit();
check('cancel collapses the connection block again', !cbox.classList.contains('open'));

// 2. adding a provider
window.newProvider();
check('add opens the connection block for the new provider', cbox.classList.contains('open'));
check('newProvider adds a second provider', window.providers.length === 2, window.providers.length);
check('new provider becomes active and clears the form',
  val('apiUrl') === '' && val('provName').indexOf('AI') === 0, val('provName'));
check('cfg follows the new empty provider', window.cfg.apiUrl === '');
check('dropdown now offers both', provOpts().length === 2);
window.saveProviderEdit();
check('save collapses the connection block', !cbox.classList.contains('open'));

// 3. switching back restores the stored values
const firstId = window.providers[0].id;
const firstOpt = doc.querySelector(`#provDD .cs-opt[data-val="${firstId}"]`);
window.csPick(firstOpt);
check('switching back restores url/key/model',
  val('apiUrl') === LEGACY.apiUrl && val('modelName') === 'gpt-4o' && provText() === 'OpenAI');
check('cfg follows the switched provider', window.cfg.apiUrl === LEGACY.apiUrl);

// 4. edits are kept per provider
window.sV('apiUrl', 'https://api.deepseek.com/chat/completions');
window.sV('provName', 'DeepSeek');
window.persistActiveProvider();
const newId = window.providers[1].id;
window.csPick(doc.querySelector(`#provDD .cs-opt[data-val="${newId}"]`));
window.sV('apiUrl', 'https://api.groq.com/openai/v1/chat/completions');
window.sV('modelName', 'llama-3.3-70b-versatile');
window.persistActiveProvider();
window.csPick(doc.querySelector(`#provDD .cs-opt[data-val="${firstId}"]`));
check('first provider kept its edited name', provText() === 'DeepSeek', provText());
check('first provider kept its edited url', val('apiUrl') === 'https://api.deepseek.com/chat/completions', val('apiUrl'));
window.csPick(doc.querySelector(`#provDD .cs-opt[data-val="${newId}"]`));
check('second provider kept its own url/model',
  val('apiUrl') === 'https://api.groq.com/openai/v1/chat/completions' && val('modelName') === 'llama-3.3-70b-versatile');

// 5. models endpoint derivation
check('openai chat endpoint -> /v1/models',
  window.modelsUrlFor('https://api.openai.com/v1/chat/completions', 'openai') === 'https://api.openai.com/v1/models',
  window.modelsUrlFor('https://api.openai.com/v1/chat/completions', 'openai'));
check('anthropic messages endpoint -> /v1/models',
  window.modelsUrlFor('https://api.anthropic.com/v1/messages', 'anthropic') === 'https://api.anthropic.com/v1/models');
check('gemini generateContent endpoint -> /v1beta/models',
  window.modelsUrlFor('https://generativelanguage.googleapis.com/v1beta/models/GEMINI_MODEL:generateContent', 'gemini')
  === 'https://generativelanguage.googleapis.com/v1beta/models',
  window.modelsUrlFor('https://generativelanguage.googleapis.com/v1beta/models/GEMINI_MODEL:generateContent', 'gemini'));
check('local ollama endpoint -> /v1/models',
  window.modelsUrlFor('http://localhost:11434/v1/chat/completions', 'openai') === 'http://localhost:11434/v1/models');
check('bare base url -> /models', window.modelsUrlFor('https://example.com/v1/', 'openai') === 'https://example.com/v1/models');

// 6. response parsing for the three formats
check('openai list parsed', JSON.stringify(window.parseModelList({ data: [{ id: 'gpt-4o' }, { id: 'gpt-4o-mini' }] }, 'openai'))
  === '["gpt-4o","gpt-4o-mini"]');
check('anthropic duplicates removed', window.parseModelList({ data: [{ id: 'a' }, { id: 'a' }] }, 'anthropic').length === 1);
check('gemini prefixes stripped and non-generate models dropped',
  JSON.stringify(window.parseModelList({ models: [{ name: 'models/gemini-2.0-flash' }, { name: 'models/embed', supportedGenerationMethods: ['embedContent'] }] }, 'gemini'))
  === '["gemini-2.0-flash"]');

// 7. loading a model list from the API
let askedUrl = null, askedHeaders = null;
window.fetch = (url, opts) => {
  askedUrl = url; askedHeaders = (opts && opts.headers) || {};
  return Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ data: [{ id: 'z-model' }, { id: 'a-model' }] }),
    text: () => Promise.resolve(''),
  });
};
window.sV('apiKey', 'sk-test');
const loaded = await window.fetchModelList();
check('fetchModelList returns the parsed list', Array.isArray(loaded) && loaded.length === 2, loaded);
check('models request hits the derived endpoint', askedUrl === 'https://api.groq.com/openai/v1/models', askedUrl);
check('models request carries the bearer key', askedHeaders.Authorization === 'Bearer sk-test', askedHeaders.Authorization);
check('model dropdown is populated', JSON.stringify(modelOpts()) === '["a-model","z-model"]', modelOpts());
check('model list cached on the provider', window.providers[1].models.length === 2);
check('success message reports the model count',
  doc.getElementById('testR').textContent.indexOf(window.T[window.locale].modelsLoaded.replace('{n}', 2)) === 0,
  doc.getElementById('testR').textContent);

// 8. picking a model fills the model field and cfg
window.sV('modelName', '');
window.onModelPick('z-model');
check('picking a model fills modelName', val('modelName') === 'z-model', val('modelName'));
check('picking a model updates cfg', window.cfg.modelName === 'z-model');

// 9. failures surface instead of silently doing nothing
window.fetch = () => Promise.resolve({ ok: false, status: 401, json: () => Promise.resolve({}), text: () => Promise.resolve('unauthorized') });
const bad = await window.fetchModelList();
const tr = doc.getElementById('testR');
check('failed model load reports an error', bad === null && /401/.test(tr.textContent), tr.textContent);
check('error text mentions manual entry', /modelsFail|type the model name|輸入模型名稱|输入模型名称/.test(tr.textContent), tr.textContent);

// 10. missing key/url guarded
window.sV('apiKey', '');
const noKey = await window.fetchModelList();
check('load without API key is refused', noKey === null, noKey);

// 11. deletion rules
window.sV('apiKey', 'x');
window.confirm = () => true;
window.deleteProvider();
check('provider deleted when more than one exists', window.providers.length === 1, window.providers.length);
window.deleteProvider();
check('last provider cannot be deleted', window.providers.length === 1, window.providers.length);
check('dropdown still lists the last provider', provOpts().length === 1);

// 12. reload shows the saved providers (no re-migration)
window.sV('provName', 'Kept');
window.sV('apiUrl', 'https://api.anthropic.com/v1/messages');
window.sV('modelName', 'claude-sonnet-4-20250514');
window.sV('apiFormat', 'anthropic');
window.persistActiveProvider();
const dom2 = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost/', beforeParse(w) {
  w.localStorage.setItem('bp_providers', window.localStorage.getItem('bp_providers'));
  w.localStorage.setItem('bp_active_provider', window.localStorage.getItem('bp_active_provider'));
  w.localStorage.setItem('bp_cfg', window.localStorage.getItem('bp_cfg'));
} });
await new Promise(res => { if (dom2.window.document.readyState === 'complete') res(); else dom2.window.addEventListener('load', res); });
check('saved provider survives a reload',
  dom2.window.document.getElementById('provName').value === 'Kept'
  && dom2.window.document.getElementById('apiUrl').value === 'https://api.anthropic.com/v1/messages'
  && dom2.window.cfg.apiFormat === 'anthropic',
  dom2.window.document.getElementById('provName').value);
check('reload does not create extra providers', dom2.window.providers.length === 1, dom2.window.providers.length);

// 13. locale switch keeps the provider UI translated and intact
dom2.window.locale = 'zh-CN';
dom2.window.applyI18n();
check('provider fields survive a locale switch', dom2.window.document.getElementById('provName').value === 'Kept');
check('load-models button is translated',
  dom2.window.document.querySelector('#loadModelsBtn .cs-txt').textContent === dom2.window.T['zh-CN'].loadModels,
  dom2.window.document.querySelector('#loadModelsBtn .cs-txt').textContent);
check('provider label is translated',
  dom2.window.document.querySelector('[data-i="aiProvider"]').textContent === dom2.window.T['zh-CN'].aiProvider);

console.log('\n' + pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
