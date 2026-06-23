def summarize_prophet_first_check_players(data):
    """预言家/通灵师身份的 D1夜目标1，按姓名汇总为首验目标：姓名（次数）、…"""
    empty = pd.DataFrame({'姓名': pd.Series(dtype=str), '首验': pd.Series(dtype=str)})
    if NIGHT_TARGET1_COL not in data.columns:
        return empty

    checks = data.loc[
        data['身份'].isin(PROPHET_FIRST_CHECK_ROLES),
        ['姓名', NIGHT_TARGET1_COL],
    ].dropna(subset=[NIGHT_TARGET1_COL])
    checks[NIGHT_TARGET1_COL] = checks[NIGHT_TARGET1_COL].astype(str).str.strip()
    checks = checks[checks[NIGHT_TARGET1_COL] != '']
    if checks.empty:
        return empty

    def format_target_counts(series):
        counts = series.value_counts()
        return '、'.join(
            f'{name}（{int(cnt)}）'
            for name, cnt in counts.sort_values(ascending=False).items()
        )

    return (
        checks.groupby('姓名')[NIGHT_TARGET1_COL]
        .apply(format_target_counts)
        .reset_index(name='首验')
    )
