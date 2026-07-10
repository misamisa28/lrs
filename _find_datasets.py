import json
from pathlib import Path
import re

nb = json.loads(Path(r'f:/lrs/statistics.ipynb').read_text(encoding='utf-8'))
s = ''.join(nb['cells'][0]['source'])
for m in re.finditer(r'DATASETS\s*=', s):
    print(s[m.start():m.start()+500])
    break
