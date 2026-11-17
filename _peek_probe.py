# -*- coding: utf-8 -*-
"""Print a line range of a file. Usage: python _peek_probe.py <file> <from> <to>"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
path = sys.argv[1]
a = int(sys.argv[2])
b = int(sys.argv[3])
lines = io.open(path, encoding='utf-8', newline='').read().split('\r\n')
for i in range(a - 1, min(b, len(lines))):
    print('%d: %s' % (i + 1, lines[i]))
