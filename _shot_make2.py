# -*- coding: utf-8 -*-
"""Same as _shot_make.py but without clicking Edit: the collapsed default state."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
src = io.open('letter-polisher.html', encoding='utf-8', newline='').read()
inject = """
<script>
window.addEventListener('load', function () {
  setTimeout(function () {
    var ov = document.getElementById('sOv');
    if (ov) ov.classList.add('open');
  }, 120);
});
</script>
<style>#probeOut{display:none !important;}</style>
</head>
"""
io.open('_shot_closed.html', 'w', encoding='utf-8', newline='').write(src.replace('</head>', inject, 1))
print('wrote _shot_closed.html')
