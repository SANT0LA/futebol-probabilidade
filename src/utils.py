def criar_tabela_inicial(df):
    tabela = {}

    for _, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']
        hg = row['home_goals']
        ag = row['away_goals']

        if home not in tabela:
            tabela[home] = 0
        if away not in tabela:
            tabela[away] = 0

        if hg > ag:
            tabela[home] += 3
        elif ag > hg:
            tabela[away] += 3
        else:
            tabela[home] += 1
            tabela[away] += 1

    return tabela