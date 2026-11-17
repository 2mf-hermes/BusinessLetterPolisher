# -*- coding: utf-8 -*-
import io

p = 'letter-polisher.html'
t = io.open(p, 'r', encoding='utf-8').read()

pairs = [
    ('Apple Design System — iOS 26 / macOS 26 Glass Style', 'Modern Glass Design System'),
    ('/* Accent — Apple system blue */', '/* Accent — system blue */'),
    ('/* Radii — Apple system */', '/* Radii — system */'),
    ('font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue","Noto Sans TC","Segoe UI",sans-serif;',
     'font-family:"Segoe UI","Noto Sans TC","Helvetica Neue",sans-serif;'),
    ('/* ===== Header — iOS navigation bar ===== */', '/* ===== Header — top navigation bar ===== */'),
    ('/* ===== Apple Custom Select / Menu ===== */', '/* ===== Custom Select / Menu ===== */'),
    ('/* Dropdown panel — iOS popover glass */', '/* Dropdown panel — glass popover */'),
    ('/* Options — iOS menu items */', '/* Options — menu items */'),
    ('/* iOS-style checkmark indicator */', '/* Checkmark indicator */'),
    ('/* ===== Cards — Apple glass material ===== */', '/* ===== Cards — glass material ===== */'),
    ('/* ===== Form — Apple-style aligned grid ===== */', '/* ===== Form — aligned grid ===== */'),
    ('/* ===== Buttons — Apple system style ===== */', '/* ===== Buttons — system style ===== */'),
    ('/* Primary — Apple blue pill */', '/* Primary — accent blue pill */'),
    ('/* ===== Tabs — iOS segmented feel ===== */', '/* ===== Tabs — segmented feel ===== */'),
    ('/* ===== FABs — Apple-style floating action ===== */', '/* ===== FABs — floating action ===== */'),
    ('/* ===== Overlay + Panel — iOS sheet ===== */', '/* ===== Overlay + Panel — bottom sheet ===== */'),
    ('<!-- Apple-style 2×2 selector grid -->', '<!-- 2×2 selector grid -->'),
]

count = 0
for old, new in pairs:
    n = t.count(old)
    if n:
        t = t.replace(old, new)
        count += n
        print('replaced %dx: %s' % (n, old[:60]))
    else:
        print('NOT FOUND: %s' % old[:60])

io.open(p, 'w', encoding='utf-8', newline='').write(t)

r = 'README.md'
rt = io.open(r, 'r', encoding='utf-8').read()
n = rt.count('**iOS 26 玻璃風格**')
rt = rt.replace('**iOS 26 玻璃風格**', '**玻璃質感風格**')
io.open(r, 'w', encoding='utf-8', newline='').write(rt)
print('README replaced %dx' % n)
print('total replaced:', count)
