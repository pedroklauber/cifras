import streamlit as st
import os
import pathlib

# Caminho da pasta de cifras
PASTA_CIFRAS = pathlib.Path(__file__).parent / "cifras"
os.makedirs(PASTA_CIFRAS, exist_ok=True)

# Lista de arquivos
arquivos = [f for f in os.listdir(PASTA_CIFRAS) if f.endswith(".txt")]
titulos = [f.replace(".txt", "").replace("-", " ").title() for f in arquivos]

if not arquivos:
    st.warning("Nenhuma cifra encontrada na pasta 'cifras'. Adicione arquivos .txt.")
    st.stop()

# Seleção
st.markdown("### 🎶 Cifras responsivas com destaque leve")
selecionada = st.selectbox("Escolha a música:", titulos)
arquivo = arquivos[titulos.index(selecionada)]

# Lê e processa cifra
with open(PASTA_CIFRAS / arquivo, "r", encoding="utf-8") as f:
    linhas = f.read().splitlines()

# Opcional: marcar acordes com *
import re

def linha_so_de_acordes(linha):
    tokens = re.split(r'\s+', linha.strip())
    if not tokens:
        return False
    return all(re.fullmatch(r'[A-G][#b]?(m|maj|min|sus|dim|aug|add)?\d*(/[A-G][#b]?)?', t) for t in tokens if t)

def marcar_acordes(linha):
    if linha_so_de_acordes(linha):
        tokens = re.split(r'(\s+)', linha)
        return ''.join(f'*{t}*' if re.fullmatch(r'[A-G][#b]?(m|maj|min|sus|dim|aug|add)?\d*(/[A-G][#b]?)?', t) else t for t in tokens)
    return linha

# Aplica marcação
cifra_formatada = '\n'.join([marcar_acordes(l) for l in linhas])

# Exibe com st.code (melhor para responsividade + modo escuro)
st.code(cifra_formatada, language="text")
