def build_player_stats(data):
    """按姓名汇总并计算比率。"""
    tmp = data.assign(
        狼存活天数=data['存活天数'] * data['狼标记'],
        好人存活天数=data['存活天数'] * data['好人标记'],
    )
    stat = tmp.groupby('姓名').agg(
        出场次数=('姓名', 'count'),
        胜场次数=('胜利标记', 'sum'),
        狼次数=('狼标记', 'sum'),
        技能狼次数=('技能狼标记', 'sum'),
        悍跳次数=('悍跳标记', 'sum'),
        拉杆次数=('拉杆标记', 'sum'),
        拉杆成功次数=('拉杆成功标记', 'sum'),
        起跳预言家次数=('起跳预言家标记', 'sum'),
        自爆次数=('自爆标记', 'sum'),
        非盗宝红狼次数=('非盗宝红狼标记', 'sum'),
        自刀次数=('自刀标记', 'sum'),
        狼队友自刀次数=('狼队友自刀标记', 'sum'),
        首刀女巫次数=('首刀女巫标记', 'sum'),
        好人次数=('好人标记', 'sum'),
        好人胜利次数=('好人胜利标记', 'sum'),
        女巫毒师次数=('女巫毒师标记', 'sum'),
        压毒次数=('压毒标记', 'sum'),
        毒药使用次数=('毒药使用标记', 'sum'),
        毒狼次数=('毒狼人标记', 'sum'),
        猎人次数=('猎人标记', 'sum'),
        猎人技能次数=('猎人技能次数', 'sum'),
        猎人技能狼人次数=('猎人技能狼人次数', 'sum'),
        盲毒次数=('盲毒标记', 'sum'),
        盲毒狼人次数=('盲毒狼人标记', 'sum'),
        摄梦人次数=('摄梦人标记', 'sum'),
        首摄狼人次数=('首摄狼人标记', 'sum'),
        首摄狼王盗宝猎人次数=('首摄狼王盗宝猎人标记', 'sum'),
        被盲毒次数=('被盲毒标记', 'sum'),
        非狼被盲毒次数=('非狼被盲毒标记', 'sum'),
        被首验次数=('被首验标记', 'sum'),
        混血儿榜样次数=('混血儿榜样标记', 'sum'),
        接狼人金水次数=('假金标记', 'sum'),
        机械狼次数=('机械狼标记', 'sum'),
        机械女巫次数=('机械女巫标记', 'sum'),
        机械猎人次数=('机械猎人标记', 'sum'),
        机械守卫次数=('机械守卫标记', 'sum'),
        机械通灵师次数=('机械通灵师标记', 'sum'),
        机械双刀次数=('机械双刀标记', 'sum'),
        机械平民次数=('机械平民标记', 'sum'),
        警徽票正确次数=('警徽票正确标记', 'sum'),
        警徽票次数=('警徽票标记', 'sum'),
        平民放逐票次数=('平民放逐票', 'sum'),
        平民正确放逐票次数=('平民正确放逐票', 'sum'),
        平民警徽票次数=('平民警徽票标记', 'sum'),
        平民警徽票正确次数=('平民警徽票正确标记', 'sum'),
        好人警下次数=('警下标记', 'sum'),
        身份次数=('身份标记', 'sum'),
        预通次数=('预通标记', 'sum'),
        神职身份次数=('神职身份标记', 'sum'),
        狼胜利次数=('狼胜利标记', 'sum'),
        正确放逐票次数=('正确放逐票', 'sum'),
        放逐票次数=('放逐票次数', 'sum'),
        无预通生推正确放逐票次数=('无预通生推正确放逐票', 'sum'),
        无预通放逐票次数=('无预通放逐票', 'sum'),
        存活天数总和=('存活天数', 'sum'),
        狼存活天数总和=('狼存活天数', 'sum'),
        好人存活天数总和=('好人存活天数', 'sum'),
    ).reset_index()
    stat = stat.rename(columns={'首摄狼王盗宝猎人次数': '首摄狼王/盗宝猎人次数'})
    stat = stat.merge(summarize_player_game_lists(data), on='姓名', how='left')
    stat['参与场次'] = stat['参与场次'].fillna('')
    stat['胜利场次'] = stat['胜利场次'].fillna('')
    stat = stat.merge(summarize_prophet_first_check_players(data), on='姓名', how='left')
    stat['首验'] = stat['首验'].fillna('')
    stat = stat.merge(summarize_first_checked_by(data), on='姓名', how='left')
    stat['被首验'] = stat['被首验'].fillna('')
    stat = stat.merge(summarize_blind_poison_wolves(data), on='姓名', how='left')
    stat['盲毒狼人'] = stat['盲毒狼人'].fillna('')
    stat = stat.merge(summarize_poison_records(data), on='姓名', how='left')
    stat['毒药记录'] = stat['毒药记录'].fillna('')
    stat = stat.merge(summarize_hunter_skill_records(data), on='姓名', how='left')
    stat['猎人技能记录'] = stat['猎人技能记录'].fillna('')
    stat = stat.merge(summarize_mixed_blood_records(data), on='姓名', how='left')
    stat['混血儿记录'] = stat['混血儿记录'].fillna('')
    stat = stat.merge(summarize_fake_gold_givers(data), on='姓名', how='left')
    stat['接狼人金水'] = stat['接狼人金水'].fillna('')
    stat = stat.merge(summarize_lagan_records(data), on='姓名', how='left')
    stat['拉杆记录'] = stat['拉杆记录'].fillna('')
    stat = stat.merge(summarize_sheriff_vote_error_records(data), on='姓名', how='left')
    stat['警徽票错误记录'] = stat['警徽票错误记录'].fillna('')
    stat = stat.merge(summarize_identity_win_rates(data), on='姓名', how='left')
    stat['身份胜率'] = stat['身份胜率'].fillna('')
    stat = stat.merge(summarize_banxing_win_rates(data), on='姓名', how='left')
    stat['版型胜率'] = stat['版型胜率'].fillna('')
    stat['平均存活天数'] = (stat['存活天数总和'] / stat['出场次数']).round(1)
    stat['狼人平均存活天数'] = (
        stat['狼存活天数总和'] / stat['狼次数'].replace(0, pd.NA)
    ).fillna(0).round(1)
    stat['好人平均存活天数'] = (
        stat['好人存活天数总和'] / stat['好人次数'].replace(0, pd.NA)
    ).fillna(0).round(1)
    stat = stat.drop(columns=['存活天数总和', '狼存活天数总和', '好人存活天数总和'])
    for name, (num, den) in RATE_COLS.items():
        stat[name] = (stat[num] / stat[den].replace(0, pd.NA)).fillna(0)
    stat = stat.sort_values('出场次数', ascending=False).reset_index(drop=True)
    stat[list(RATE_COLS)] = stat[list(RATE_COLS)].map(lambda x: f'{x:.1%}')
    return stat
