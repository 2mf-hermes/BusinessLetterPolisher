# -*- coding: utf-8 -*-
import io, sys
sys.stdout.reconfigure(encoding='utf-8')
s = io.open('letter-polisher.html', encoding='utf-8', newline='').read()
print('total LF      :', s.count('\n'))
print('total CRLF    :', s.count('\r\n'))
print('LF-only lines :', s.count('\n') - s.count('\r\n'))
lines = s.split('\n')
for i in list(range(726, 733)):
    print(i + 1, repr(lines[i][:150]))
print('grid close check:', repr(lines[729][:80]))
