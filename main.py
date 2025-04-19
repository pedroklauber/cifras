import streamlit as st
import os
import pathlib

# Caminho da pasta
PASTA_CIFRAS = pathlib.Path(__file__).parent / "cifras"
os.makedirs(PASTA_CIFRAS, exist_ok=True)

# Lista de arquivos
arquivos = [f for f in os.listdir(PASTA_CIFRAS) if f.endswith(".txt")]
titulos = [f.replace(".txt", "").replace("-", " ").title() for f in arquivos]

if not arquivos:
    st.warning("Nenhuma cifra encontrada na pasta 'cifras'. Adicione arquivos .txt.")
    st.stop()

# Seleção
st.markdown("### 🎶 Visualizador de Cifras com Marcação Inteligente")
selecionada = st.selectbox("Escolha a música:", titulos)
arquivo = arquivos[titulos.index(selecionada)]

# Leitura
with open(PASTA_CIFRAS / arquivo, "r", encoding="utf-8") as f:
    linhas = f.read().splitlines()

# Interpretação dos blocos
blocos = []
i = 0
while i < len(linhas):
    linha = linhas[i].strip()

    if not linha or linha.startswith("//"):  # ignora comentários e vazios
        i += 1
        continue

    if linha.startswith("#"):  # título/seção
        blocos.append(("SECAO", linha[1:].strip()))
        i += 1
        continue

    if linha.startswith(">"):  # acorde + letra abaixo
        acorde = linha[1:].rstrip()
        letra = ""
        if i + 1 < len(linhas):
            prox = linhas[i + 1].strip()
            if prox and not prox.startswith(">") and not prox.startswith("#") and not prox.startswith("//"):
                letra = prox
                i += 1
        blocos.append(("BLOCO", acorde, letra))
        i += 1
        continue

    # letra solta
    blocos.append(("LETRA", linha))
    i += 1

# Exibição
for bloco in blocos:
    if bloco[0] == "SECAO":
        st.markdown(f"**{bloco[1]}**")
    elif bloco[0] == "BLOCO":
        st.markdown(f"```text\n{bloco[1]}\n{bloco[2]}\n```")
    elif bloco[0] == "LETRA":
        st.markdown(f"`{bloco[1]}`")
