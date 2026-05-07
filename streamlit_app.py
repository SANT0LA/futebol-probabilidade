import streamlit as st
import pandas as pd
from src.model import calcular_forca
from src.simulation import monte_carlo_detalhado, calcular_probabilities
from src.utils import criar_tabela_inicial
from src.data_fetch import get_jogos_brasileirao, transformar_em_df
import time

# Configuração da página
st.set_page_config(
    page_title="Probabilidades Brasileirão",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .probability-high {
        color: #28a745;
        font-weight: bold;
    }
    .probability-medium {
        color: #ffc107;
        font-weight: bold;
    }
    .probability-low {
        color: #dc3545;
        font-weight: bold;
    }
    .team-name {
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Cache para dados (evita recarregar a cada interação)
@st.cache_data
def load_data():
    """Carrega e processa os dados dos jogos"""
    data = get_jogos_brasileirao()
    df_jogados, df_restantes = transformar_em_df(data)
    return df_jogados, df_restantes

@st.cache_data
def run_simulation(_df_jogados, _df_restantes, n_simulations=10000):
    """Executa a simulação Monte Carlo"""
    stats = calcular_forca(_df_jogados)
    tabela_atual = criar_tabela_inicial(_df_jogados)
    tabelas_finais = monte_carlo_detalhado(_df_restantes, stats, tabela_atual, n=n_simulations)
    probs = calcular_probabilities(tabelas_finais)
    return probs, stats, tabela_atual

def get_probability_class(prob):
    """Retorna classe CSS baseada na probabilidade"""
    if prob >= 0.5:
        return "probability-high"
    elif prob >= 0.1:
        return "probability-medium"
    else:
        return "probability-low"

def display_probabilities(probs, category_name, description):
    """Exibe as probabilidades de uma categoria específica"""
    st.subheader(f"🎯 {category_name}")
    st.markdown(f"*{description}*")

    # Ordenar por probabilidade decrescente
    sorted_probs = sorted(probs.items(), key=lambda x: x[1], reverse=True)

    # Criar colunas para layout responsivo
    col1, col2 = st.columns(2)

    for i, (team, prob) in enumerate(sorted_probs):
        if prob > 0:  # Só mostrar times com probabilidade > 0
            prob_class = get_probability_class(prob)

            # Alternar entre colunas
            col = col1 if i % 2 == 0 else col2

            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <span class="team-name">{team}</span><br>
                    <span class="{prob_class}">{prob:.1%}</span>
                </div>
                """, unsafe_allow_html=True)

def main():
    # Título principal
    st.markdown('<h1 class="main-header">⚽ Probabilidades do Brasileirão</h1>', unsafe_allow_html=True)

    # Sidebar com informações
    st.sidebar.title("📊 Sobre")
    st.sidebar.markdown("""
    **Análise probabilística do Campeonato Brasileiro**

    Este aplicativo utiliza simulações Monte Carlo para calcular
    as probabilidades de cada time alcançar diferentes objetivos
    no restante do campeonato.
    """)

    # Carregar dados
    with st.spinner("Carregando dados dos jogos..."):
        df_jogados, df_restantes = load_data()

    # Estatísticas rápidas na sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📈 Estatísticas Rápidas**")
    st.sidebar.metric("Jogos Disputados", len(df_jogados))
    st.sidebar.metric("Jogos Restantes", len(df_restantes))

    # Calcular rodada atual aproximada
    total_jogos = len(df_jogados) + len(df_restantes)
    jogos_por_rodada = 10  # Aproximadamente 10 jogos por rodada
    rodada_atual = (len(df_jogados) // jogos_por_rodada) + 1
    rodada_total = total_jogos // jogos_por_rodada

    st.sidebar.metric("Rodada Atual", f"{rodada_atual}/{rodada_total}")

    if len(df_restantes) > 0:
        prox_jogo = df_restantes.iloc[0]
        st.sidebar.markdown("---")
        st.sidebar.markdown("**⚽ Próximo Jogo**")
        st.sidebar.write(f"{prox_jogo['home_team']} vs {prox_jogo['away_team']}")

    # Mostrar informações das simulações se já executadas
    if 'n_simulations' in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown("**🎲 Última Simulação**")
        st.sidebar.metric("Iterações", f"{st.session_state['n_simulations']:,}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**🔧 Configurações**")
    n_simulations = st.sidebar.slider("Número de Simulações", 1000, 50000, 10000, 1000)

    # Executar simulação
    if st.button("🚀 Executar Simulação", type="primary"):
        with st.spinner(f"Executando {n_simulations:,} simulações Monte Carlo (isso pode levar alguns segundos)..."):
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)  # Simular progresso
                progress_bar.progress(i + 1)

            probs, stats, tabela_atual = run_simulation(df_jogados, df_restantes, n_simulations=n_simulations)
            progress_bar.empty()

        st.success(f"✅ Simulação concluída com {n_simulations:,} iterações!")

        # Armazenar resultados na sessão
        st.session_state['probs'] = probs
        st.session_state['tabela_atual'] = tabela_atual
        st.session_state['stats'] = stats
        st.session_state['n_simulations'] = n_simulations

    # Verificar se há resultados na sessão
    if 'probs' in st.session_state:
        probs = st.session_state['probs']
        tabela_atual = st.session_state['tabela_atual']

        # Tabs para diferentes visualizações
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏆 Campeão",
            "🎯 G4",
            "🌎 Libertadores",
            "🇧🇷 Sul-Americana",
            "⬇️ Rebaixamento",
            "📋 Classificação Atual"
        ])

        with tab1:
            display_probabilities(
                probs['campeao'],
                "Chance de Campeonato",
                "Probabilidade de cada time terminar o campeonato em 1º lugar"
            )

        with tab2:
            display_probabilities(
                probs['g4'],
                "Chance de G4",
                "Probabilidade de cada time terminar entre os 4 primeiros colocados"
            )

        with tab3:
            display_probabilities(
                probs['libertadores'],
                "Chance de Libertadores",
                "Probabilidade de cada time se classificar para a Copa Libertadores (posições 1-6)"
            )

        with tab4:
            display_probabilities(
                probs['sulamericana'],
                "Chance de Sul-Americana",
                "Probabilidade de cada time se classificar para a Copa Sul-Americana (posições 5-8)"
            )

        with tab5:
            display_probabilities(
                probs['rebaixamento'],
                "Chance de Rebaixamento",
                "Probabilidade de cada time ser rebaixado para a Série B (últimas 4 posições)"
            )

        with tab6:
            st.subheader("📋 Classificação Atual")
            st.markdown("*Pontuação atual dos times no campeonato*")

            # Ordenar tabela atual
            sorted_tabela = sorted(tabela_atual.items(), key=lambda x: x[1], reverse=True)

            # Criar DataFrame para exibir
            df_classificacao = pd.DataFrame(sorted_tabela, columns=['Time', 'Pontos'])
            df_classificacao.index = range(1, len(df_classificacao) + 1)
            df_classificacao.index.name = 'Posição'

            st.dataframe(df_classificacao)

    else:
        st.info("👆 Clique em 'Executar Simulação' para começar a análise.")

    # Footer
    st.markdown("---")
    st.markdown("*SANTOLA Corp.*")

if __name__ == "__main__":
    main()