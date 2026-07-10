import json
import pandas as pd

nb = json.load(open(r'f:/lrs/statistics.ipynb', encoding='utf-8'))
exec(compile(''.join(nb['cells'][0]['source']), 'statistics.ipynb', 'exec'), {'__name__': '__main__'})

# After exec we'd need to not run main - the notebook cell probably runs on import. 
# Better: extract only needed functions
