import json
from pathlib import Path

import pandas as pd

PROPHET = ['预言家', '通灵师']


def filled(s):
    if pd.isna(s):
        return False
    t = str(s).strip()
    return t not in ('', 'None', '<NA>', 'nan')


def compute_jump(df):
    gk = ['日期', '版型']
    role = df['身份']
    is_good = ~df['阵营'].isin(['狼人', '狼人混'])
    is_prophet = role.isin(PROPHET)
    check = df['D1验人'].apply(filled)
    jump = (is_prophet & check).astype(int)
    prophet_rows = df.loc[is_prophet, gk + ['D1验人']]
    if prophet_rows.empty:
        return jump
    prophet_empty = (
        prophet_rows.groupby(gk)
        .apply(lambda g: not g['D1验人'].apply(filled).any(), include_groups=False)
        .reset_index(name='_all_empty')
    )
    for idx in df.index[is_good & ~is_prophet & check]:
        row = df.loc[idx]
        pe = prophet_empty[(prophet_empty['日期'] == row['日期']) & (prophet_empty['版型'] == row['版型'])]
        if not pe.empty and pe['_all_empty'].iloc[0]:
            jump.loc[idx] = 1
    return jump


for raw_path in sorted(Path(r'f:/lrs/data').glob('*原始数据.json')):
    df = pd.DataFrame(json.loads(raw_path.read_text(encoding='utf-8')))
    gk = ['日期', '版型']
    role = df['身份']
    is_good = ~df['阵营'].isin(['狼人', '狼人混'])
    is_prophet = role.isin(PROPHET)
    check = df['D1验人'].apply(filled)
    prophet_no = is_prophet & ~check
    game_has = df.assign(_g=(is_good & check).astype(int)).groupby(gk)['_g'].transform('max').gt(0)
    replaced = prophet_no & game_has
    df['_replaced'] = replaced.astype(int)
    game_rep = df.groupby(gk)['_replaced'].transform('max').gt(0)
    jump = compute_jump(df)
    old = is_good & check & game_rep
    new = (jump == 1) & ~is_prophet & game_rep
    bad = df[old & ~new]
    if not bad.empty:
        print('FILE', raw_path.name, 'rows old not new', len(bad))
        print(bad[['日期', '姓名', '身份', 'D1验人', 'D1验人结果']].head(10).to_string())
