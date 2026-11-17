import io
h = io.open('letter-polisher.html', encoding='utf-8', newline='').read()
s = h.index('<div class="ps"><div class="ps-t" data-i="apiEndpoint">')
e = h.index('<div class="ps"><div class="custom-prompt">')
seg = h[s:e]
io.open('../seg_dump.txt', 'w', encoding='utf-8').write(seg.replace('><', '>\n<'))
print(len(seg))
