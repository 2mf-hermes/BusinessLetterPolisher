# -*- coding: utf-8 -*-
"""Dump the provider area of the settings panel, one tag per line."""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
start = s.index('data-i="aiProvider"')
end = s.index('</div>', s.index('id="temperature"'))
seg = s[start - 120:end]
seg = re.sub(r'><', '>\n<', seg)
print(seg)
