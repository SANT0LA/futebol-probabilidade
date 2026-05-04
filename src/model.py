import pandas as pd

def calcular_forca(df):
    times = pd.unique(df[['home_team', 'away_team']].values.ravel())
    
    stats = {}

    for time in times:
        jogos_casa = df[df['home_team'] == time]
        jogos_fora = df[df['away_team'] == time]

        casa_v = (jogos_casa['home_goals'] > jogos_casa['away_goals']).mean()
        casa_e = (jogos_casa['home_goals'] == jogos_casa['away_goals']).mean()
        casa_d = (jogos_casa['home_goals'] < jogos_casa['away_goals']).mean()

        fora_v = (jogos_fora['away_goals'] > jogos_fora['home_goals']).mean()
        fora_e = (jogos_fora['away_goals'] == jogos_fora['home_goals']).mean()
        fora_d = (jogos_fora['away_goals'] < jogos_fora['home_goals']).mean()

        stats[time] = {
            "casa_v": casa_v,
            "casa_e": casa_e,
            "casa_d": casa_d,
            "fora_v": fora_v,
            "fora_e": fora_e,
            "fora_d": fora_d,
        }

    return stats


def prob_jogo(time_a, time_b, stats):
    a = stats[time_a]
    b = stats[time_b]

    prob_vitoria_a = (a["casa_v"] + b["fora_d"]) / 2
    prob_empate = (a["casa_e"] + b["fora_e"]) / 2
    prob_vitoria_b = 1 - prob_vitoria_a - prob_empate

    return [prob_vitoria_a, prob_empate, prob_vitoria_b]