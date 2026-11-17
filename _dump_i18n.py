import io
L = io.open('letter-polisher.html', encoding='utf-8', newline='').read().split('\n')
for n in (829, 830, 831, 864, 865, 866, 897, 898, 899):
    s = L[n-1]
    print('--- line', n, 'len', len(s))
    print('HEAD:', s[:80])
    print('TAIL:', s[-160:])
    print('updErrorTitle count:', s.count('updErrorTitle:'))
