import streamlit as st
import os
import pathlib
import re

# Caminho da pasta
PASTA_CIFRAS = pathlib.Path(__file__).parent / "cifras"
os.makedirs(PASTA_CIFRAS, exist_ok=True)

# Arquivos
arquivos = [f for f in os.listdir(PASTA_CIFRAS) if f.endswith(".txt")]
titulos = [f.replace(".txt", "").replace("-", " ").title() for f in arquivos]

if not arquivos:
    st.warning("Nenhuma cifra encontrada na pasta 'cifras'. Adicione arquivos .txt.")
    st.stop()

# Seleção
st.markdown("### 🎶 Cifras com alinhamento nota/letra no celular")
selecionada = st.selectbox("Escolha a música:", titulos)
arquivo = arquivos[titulos.index(selecionada)]

# Leitura do arquivo
with open(PASTA_CIFRAS / arquivo, "r", encoding="utf-8") as f:
    linhas = f.read().splitlines()

# Detectar se é uma linha de acordes
def linha_de_acordes(linha):
    tokens = re.split(r'\s+', linha.strip())
    return (
        len(tokens) > 0 and
        all(re.fullmatch(r'[A-G][#b]?(m|maj|min|sus|dim|aug|add)?\d*(/[A-G][#b]?)?', t) for t in tokens if t)
    )

# Montar blocos acordes + letra
blocos = []
i = 0
while i < len(linhas):
    linha = linhas[i]
    if linha_de_acordes(linha):
        acorde = linha
        letra = linhas[i+1] if i + 1 < len(linhas) and not linha_de_acordes(linhas[i+1]) else ""
        blocos.append((acorde, letra))
        i += 2 if letra else 1
    else:
        blocos.append(("", linha))  # linha solta de letra (ex: refrão)
        i += 1

# Exibir blocos: nota acima, letra abaixo
for acorde, letra in blocos:
    bloco = f"{acorde}\n{letra}"
    st.markdown(f"```text\n{bloco}\n```")
