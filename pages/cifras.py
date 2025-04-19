import streamlit as st
import os
import pathlib

# Caminho
PASTA_CIFRAS = pathlib.Path(__file__).parent / "cifras"
os.makedirs(PASTA_CIFRAS, exist_ok=True)

# Arquivos disponíveis
arquivos = [f for f in os.listdir(PASTA_CIFRAS) if f.endswith(".txt")]
titulos = [f.replace(".txt", "").replace("-", " ").title() for f in arquivos]

if not arquivos:
    st.warning("Nenhuma cifra encontrada na pasta 'cifras'. Adicione arquivos .txt.")
    st.stop()

# Seleção
st.markdown("###  Louvores Seleção")
selecionada = st.selectbox("Escolha a música:", titulos)
arquivo = arquivos[titulos.index(selecionada)]

# Estilo HTML seguro para fundo escuro/claro
st.markdown("""
    <style>
        .cifra {
            font-family: monospace;
            font-size: 15px;
            background-color: var(--background-color);
            color: var(--text-color);
            padding: 20px;
            border-radius: 8px;
            white-space: pre-wrap;
            line-height: 1.6;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .acorde {
            font-weight: bold;
            color: #3d8eff;
        }
        .secao {
            font-weight: bold;
            color: #999;
        }
        @media (prefers-color-scheme: dark) {
            :root {
                --background-color: #1e1e1e;
                --text-color: #f2f2f2;
            }
        }
        @media (prefers-color-scheme: light) {
            :root {
                --background-color: #f9f9f9;
                --text-color: #111;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Leitura do arquivo
with open(PASTA_CIFRAS / arquivo, "r", encoding="utf-8") as f:
    linhas = f.read().splitlines()

# Monta HTML com marcação leve
html = ""
for i, linha in enumerate(linhas):
    linha = linha.strip()

    if not linha or linha.startswith("//"):
        html += "<br>"
        continue

    if linha.startswith("#"):
        html += f'<div class="secao">{linha[1:].strip()}</div><br>'
    elif linha.startswith(">"):
        acorde = linha[1:].replace(" ", "&nbsp;")
        html += f'<span class="acorde">{acorde}</span><br>'
    else:
        letra = linha.replace(" ", "&nbsp;")
        html += letra + "<br>"

# Exibir
st.markdown(f'<div class="cifra">{html}</div>', unsafe_allow_html=True)
