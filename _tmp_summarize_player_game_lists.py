def summarize_player_game_lists(data):
    """按姓名汇总参与/胜利场次明细：日期（版型，身份）、…"""
    empty = pd.DataFrame({
        '姓名': pd.Series(dtype=str),
        '参与场次': pd.Series(dtype=str),
        '胜利场次': pd.Series(dtype=str),
    })
    if '日期' not in data.columns:
        return empty

    def join_entries(group):
        if group.empty:
            return ''
        ordered = group.sort_values('日期', ascending=False)
        return '、'.join(_format_game_entry(row) for _, row in ordered.iterrows())

    participation = (
        data.groupby('姓名', group_keys=False)
        .apply(join_entries, include_groups=False)
        .reset_index(name='参与场次')
    )
    win_rows = data[data['胜利'].isin(['狼', '好人'])]
    if win_rows.empty:
        participation['胜利场次'] = ''
        return participation
    wins = (
        win_rows.groupby('姓名', group_keys=False)
        .apply(join_entries, include_groups=False)
        .reset_index(name='胜利场次')
    )
    return participation.merge(wins, on='姓名', how='left')
