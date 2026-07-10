import pandas as pd

def filled(v):
    if pd.isna(v):
        return False
    s = str(v).strip()
    return s != '' and s.lower() != 'nan'

df = pd.read_excel(r'f:/lrs/粤小.xlsx', sheet_name='S1')
game_keys = ['日期', '版型']
for g, game in df.groupby(game_keys):
    yf = game[game['姓名'] == '翼风']
    hgg = game[game['姓名'] == '豪哥哥']
    if yf.empty or hgg.empty:
        continue
    yf_row = yf.iloc[0]
    hgg_row = hgg.iloc[0]
    if yf_row['身份'] not in ('预言家', '通灵师'):
        continue
    if filled(yf_row['D1验人']) or not filled(hgg_row['D1验人']):
        continue
    print('\n===', g, '===')
    print(game[['姓名', '身份', '阵营', 'D1验人']].to_string())
