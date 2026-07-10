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
df = g['assign_camp_from_identity'](df)
df = g['merge_vote_camps'](df)
df = g['add_markers'](df)

mask = g['_is_prophet_didi_jumper_mask'](df)
lines = [
    f'预通被代跳标记 sum: {int(df["预通被代跳标记"].sum())}',
    f'帮预通滴滴标记 sum: {int(df["帮预通滴滴标记"].sum())}',
    f'起跳预言家标记 sum: {int(df["起跳预言家标记"].sum())}',
    f'jumper mask sum: {int(mask.sum())}',
]
rec = g['summarize_prophet_didi_records'](df)
nonempty = rec[(rec['预通滴滴记录'].fillna('').astype(str).str.strip() != '') | (rec['帮预通滴滴记录'].fillna('').astype(str).str.strip() != '')]
lines.append(f'records nonempty: {len(nonempty)}')
yf = rec[rec['姓名']=='翼风']
if not yf.empty:
    lines.append(f'翼风 预通被代跳次数 in stats would be: {int(((df["姓名"]=="翼风")&(df["预通被代跳标记"]==1)).sum())}')
    lines.append(f'翼风 预通滴滴记录: {yf.iloc[0]["预通滴滴记录"]!r}')
    lines.append(f'翼风 帮预通滴滴记录: {yf.iloc[0]["帮预通滴滴记录"]!r}')

# check 翼风 replaced games
prophets = df.loc[df['预通被代跳标记']==1, ['姓名','日期','版型']]
yf_games = prophets[prophets['姓名']=='翼风']
lines.append(f'翼风 replaced games: {len(yf_games)}')
for _, row in yf_games.iterrows():
    sub = df[(df['日期']==row['日期'])&(df['版型']==row['版型'])]
    jump = sub[mask[sub.index]]
    lines.append(f"  {row['日期']} {row['版型']}: jumpers={jump['姓名'].tolist()}, 起跳={sub.loc[sub['起跳预言家标记']==1,'姓名'].tolist()}")

open(r'f:/lrs/_out.txt', 'w', encoding='utf-8').write('\n'.join(lines))
