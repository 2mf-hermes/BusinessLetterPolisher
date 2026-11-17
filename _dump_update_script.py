import io, sys

exe = '商業信件潤飾工具.exe'
b = open(exe, 'rb').read()

# C# string literals live in the #US heap as UTF-16; scan with both byte alignments.
found = {}
needles = ['set "TARGET=', 'set "SOURCE=', 'set "TEMP_DIR=', 'blp-update-log.txt',
           'setlocal enableextensions', 'findstr /R /C:', 'robocopy exit=', 'goto copy',
           'set /a TRIES+=1', 'if %TRIES% GEQ 90 goto copy', 'start "" "%TARGET%\\',
           '/E /IS /R:5 /W:1 /XD user_data runtime']
for n in needles:
    hit = 0
    for off in (0, 1):
        if b.find(n.encode('utf-16-le'), off) >= 0:
            hit += 1
    found[n] = hit
    print(('OK  ' if hit else 'MISS'), repr(n), 'alignments:', hit)

bad = [n for n in needles if not found[n]]
# the old broken construction must be gone
assert b.find('set TARGET="'.encode('utf-16-le')) < 0, 'old quoted-set line still present'

# reconstruct the cmd template in order for eyeballing
raw = '@echo off'.encode('utf-16-le')
start = b.find(raw)
if start < 0:
    start = b.find(raw, 1) - 1
chunk = b[start:start + 3000].decode('utf-16-le', 'ignore')
out = []
for ch in chunk:
    out.append(ch if (ch.isprintable() or ch in '\r\n\t') else '\u00b7')
print('\n--- exe string heap, cmd template (· marks non-literal gaps) ---')
print(''.join(out))
print('--- end ---')

sys.exit(1 if bad else 0)
