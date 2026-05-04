from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("API_KEY")

def get_jogos_brasileirao():
    url = "https://v3.football.api-sports.io/fixtures"
    
    headers = {
        "x-apisports-key": API_KEY
    }

    params = {
        "league": 71,   # Brasileirão Série A
        "season": 2024
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data

import pandas as pd

def transformar_em_df(data):
    jogos_jogados = []
    jogos_restantes = []

    for item in data['response']:
        jogo = {
            "home_team": item['teams']['home']['name'],
            "away_team": item['teams']['away']['name'],
            "home_goals": item['goals']['home'],
            "away_goals": item['goals']['away']
        }
        
        if item['fixture']['status']['short'] == 'FT':
            jogos_jogados.append(jogo)
        else:
            jogos_restantes.append(jogo)

    df_jogados = pd.DataFrame(jogos_jogados)
    df_restantes = pd.DataFrame(jogos_restantes)
    
    return df_jogados, df_restantes