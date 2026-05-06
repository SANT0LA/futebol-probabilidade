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


def monte_carlo_detalhado(jogos_restantes, stats, tabela_atual, n=10000):
    """Simula campeonato e retorna tabelas finais para análise detalhada"""
    tabelas_finais = []
    
    for _ in range(n):
        tabela_final = simular_campeonato(jogos_restantes, stats, tabela_atual)
        tabelas_finais.append(tabela_final)
    
    return tabelas_finais


def calcular_probabilities(tabelas_finais):
    """Calcula probabilidades de campeão, G4, Libertadores, Sul-Americana e rebaixamento"""
    if not tabelas_finais:
        return {}
    
    times = list(tabelas_finais[0].keys())
    n_simulacoes = len(tabelas_finais)
    n_times = len(times)
    
    # Inicializar contadores
    campeao_count = {time: 0 for time in times}
    g4_count = {time: 0 for time in times}
    libertadores_count = {time: 0 for time in times}
    sulamericana_count = {time: 0 for time in times}
    rebaixamento_count = {time: 0 for time in times}
    
    # Contar ocorrências
    for tabela in tabelas_finais:
        # Ordenar times por pontos (descendente)
        classificacao = sorted(times, key=lambda t: tabela[t], reverse=True)
        
        for idx, time in enumerate(classificacao):
            posicao = idx + 1
            
            # Campeão (1º lugar)
            if posicao == 1:
                campeao_count[time] += 1
            
            # G4 (posições 1-4)
            if posicao <= 4:
                g4_count[time] += 1
            
            # Libertadores (posições 1-6)
            if posicao <= 6:
                libertadores_count[time] += 1
            
            # Sul-Americana (posições 5-8, considerando critério comum)
            if 5 <= posicao <= 8:
                sulamericana_count[time] += 1
            
            # Rebaixamento (últimas 4 posições)
            if posicao > n_times - 4:
                rebaixamento_count[time] += 1
    
    # Converter para probabilidades
    resultados = {
        'campeao': {time: campeao_count[time] / n_simulacoes for time in times},
        'g4': {time: g4_count[time] / n_simulacoes for time in times},
        'libertadores': {time: libertadores_count[time] / n_simulacoes for time in times},
        'sulamericana': {time: sulamericana_count[time] / n_simulacoes for time in times},
        'rebaixamento': {time: rebaixamento_count[time] / n_simulacoes for time in times}
    }
    
    return resultados