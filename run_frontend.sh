#!/bin/bash

# Script para executar o frontend Streamlit
echo "🚀 Iniciando Probabilidades do Brasileirão..."

# Verificar se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "❌ Ambiente virtual não encontrado. Execute primeiro:"
    echo "python3 -m venv .venv"
    echo "source .venv/bin/activate"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Ativar ambiente virtual
source .venv/bin/activate

# Verificar se streamlit está instalado
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando Streamlit..."
    pip install streamlit
fi

# Executar o aplicativo
echo "🌐 Abrindo aplicativo em http://localhost:8501"
streamlit run streamlit_app.py --server.headless true --server.port 8501