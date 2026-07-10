import json
import os
import pandas as pd

nb_path = r'f:/lrs/statistics.ipynb'
src = ''.join(json.load(open(nb_path, encoding='utf-8'))['cells'][0]['source'])
cut = src.find('\ndef export_sheet(')
g = {'pd': pd, 'os': os, '__name__': 'extract'}
exec(compile(src[:cut], nb_path, 'exec'), g)

df = pd.read_excel(r'f:/lrs/粤小.xlsx', sheet_name='S1')
df = g['normalize_special_exile_column'](df)
df = g['normalize_d1_check_result_column'](df)
df_raw_camp = g['assign_camp_from_identity'](df.copy())
df = df_raw_camp.copy()
df = g['merge_vote_camps'](df)
df = g['add_markers'](df)

mask = g['_is_prophet_didi_jumper_mask'](df)
hgg = df[(df['姓名'] == '豪哥哥') & mask]
lines = ['豪哥哥 jumper games after merge_vote_camps:']
for _, r in hgg.iterrows():
    raw = df_raw_camp[(df_raw_camp['日期'] == r['日期']) & (df_raw_camp['姓名'] == '豪哥哥')]
    raw_camp = raw.iloc[0]['阵营'] if not raw.empty else '?'
    lines.append(f"{r['日期']} {r['版型']} 身份={r['身份']} 阵营={r['阵营']} raw阵营={raw_camp} 起跳={r['起跳预言家标记']}")

open(r'f:/lrs/_out.txt', 'w', encoding='utf-8').write('\n'.join(lines))
