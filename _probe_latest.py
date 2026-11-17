import zipfile, re, sys, hashlib, io
sys.stdout.reconfigure(encoding='utf-8')
p = r'..\dist\_latest_probe.zip'
z = zipfile.ZipFile(p)
name = [x for x in z.namelist() if x.endswith('letter-polisher.html')][0]
raw = z.read(name)
t = raw.decode('utf-8')
m = re.search(r"APP_VERSION='([0-9.]+)'", t)
print('asset file      :', p)
print('in-zip html     :', name)
print('in-asset version:', m.group(1) if m else 'N/A')
local = open('letter-polisher.html', 'rb').read()
print('same bytes as local source:', hashlib.sha256(raw).hexdigest() == hashlib.sha256(local).hexdigest())
print('markers:')
for k in ['function cleanResult', "applyPreset", "source letter's language", 'presetApplied']:
    print('  ', k, '->', k in t)
