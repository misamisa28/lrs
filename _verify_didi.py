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
bad = df.loc[mask & df['身份'].isin(g['WOLF_IDENTITIES'] | g['WOLF_MIX_IDENTITIES'])]
print('wolf identity jumpers:', len(bad))
if not bad.empty:
    print(bad[['姓名','身份','阵营','日期','版型','D1验人']].to_string())

rec = g['summarize_prophet_didi_records'](df)
for _, row in rec.iterrows():
    if row['预通滴滴记录']:
        print(row['姓名'], '->', row['预通滴滴记录'])
