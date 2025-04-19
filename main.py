import streamlit as st
import os
import pathlib
import re

# Caminho da pasta de cifras
PASTA_CIFRAS = pathlib.Path(__file__).parent / "cifras"
os.makedirs(PASTA_CIFRAS, exist_ok=True)

# Lista de arquivos
arquivos = [f for f in os.listdir(PASTA_CIFRAS) if f.endswith(".txt")]
titulos = [f.replace(".txt", "").replace("-", " ").title() for f in arquivos]

if not arquivos:
    st.warning("Nenhuma cifra encontrada na pasta 'cifras'. Adicione arquivos .txt.")
    st.stop()

# Estilo customizado
st.markdown("""
    <style>
        .cifra-box {
            background-color: #f9f9f9;
            font-family: monospace;
            font-size: 15px;
            padding: 18px;
            border-radius: 10px;
            white-space: pre-wrap;
            line-height: 1.6;
            overflow-x: auto;
        }
        .acorde {
            color: #1a5dcc;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Seleção
st.markdown("### 🎶 Cifras com destaque de acordes (ideal para celular)")
selecionada = st.selectbox("Escolha a música:", titulos)
arquivo = arquivos[titulos.index(selecionada)]

# Lê a cifra
with open(PASTA_CIFRAS / arquivo, "r", encoding="utf-8") as f:
    linhas = f.read().splitlines()

# Detecta linhas de acordes e aplica destaque
def linha_so_de_acordes(linha):
    tokens = re.split(r'\s+', linha.strip())
    if not tokens:
        return False
    return all(re.fullmatch(r'[A-G][#b]?(m|maj|min|sus|dim|aug|add)?\d*(/[A-G][#b]?)?', t) for t in tokens if t)

def formatar_linha(linha):
    linha_espacada = linha.replace(' ', '&nbsp;')
    if linha_so_de_acordes(linha):
        return f'<span class="acorde">{linha_espacada}</span>'
    return linha_espacada

# Gera HTML final
html_cifra = "<br>".join([formatar_linha(l) for l in linhas])
st.markdown(f'<div class="cifra-box">{html_cifra}</div>', unsafe_allow_html=True)
