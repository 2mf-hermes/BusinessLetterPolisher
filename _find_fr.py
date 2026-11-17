# -*- coding: utf-8 -*-
"""Find CSS rules whose selector mentions the .fr / .f1 / .fg classes."""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
for m in re.finditer(r'([^{}\n]*\.(?:fr|f1|fg)\b[^{}\n]*)\{([^}]*)\}', s):
    line = s[:m.start()].count('\n') + 1
    print('%5d| %s { %s }' % (line, m.group(1).strip()[:120], m.group(2).strip()[:200]))
