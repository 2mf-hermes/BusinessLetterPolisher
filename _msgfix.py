import io

p = 'letter-polisher.html'
with io.open(p, 'r', encoding='utf-8', newline='') as f:
    h = f.read()

pairs = [
    ("modelsLoaded:'已載入模型清單，共'", "modelsLoaded:'已載入模型清單，共 {n} 個模型'"),
    ("modelsLoaded:'已载入模型清单，共'", "modelsLoaded:'已载入模型清单，共 {n} 个模型'"),
    ("modelsLoaded:'Model list loaded:'", "modelsLoaded:'Model list loaded: {n} models'"),
    ("showTR(t('modelsLoaded')+' '+list.length,'ok')",
     "showTR(t('modelsLoaded').replace('{n}',list.length),'ok')"),
]
for old, new in pairs:
    assert h.count(old) == 1, (old, h.count(old))
    h = h.replace(old, new)

with io.open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(h)
print('model-count message polished;', len(h), 'chars')
