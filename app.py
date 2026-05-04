import pandas as pd
from src.model import calcular_forca
from src.simulation import monte_carlo
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

# rodar simulação
resultado = monte_carlo(jogos_restantes, stats, tabela_atual, n=1000)

# mostrar resultado
for time, prob in resultado.items():
    print(f"{time}: {prob:.2%}")