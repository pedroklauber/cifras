import streamlit as st
import os
import pathlib

# Caminho da pasta
PASTA_CIFRAS = pathlib.Path(__file__).parent / "cifras"
os.makedirs(PASTA_CIFRAS, exist_ok=True)

# Carrega arquivos
arquivos = [f for f in os.listdir(PASTA_CIFRAS) if f.endswith(".txt")]
titulos = [f.replace(".txt", "").replace("-", " ").title() for f in arquivos]

if not arquivos:
    st.warning("Nenhuma cifra encontrada na pasta 'cifras'. Adicione arquivos .txt.")
    st.stop()

# Seleção
st.markdown("### 🎶 Cifras – Visual limpo, leitura clara no celular")
selecionada = st.selectbox("Escolha a música:", titulos)
arquivo = arquivos[titulos.index(selecionada)]

# Leitura da cifra
with open(PASTA_CIFRAS / arquivo, "r", encoding="utf-8") as f:
    linhas = f.read().splitlines()

# Quebra a cifra em blocos de 2 linhas: acorde + letra
blocos = []
i = 0
while i < len(linhas):
    linha1 = linhas[i]
    linha2 = linhas[i+1] if i + 1 < len(linhas) else ""
    blocos.append(f"{linha1}\n{linha2}")
    i += 2 if linha2 else 1

# Exibição com blocos st.markdown com alinhamento
for bloco in blocos:
    st.markdown(f"```text\n{bloco}\n```")
