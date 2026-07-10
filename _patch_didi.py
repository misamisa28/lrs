import json
from pathlib import Path

path = Path(r'f:/lrs/statistics.ipynb')
nb = json.loads(path.read_text(encoding='utf-8'))
src = nb['cells'][0]['source']

start = next(i for i, line in enumerate(src) if line.startswith('def _is_prophet_didi_jumper_mask'))
end = next(i for i in range(start + 1, len(src)) if src[i].startswith('def assign_prophet_replaced_jump_markers'))

block = src[start:end]
text = ''.join(block)
if '            & is_good\n' in text:
    print('already patched')
else:
    needle = "            (data['起跳预言家标记'] == 1)\n\n            & ~role.isin(PROPHET_FIRST_CHECK_ROLES)\n"
    repl = "            (data['起跳预言家标记'] == 1)\n\n            & is_good\n\n            & ~role.isin(PROPHET_FIRST_CHECK_ROLES)\n"
    if needle not in text:
        raise SystemExit('needle not found')
    text = text.replace(needle, repl, 1)
    text = text.replace(
        '    """代跳好人：优先起跳预言家标记且非预/通灵、非狼人混（好人混可计）。"""\n',
        '    """代跳好人：好人侧、起跳预言家标记且非预/通灵、非狼人混（好人混可计）。"""\n',
        1,
    )
    nb['cells'][0]['source'] = src[:start] + [text] + src[end:]
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding='utf-8')
    print('patched statistics.ipynb')
