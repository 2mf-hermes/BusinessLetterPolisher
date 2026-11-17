# -*- coding: utf-8 -*-
"""Dump a line range of a file: python _show.py <file> <start> <end> [maxchars]"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

path = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
width = int(sys.argv[4]) if len(sys.argv) > 4 else 400

lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
for i in range(start - 1, min(end, len(lines))):
    print(i + 1, lines[i][:width])
