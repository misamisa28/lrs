import json
import os
import pandas as pd

nb_path = r'f:/lrs/statistics.ipynb'
src = ''.join(json.load(open(nb_path, encoding='utf-8'))['cells'][0]['source'])
cut = src.find('\ndef export_sheet(')
g = {'pd': pd, 'os': os, '__name__': 'extract'}
exec(compile(src[:cut], nb_path, 'exec'), g)

WOLF_ROLES = g['WOLF_IDENTITIES'] | g['WOLF_MIX_IDENTITIES']

for file_name, prefix, sheets in g['DATASETS']:
    for sheet in sheets:
        df = pd.read_excel(f'f:/lrs/{file_name}', sheet_name=sheet)
        df = g['normalize_special_exile_column'](df)
        df = g['normalize_d1_check_result_column'](df)
        df = g['assign_camp_from_identity'](df)
        df = g['merge_vote_camps'](df)
        df = g['add_markers'](df)
        mask = g['_is_prophet_didi_jumper_mask'](df)
        bad = df.loc[mask & (df['阵营'].isin(['狼人', '狼人混']) | df['身份'].isin(WOLF_ROLES))]
        if bad.empty:
            continue
        print('===', prefix, sheet, '===')
        print(bad[['日期', '版型', '姓名', '身份', '阵营', 'D1验人', '起跳预言家标记']].to_string())
        print()

# Also: 起跳 marker on wolf camp with check
for file_name, prefix, sheets in g['DATASETS']:
    for sheet in sheets:
        df = pd.read_excel(f'f:/lrs/{file_name}', sheet_name=sheet)
        df = g['normalize_special_exile_column'](df)
        df = g['normalize_d1_check_result_column'](df)
        df = g['assign_camp_from_identity'](df)
        df = g['merge_vote_camps'](df)
        df = g['add_markers'](df)
        bad = df[(df['起跳预言家标记'] == 1) & (df['阵营'].isin(['狼人', '狼人混']) | df['身份'].isin(WOLF_ROLES))]
        if bad.empty:
            continue
        print('=== jump marker wolves', prefix, sheet, '===')
        print(bad[['日期', '版型', '姓名', '身份', '阵营', 'D1验人']].head(20).to_string())
        print()
