# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')
s = open('letter-polisher.html', encoding='utf-8', newline='').read()
i = s.find('id="modelDD"')
print(s[i - 700:i + 200].replace('><', '>\n<'))
