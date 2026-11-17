# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')
p = 'letter-polisher.html'
raw = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
old = "  csCloseAll();\n  dd.classList.add('open');btn.classList.add('open');\n  csPlaceMenu(btn,dd);\n}".replace('\n', nl)
new = "  csCloseAll();\n  csPlaceMenu(btn,dd);\n  dd.classList.add('open');btn.classList.add('open');\n}".replace('\n', nl)
print('matches:', raw.count(old))
if raw.count(old) != 1:
    sys.exit(1)
open(p, 'w', encoding='utf-8', newline='').write(raw.replace(old, new, 1))
print('ok openModelPicker order')
