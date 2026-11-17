import io
h = io.open('letter-polisher.html', encoding='utf-8', newline='').read()
i = h.index('id="apiKeyEyeIcon"')
print(h[i + 300:i + 2200])
