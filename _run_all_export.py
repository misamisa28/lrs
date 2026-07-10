import json
import os
import pandas as pd

nb_path = r'f:/lrs/statistics.ipynb'
src = ''.join(json.load(open(nb_path, encoding='utf-8'))['cells'][0]['source'])
cut = src.find('\nfor file_name, prefix, sheets in DATASETS:')
g = {'pd': pd, 'os': os, '__name__': 'extract'}
exec(compile(src[:cut], nb_path, 'exec'), g)

for file_name, prefix, sheets in g['DATASETS']:
    for sheet in sheets:
        path = os.path.join('f:/lrs', file_name)
        print('export', prefix, sheet)
        g['export_sheet'](path, prefix, sheet)

print('all done')
