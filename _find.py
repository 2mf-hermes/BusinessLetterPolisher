# -*- coding: utf-8 -*-
import io
d = io.open('letter-polisher.html', encoding='utf-8').read()
i = d.index('id="apiKey"')
print('line', d[:i].count('\n') + 1)
print(repr(d[i-150:i+150]))