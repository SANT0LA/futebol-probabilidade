import numpy as np
from src.model import prob_jogo


def simular_jogo(probs):
    return np.random.choice(["A", "E", "B"], p=probs)


def simular_campeonato(jogos_restantes, stats, tabela_atual):
    tabela = tabela_atual.copy()

    for _, jogo in jogos_restantes.iterrows():
        probs = prob_jogo(jogo['home_team'], jogo['away_team'], stats)
        resultado = simular_jogo(probs)

        if resultado == "A":
            tabela[jogo['home_team']] += 3
        elif resultado == "B":
            tabela[jogo['away_team']] += 3
        else:
            tabela[jogo['home_team']] += 1
            tabela[jogo['away_team']] += 1

    return tabela


def monte_carlo(jogos_restantes, stats, tabela_atual, n=10000):
    resultados = {time: 0 for time in tabela_atual.keys()}

    for _ in range(n):
        tabela_final = simular_campeonato(jogos_restantes, stats, tabela_atual)
        campeao = max(tabela_final, key=tabela_final.get)
        resultados[campeao] += 1

    for time in resultados:
        resultados[time] /= n

    return resultados