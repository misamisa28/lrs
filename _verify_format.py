import json
import os
import pandas as pd

nb_path = r'f:/lrs/statistics.ipynb'
src = ''.join(json.load(open(nb_path, encoding='utf-8'))['cells'][0]['source'])
cut = src.find('\ndef export_sheet(')
g = {'pd': pd, 'os': os, '__name__': 'extract'}
exec(compile(src[:cut], nb_path, 'exec'), g)

# unit test helper
events = pd.DataFrame([
    {'姓名': '翼风', '日期': 1, '版型': 'A', '_jumper': '王正刚'},
    {'姓名': '翼风', '日期': 1, '版型': 'A', '_jumper': '周乏'},
    {'姓名': '翼风', '日期': 2, '版型': 'B', '_jumper': '豪哥哥'},
])
print('test:', g['_format_prophet_didi_record'](events))

df = pd.read_excel(r'f:/lrs/粤小.xlsx', sheet_name='S1')
df = g['normalize_special_exile_column'](df)
df = g['normalize_d1_check_result_column'](df)
df = g['assign_camp_from_identity'](df)
df = g['merge_vote_camps'](df)
df = g['add_markers'](df)
rec = g['summarize_prophet_didi_records'](df)
yf = rec[rec['姓名'] == '翼风']
print('翼风:', yf['预通滴滴记录'].iloc[0] if not yf.empty else '')
