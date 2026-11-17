# -*- coding: utf-8 -*-
"""v2026.10.02 part E: clearance under the floating buttons in the stacked layout.

When the two cards stack (<=860px) the page scrolls and the fixed floating
buttons sat over the last row of content - at 520px wide the history button
covered a copy button in the output card once fully scrolled. The stacked
layout is the only one that scrolls, so the extra bottom space goes there.
"""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
P = 'letter-polisher.html'
s = io.open(P, encoding='utf-8', newline='').read()

old = '@media(max-width:860px){.row2{grid-template-columns:1fr;}}'
new = ('@media(max-width:860px){\r\n'
       '  .row2{grid-template-columns:1fr;}\r\n'
       '  /* Stacked layout scrolls; keep empty room under the content so the\r\n'
       '     floating buttons never sit on top of the last control. */\r\n'
       '  .wrap{padding-bottom:84px;}\r\n'
       '}')
assert s.count(old) == 1, 'breakpoint not found'
s = s.replace(old, new, 1)
io.open(P, 'w', encoding='utf-8', newline='').write(s)
print('v106e applied: stacked layout clears the floating buttons')
