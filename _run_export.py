import json
import os
import pandas as pd

nb_path = r'f:/lrs/statistics.ipynb'
src = ''.join(json.load(open(nb_path, encoding='utf-8'))['cells'][0]['source'])
# include export_sheet but stop before main loop
cut = src.find('\nfor file_name, prefix, sheets in DATASETS:')
if cut < 0:
    cut = len(src)
g = {'pd': pd, 'os': os, '__name__': 'extract'}
exec(compile(src[:cut], nb_path, 'exec'), g)

g['export_sheet'](r'f:/lrs/粤小.xlsx', '粤小', 'S1')

rows = json.load(open(r'f:/lrs/data/粤小S1玩家统计.json', encoding='utf-8'))
yf = next(r for r in rows if r['姓名'] == '翼风')
nonempty = sum(1 for r in rows if str(r.get('预通滴滴记录', '')).strip() or str(r.get('帮预通滴滴记录', '')).strip())
lines = [
    f"翼风 预通被代跳次数: {yf.get('预通被代跳次数')}",
    f"翼风 帮预通滴滴次数: {yf.get('帮预通滴滴次数')}",
    f"翼风 预通滴滴记录: {yf.get('预通滴滴记录')!r}",
    f"翼风 帮预通滴滴记录: {yf.get('帮预通滴滴记录')!r}",
    f'players with records: {nonempty}',
]
open(r'f:/lrs/_out.txt', 'w', encoding='utf-8').write('\n'.join(lines))
