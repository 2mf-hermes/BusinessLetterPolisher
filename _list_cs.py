# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
d = open('letter-polisher.html', encoding='utf-8').read()
for m in re.finditer(r'<div class="cs[^"]*"[^>]*>', d):
    print(m.group(0)[:120])
