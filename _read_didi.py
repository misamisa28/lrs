import json
from pathlib import Path

nb = json.loads(Path(r'f:/lrs/statistics.ipynb').read_text(encoding='utf-8'))
s = ''.join(nb['cells'][0]['source'])
start = s.find('def assign_prophet_replaced_jump_markers')
end = s.find('def summarize_prophet_didi_records', start)
print(s[start:end+2500])
