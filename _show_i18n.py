import io, re
h = io.open('letter-polisher.html', encoding='utf-8', newline='').read()
keys = ['aiProvider', 'provLabel', 'provName', 'provNew', 'provDel', 'provDefault', 'provAdded',
        'provDeleted', 'provDeleteConfirm', 'provLastOne', 'needKey', 'needUrl', 'loadModels',
        'loadingModels', 'modelsLoaded', 'modelsFail', 'noModels']
for k in keys:
    print('==', k)
    for m in re.finditer(r"\b" + k + r":'((?:[^'\\]|\\.)*)'", h):
        print('   ', m.group(1))
