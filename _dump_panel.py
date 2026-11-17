# -*- coding: utf-8 -*-
import io
d = io.open('letter-polisher.html', encoding='utf-8').read()

# Find the settings panel HTML (sOv)
start = d.index('<div class="ov" id="sOv">')
# Find the closing </div></div> for the panel
# We need to match div depth
depth = 0
for i in range(start, len(d)):
    if d[i:i+5] == '<div ' or d[i:i+4] == '<div':
        depth += 1
    elif d[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            end = i + 6
            break

panel = d[start:end]
print('Length:', len(panel))
# Print with newlines for readability
import re
panel = re.sub(r'(</?div[^>]*>)', r'\1\n', panel)
panel = re.sub(r'(</?button[^>]*>)', r'\1\n', panel)
panel = re.sub(r'(</?input[^>]*>)', r'\1\n', panel)
panel = re.sub(r'(</?label[^>]*>)', r'\1\n', panel)
panel = re.sub(r'(</?select[^>]*>)', r'\1\n', panel)
panel = re.sub(r'(</?option[^>]*>)', r'\1\n', panel)
print(panel[:3000])
print('...')
print(panel[-500:])