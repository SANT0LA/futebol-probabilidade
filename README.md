# ⚽ Probabilidades do Brasileirão

Análise probabilística completa do Campeonato Brasileiro usando simulações Monte Carlo.

## 📋 Funcionalidades

- **🏆 Chance de Campeonato**: Probabilidade de cada time ser campeão
- **🎯 Chance de G4**: Probabilidade de terminar entre os 4 primeiros
- **🌎 Libertadores**: Probabilidade de classificação para Copa Libertadores (posições 1-6)
- **🇧🇷 Sul-Americana**: Probabilidade de classificação para Copa Sul-Americana (posições 5-8)
- **⬇️ Rebaixamento**: Probabilidade de rebaixamento para Série B (últimas 4 posições)
- **📋 Classificação Atual**: Tabela de pontos atual dos times

## 🚀 Como executar

### Pré-requisitos
- Python 3.8+
- Ambiente virtual (recomendado)

### Instalação

1. Clone o repositório e entre na pasta:
```bash
cd futebol_prob
```

2. Crie e ative o ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar o Frontend Streamlit

**Opção 1 - Script automático (recomendado):**
```bash
./run_frontend.sh
```

**Opção 2 - Manual:**
```bash
streamlit run streamlit_app.py
```

O aplicativo será aberto no navegador em `http://localhost:8501`

### Executar versão Console (opcional)

```bash
python3 app.py
```

## 📊 Como funciona

1. **Coleta de Dados**: Os dados dos jogos são obtidos via API
2. **Cálculo de Força**: Algoritmo calcula a força relativa de cada time baseado nos jogos já disputados
3. **Simulação Monte Carlo**: São executadas 10.000 simulações do restante do campeonato
4. **Análise de Probabilidades**: Para cada simulação, são calculadas as probabilidades de diferentes cenários

## 🏗️ Estrutura do Projeto

```
futebol_prob/
├── app.py                 # Versão console da aplicação
├── streamlit_app.py       # Frontend Streamlit
├── requirements.txt       # Dependências Python
├── data/                  # Dados dos jogos
│   ├── jogos_jogados.csv
│   ├── jogos_restantes.csv
│   └── jogos.csv
└── src/                   # Código fonte
    ├── data_fetch.py      # Coleta de dados da API
    ├── model.py          # Cálculo de força dos times
    ├── simulation.py     # Simulações Monte Carlo
    └── utils.py          # Utilitários
```

## 🎨 Interface Streamlit

- **Design responsivo** com cards coloridos
- **Navegação por abas** para diferentes análises
- **Visualização clara** das probabilidades com cores indicativas:
  - 🟢 Verde: > 50% (alta chance)
  - 🟡 Amarelo: 10-50% (chance média)
  - 🔴 Vermelho: < 10% (baixa chance)
- **Cache inteligente** para evitar recálculos desnecessários
- **Sidebar informativo** com estatísticas do campeonato
- **Controle de simulações** (1000-50000 iterações)
- **Barra de progresso** durante as simulações

## 📈 Interpretação dos Resultados

- **Probabilidades em verde**: > 50% (alta chance)
- **Probabilidades em amarelo**: 10-50% (chance média)
- **Probabilidades em vermelho**: < 10% (baixa chance)

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias no código, interface ou algoritmos!

## 📄 Licença

Este projeto é para fins educacionais e de análise esportiva.