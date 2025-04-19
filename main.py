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

# Título e seleção
st.markdown("### 🎶 Cifras de Louvor – Modo Celular")
selecionada = st.selectbox("Escolha a música:", titulos)
arquivo = arquivos[titulos.index(selecionada)]

# Lê a cifra
with open(PASTA_CIFRAS / arquivo, "r", encoding="utf-8") as f:
    cifra = f.read()

# Exibe cifra com alinhamento preservado
st.markdown("##### 📄 Visualização perfeita:")
st.code(cifra, language="text")

# Opcional: copiar texto puro
with st.expander("📋 Copiar texto puro"):
    st.text(cifra)
