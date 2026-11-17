# -*- coding: utf-8 -*-
"""Rewrite every past release body with the concise note files."""
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

tags = ['v2026.10.01.2', 'v2026.10.01.1', 'v2026.10.01', 'v2026.08.31.3', 'v2026.08.31.2',
        'v2026.08.31.1', 'v2026.08.31', 'v2026.08.29', 'v2026.08.28.2', 'v2026.08.28.1',
        'v2026.08.28', 'v2026.08.27']

for tag in tags:
    r = subprocess.run(['gh', 'release', 'edit', tag, '--title', tag,
                        '--notes-file', 'release-notes-%s.md' % tag],
                       capture_output=True, text=True, encoding='utf-8')
    status = 'OK' if r.returncode == 0 else 'FAIL rc=%d %s' % (r.returncode, (r.stderr or '').strip()[:120])
    print('%-16s %s' % (tag, status))
