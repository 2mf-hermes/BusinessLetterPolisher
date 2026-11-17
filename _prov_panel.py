# Replaces the single-endpoint API block in the settings panel with the
# AI-provider block (provider picker + name + new/delete buttons).
import io, sys

PATH = r"C:\Users\MINFU LIAO\OpenWorker\4e6bb304-22a\商業信件潤飾工具\letter-polisher.html"
with io.open(PATH, "r", encoding="utf-8", newline="") as f:
    html = f.read()

START = '<div class="ps"><div class="ps-t" data-i="apiEndpoint">'
END = '<div class="ps"><div class="custom-prompt">'

assert html.count(START) == 1, "start anchor count=%d" % html.count(START)
assert html.count(END) == 1, "end anchor count=%d" % html.count(END)

NEW = (
    '<div class="ps">'
    '<div class="ps-t" data-i="aiProvider"></div>'
    '<div class="fr">'
    '<div class="fg"><label data-i="provLabel"></label>'
    '<div class="cs cs-nosync" id="provCS">'
    '<button class="cs-btn" onclick="csToggle(this)" type="button"><span class="cs-txt"></span>'
    '<svg class="cs-arr" viewBox="0 0 12 12"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
    '</button><div class="cs-dd" id="provDD"></div><input type="hidden" id="provider" value=""></div>'
    '</div>'
    '<div class="fg"><label data-i="provName"></label><input id="provName" placeholder="OpenAI"></div>'
    '</div>'
    '<div class="btns" style="margin-top:8px;">'
    '<button class="btn btn-s btn-sm" type="button" onclick="newProvider()">'
    '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M8 3.5v9M3.5 8h9"/></svg>'
    '<span data-i="provNew"></span></button>'
    '<button class="btn btn-s btn-sm" type="button" onclick="deleteProvider()">'
    '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5h10M6.5 5V3.5h3V5M5 5l.6 8h4.8L11 5"/></svg>'
    '<span data-i="provDel"></span></button>'
    '</div>'
    '<div class="fr">'
    '<div class="fg"><label>URL</label><input class="mono" id="apiUrl" placeholder="https://api.openai.com/v1/chat/completions"></div>'
    '<div class="fg"><label>API Key</label>'
    '<div style="display:flex;align-items:center;gap:6px;">'
    '<input class="mono" id="apiKey" type="password" placeholder="sk-..." style="flex:1;">'
    '<button type="button" onclick="toggleApiKeyVisibility()" title="Show/Hide API Key" style="flex-shrink:0;background:none;border:0.5px solid var(--bd);border-radius:var(--r3);padding:6px 8px;cursor:pointer;color:var(--tx2);display:flex;align-items:center;justify-content:center;">'
    '<svg id="apiKeyEyeIcon" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16">'
    '<path d="M1 10s4-7 9-7 9 7 9 7-4 7-9 7-9-7-9-7z"/><circle cx="10" cy="10" r="3"/></svg>'
    '</button></div></div>'
    '</div>'
    '<div class="fr">'
    '<div class="fg"><label data-i="modelName"></label>'
    '<div style="display:flex;align-items:center;gap:6px;">'
    '<input id="modelName" placeholder="gpt-4o" style="flex:1;">'
    '<div class="cs cs-nosync" id="modelCS" style="width:auto;flex-shrink:0;">'
    '<button class="cs-btn" id="loadModelsBtn" onclick="openModelPicker(this)" type="button" style="width:auto;white-space:nowrap;" title="">'
    '<span class="cs-txt" data-i="loadModels"></span>'
    '<svg class="cs-arr" viewBox="0 0 12 12"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
    '</button><div class="cs-dd" id="modelDD"></div><input type="hidden" id="modelPick" value=""></div>'
    '</div></div>'
    '<div class="fg"><label data-i="temperature"></label>'
    '<input type="number" id="temperature" value="0.7" min="0" max="2" step="0.1"></div>'
    '</div>'
    '<div class="fr f1">'
    '<div class="fg"><label data-i="apiFormat"></label>'
    '<div class="cs" id="apiFormatCS">'
    '<button class="cs-btn" onclick="csToggle(this)" type="button">'
    '<span class="cs-txt" data-i="fmtOpenAI"></span>'
    '<svg class="cs-arr" viewBox="0 0 12 12"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
    '</button>'
    '<div class="cs-dd">'
    '<div class="cs-opt sel" data-val="openai" data-i="fmtOpenAI" onclick="csPick(this)"><span></span><span class="cs-chk">\u2713</span></div>'
    '<div class="cs-opt" data-val="anthropic" data-i="fmtAnthropic" onclick="csPick(this)"><span></span><span class="cs-chk">\u2713</span></div>'
    '<div class="cs-opt" data-val="gemini" data-i="fmtGemini" onclick="csPick(this)"><span></span><span class="cs-chk">\u2713</span></div>'
    '</div>'
    '<input type="hidden" id="apiFormat" value="openai">'
    '</div></div>'
    '</div>'
    '</div>'
)

html = html[:html.index(START)] + NEW + html[html.index(END):]

with io.open(PATH, "w", encoding="utf-8", newline="") as f:
    f.write(html)

print("panel block replaced; file is now %d chars" % len(html))
