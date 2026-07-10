import json
from pathlib import Path

path = Path(r'f:/lrs/statistics.ipynb')
text = ''.join(json.loads(path.read_text(encoding='utf-8'))['cells'][0]['source'])

insert_after = '    )\n\n\n\ndef _is_prophet_didi_jumper_mask(data):'
new_func = '''    )


def _format_prophet_didi_record(events):
    """预通滴滴记录：同局多名代跳用 - 连接，不同局用顿号连接。"""
    game_keys = ['日期', '版型']
    game_tokens = []
    for _, group in events.groupby(game_keys, sort=False):
        names = []
        for name in group['_jumper']:
            text = str(name).strip()
            if not text or text in ('', '<NA>', 'nan', 'None'):
                continue
            if text not in names:
                names.append(text)
        if not names:
            continue
        game_tokens.append(names[0] if len(names) == 1 else '-'.join(names))
    return _format_name_count_list(game_tokens)



def _is_prophet_didi_jumper_mask(data):'''

if '_format_prophet_didi_record' in text:
    print('already has _format_prophet_didi_record')
else:
    if insert_after not in text:
        raise SystemExit('insert point not found')
    text = text.replace(insert_after, new_func, 1)
    print('inserted _format_prophet_didi_record')

old_summarize = """    prophet_records = (

        events.groupby('姓名')['_jumper']

        .apply(lambda series: _format_name_count_list(series.tolist()))

        .reset_index(name='预通滴滴记录')

    )"""

new_summarize = """    prophet_records = (

        events.groupby('姓名', sort=False)

        .apply(lambda group: _format_prophet_didi_record(group))

        .reset_index(name='预通滴滴记录')

    )"""

if old_summarize not in text:
    if '_format_prophet_didi_record(group)' in text:
        print('summarize already patched')
    else:
        raise SystemExit('summarize block not found')
else:
    text = text.replace(old_summarize, new_summarize, 1)
    print('patched summarize')

old_rule = "'预通滴滴记录': '预通被代跳局中，同局 D1验人 有值的好人姓名（顿号连接），多次则在姓名后加次数，如鲸鱼2次',"
new_rule = """'预通滴滴记录': (
                '预通被代跳局中，同局代跳好人姓名；同局多人用 - 连接，不同局用顿号连接，'
                '同一 token 多次则在末尾加次数，如鲸鱼2次'
            ),"""
if old_rule in text:
    text = text.replace(old_rule, new_rule, 1)
    print('patched notebook rule')

nb = json.loads(path.read_text(encoding='utf-8'))
nb['cells'][0]['source'] = [text]
path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
print('done')
