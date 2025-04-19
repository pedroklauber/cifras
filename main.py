import streamlit as st
import os
import pathlib

# Caminho dos arquivos
BASE_DIR = pathlib.Path(__file__).parent
PASTA_CIFRAS = BASE_DIR / "cifras"
os.makedirs(PASTA_CIFRAS, exist_ok=True)

ARQUIVO_LISTA = BASE_DIR / "lista.txt"
if not ARQUIVO_LISTA.exists():
    st.warning("Arquivo 'lista.txt' não encontrado.")
    st.stop()

# Categorias disponíveis
categorias = ["Clássico", "Libertação", "Festivo", "Oração", "Adoração"]
cifras_por_categoria = {cat: [] for cat in categorias}

# Leitura do lista.txt
with open(ARQUIVO_LISTA, "r", encoding="utf-8") as f:
    for linha in f:
        if "|" not in linha:
            continue
        titulo, categoria, arquivo = [x.strip() for x in linha.strip().split("|")]
        if categoria in cifras_por_categoria:
            cifras_por_categoria[categoria].append((titulo, arquivo))

st.set_page_config(page_title="Cifras por Categoria", layout="wide")
st.markdown("## 🎶 Cifras por Estilo")

# Layout em colunas por categoria
colunas = st.columns(len(categorias))
for i, cat in enumerate(categorias):
    with colunas[i]:
        st.markdown(f"### {cat}")
        for titulo, arquivo in cifras_por_categoria[cat]:
            if st.button(titulo, key=f"{cat}-{titulo}"):
                st.session_state["cifra_selecionada"] = (titulo, arquivo)

# Exibe cifra se selecionada
if "cifra_selecionada" in st.session_state:
    titulo, arquivo = st.session_state["cifra_selecionada"]
    st.markdown(f"---\n### 📄 {titulo}\n")

    path_arquivo = PASTA_CIFRAS / arquivo
    if not path_arquivo.exists():
        st.error(f"O arquivo '{arquivo}' não foi encontrado na pasta 'cifras'.")
        st.stop()

    with open(path_arquivo, "r", encoding="utf-8") as f:
        linhas = f.read().splitlines()

    # Interpretar marcação com ::
    blocos = []
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()

        if not linha or linha.startswith("//"):
            i += 1
            continue

        if linha.startswith("#"):
            blocos.append(("SECAO", linha[1:].strip()))
            i += 1
            continue

        if linha.startswith("::"):
            acorde = ""
            letra = ""
            if i + 1 < len(linhas) and linhas[i + 1].strip().startswith(">"):
                acorde = linhas[i + 1].strip()[1:]
                i += 1
            if i + 1 < len(linhas):
                prox = linhas[i + 1].strip()
                if prox and not prox.startswith((">", "#", "//", "::")):
                    letra = prox
                    i += 1
            blocos.append(("BLOCO", acorde, letra))
            i += 1
            continue

        blocos.append(("LETRA", linha))
        i += 1

    # Exibição dos blocos formatados
    for bloco in blocos:
        if bloco[0] == "SECAO":
            st.markdown(f"**{bloco[1]}**")
        elif bloco[0] == "BLOCO":
            st.markdown(f"```text\n{bloco[1]}\n{bloco[2]}\n```")
        elif bloco[0] == "LETRA":
            st.markdown(bloco[1])
