import json
s = ''.join(json.load(open(r'f:/lrs/statistics.ipynb', encoding='utf-8'))['cells'][0]['source'])
for kw in ['阵营', 'assign_camp', '狼人', '狼人混']:
    idx = 0
    n = 0
    while n < 3:
        i = s.find(kw, idx)
        if i < 0:
            break
        print(f'--- {kw} at {i} ---')
        print(s[i:i+400])
        print()
        idx = i + len(kw)
        n += 1
