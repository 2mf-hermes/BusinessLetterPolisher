import sys
with open('letter-polisher.html', 'r', encoding='utf-8') as f:
    content = f.read()
idx = content.find('id="apiKey"')
if idx == -1:
    print('NOT FOUND')
else:
    print('FOUND at char', idx)
    print('CONTEXT:', repr(content[max(0,idx-300):idx+300]))
