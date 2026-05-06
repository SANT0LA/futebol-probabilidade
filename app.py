import pandas as pd
from src.model import calcular_forca
from src.simulation import monte_carlo, monte_carlo_detalhado, calcular_probabilities
from src.utils import criar_tabela_inicial

from src.data_fetch import get_jogos_brasileirao, transformar_em_df

# carregar dados da API
data = get_jogos_brasileirao()
df_jogados, df_restantes = transformar_em_df(data)

# salvar para cache (opcional)
df_jogados.to_csv("data/jogos_jogados.csv", index=False)
df_restantes.to_csv("data/jogos_restantes.csv", index=False)

# calcular forças
stats = calcular_forca(df_jogados)

# tabela atual
tabela_atual = criar_tabela_inicial(df_jogados)

# jogos restantes
jogos_restantes = df_restantes

# rodar simulação detalhada
print("Executando simulação...")
tabelas_finais = monte_carlo_detalhado(jogos_restantes, stats, tabela_atual, n=10000)
probs = calcular_probabilities(tabelas_finais)

# Menu de opções
while True:
    print("\n" + "="*50)
    print("OPÇÕES DE EXIBIÇÃO")
    print("="*50)
    print("1. Chance de CAMPEÃO")
    print("2. Chance de G4")
    print("3. Chance de LIBERTADORES")
    print("4. Chance de SUL-AMERICANA")
    print("5. Chance de REBAIXAMENTO")
    print("0. Sair")
    print("="*50)
    
    opcao = input("Escolha uma opção (0-5): ").strip()
    
    if opcao == "0":
        print("Saindo...")
        break
    
    opcoes_mapa = {
        "1": ("campeao", "CHANCE DE CAMPEÃO"),
        "2": ("g4", "CHANCE DE G4"),
        "3": ("libertadores", "CHANCE DE LIBERTADORES"),
        "4": ("sulamericana", "CHANCE DE SUL-AMERICANA"),
        "5": ("rebaixamento", "CHANCE DE REBAIXAMENTO")
    }
    
    if opcao not in opcoes_mapa:
        print("Opção inválida! Tente novamente.")
        continue
    
    chave, titulo = opcoes_mapa[opcao]
    resultado = probs[chave]
    
    print(f"\n{titulo}")
    print("-" * 50)
    
    # Ordenar por probabilidade (decrescente)
    resultado_ordenado = sorted(resultado.items(), key=lambda x: x[1], reverse=True)
    
    for time, prob in resultado_ordenado:
        print(f"{time}: {prob:.2%}")
    
    print("-" * 50)