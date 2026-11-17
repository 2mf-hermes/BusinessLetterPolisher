# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.find('id="provider"')
print(s[i - 900:i + 300].replace('><', '>\n<'))
