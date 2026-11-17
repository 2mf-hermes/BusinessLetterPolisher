# -*- coding: utf-8 -*-
"""Render the settings sheet with the provider connection block open, so the
new collapsed/expanded arrangement can be eyeballed."""
import io
import sys

sys.stdout.reconfigure(encoding='utf-8')
src = io.open('letter-polisher.html', encoding='utf-8', newline='').read()

inject = """
<script>
window.addEventListener('load', function () {
  function go() {
    var ov = document.getElementById('sOv');
    if (ov) ov.classList.add('open');
    var b = document.getElementById('provEditBtn');
    if (b && !document.getElementById('provEditBox').classList.contains('open')) b.click();
  }
  setTimeout(go, 120);
});
</script>
<style>#probeOut{display:none !important;}</style>
</head>
"""
out = src.replace('</head>', inject, 1)
io.open('_shot.html', 'w', encoding='utf-8', newline='').write(out)
print('wrote _shot.html')
