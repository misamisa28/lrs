import json
import re
from collections import Counter
from pathlib import Path

import pandas as pd

PROPHET = ['预言家', '通灵师']


def filled(s):
    if pd.isna(s):
        return False
    t = str(s).strip()
    return t not in ('', 'None', '<NA>', 'nan')


def parse_names(s):
    if not s:
        return []
    out = []
    for p in str(s).split('、'):
        p = p.strip()
        if not p:
            continue
        m = re.match(r'(.+?)(\d+)次$', p)
        out.append((m.group(1), int(m.group(2))) if m else (p, 1))
    return out


for stat_path in sorted(Path(r'f:/lrs/data').glob('*玩家统计.json')):
    stats = json.loads(stat_path.read_text(encoding='utf-8'))
    by = {r['姓名']: r for r in stats}
    for a, b in [('陈俊洁', 'JY'), ('JY', '陈俊洁')]:
        if a not in by or b not in by:
            continue
        pa = parse_names(by[a].get('预通滴滴记录', ''))
        ha = parse_names(by[a].get('帮预通滴滴记录', ''))
        pb = parse_names(by[b].get('预通滴滴记录', ''))
        hb = parse_names(by[b].get('帮预通滴滴记录', ''))
        an = {n for n, _ in pa}
        bn = {n for n, _ in pb}
        ahn = {n for n, _ in ha}
        bhn = {n for n, _ in hb}
        if b in an and a not in bhn:
            print(stat_path.name, f'{a} 预通滴滴有 {b}, 但 {b} 帮预通滴滴无 {a}:', by[b].get('帮预通滴滴记录'))
        if a in bn and b not in ahn:
            print(stat_path.name, f'{b} 预通滴滴有 {a}, 但 {a} 帮预通滴滴无 {b}:', by[a].get('帮预通滴滴记录'))
        if b in an:
            print(stat_path.name, 'OK pair:', a, 'didi', by[a].get('预通滴滴记录'), '|', b, 'help', by[b].get('帮预通滴滴记录'), 'help_count', by[b].get('帮预通滴滴次数'))
