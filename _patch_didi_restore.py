import json
from pathlib import Path

path = Path(r'f:/lrs/statistics.ipynb')
text = ''.join(json.loads(path.read_text(encoding='utf-8'))['cells'][0]['source'])

# 1) Don't run replaced markers before 起跳 exists
old_medium = """        ).fillna(False).astype(int)



    return assign_prophet_replaced_jump_markers(data)



def add_markers(data):"""

new_medium = """        ).fillna(False).astype(int)



    return data



def add_markers(data):"""

# 2) Run replaced markers after jump markers
old_add = """    data = assign_jump_prophet_markers(data)

    data = assign_help_prophet_didi_markers(data)"""

new_add = """    data = assign_jump_prophet_markers(data)

    data = assign_prophet_replaced_jump_markers(data)

    data = assign_help_prophet_didi_markers(data)"""

# 3) Fix merge index bug: preserve original row index
old_pick = """    candidates = data.loc[case1_base, pick_cols].copy()

    merged = candidates.merge(

        prophet_check_empty[game_keys + ['_prophet_all_empty']],

        on=game_keys,

        how='left',

    )

    merged = merged[merged['_prophet_all_empty'].fillna(False)]

    if merged.empty:

        return data

    if D1_SPEECH_ORDER_COL in merged.columns:

        speech = merged[D1_SPEECH_ORDER_COL].astype('string').str.strip()

        merged['_pick_rank'] = pd.to_numeric(speech, errors='coerce').fillna(999)

    else:

        merged['_pick_rank'] = 999

    merged = merged.sort_values([*game_keys, '_pick_rank', '姓名'])

    picked_idx = merged.drop_duplicates(subset=game_keys, keep='first').index

    data.loc[picked_idx, '起跳预言家标记'] = 1"""

new_pick = """    candidates = data.loc[case1_base, pick_cols].copy()

    candidates['_orig_idx'] = candidates.index

    merged = candidates.merge(

        prophet_check_empty[game_keys + ['_prophet_all_empty']],

        on=game_keys,

        how='left',

    )

    merged = merged[merged['_prophet_all_empty'].fillna(False)]

    if merged.empty:

        return data

    if D1_SPEECH_ORDER_COL in merged.columns:

        speech = merged[D1_SPEECH_ORDER_COL].astype('string').str.strip()

        merged['_pick_rank'] = pd.to_numeric(speech, errors='coerce').fillna(999)

    else:

        merged['_pick_rank'] = 999

    merged = merged.sort_values([*game_keys, '_pick_rank', '姓名'])

    picked_idx = merged.drop_duplicates(subset=game_keys, keep='first')['_orig_idx']

    data.loc[picked_idx, '起跳预言家标记'] = 1"""

for name, old, new in [('medium', old_medium, new_medium), ('add', old_add, new_add), ('pick', old_pick, new_pick)]:
    if old not in text:
        raise SystemExit(f'{name} block not found')
    text = text.replace(old, new, 1)
    print(f'patched {name}')

nb = json.loads(path.read_text(encoding='utf-8'))
nb['cells'][0]['source'] = [text]
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print('done')
