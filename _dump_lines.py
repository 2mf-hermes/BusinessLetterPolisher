# -*- coding: utf-8 -*-
"""dump a line range of letter-polisher.html: python _dump_lines.py A B"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
a = int(sys.argv[1])
b = int(sys.argv[2])
L = io.open('letter-polisher.html', encoding='utf-8', newline='').read().split('\r\n')
for i in range(a - 1, min(b, len(L))):
    print(i + 1, ':', L[i][:280])
