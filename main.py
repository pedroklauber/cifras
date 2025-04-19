import streamlit as st
import os
import re

# ---------- CONFIGURAÇÃO ----------
st.set_page_config(page_title="Cifras de Louvor", layout="centered")

st.markdown("""
    <style>
        .titulo {
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 1em;
        }
        .cifra-box {
            font-family: monospace;
            font-size: 15px;
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            white-space: pre-wrap;
            line-height: 1.6;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .acorde {
            color: #1a5dcc;
            font-weight: bold;
        }
        .copiado {
            color: green;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- FUNÇÕES ----------
def linha_so_de_acordes(linha):
    tokens = re.split(r'\s+', linha.strip())
    if not tokens:
        return False
    return all(re.fullmatch(r'[A-G][#b]?(m|maj|min|sus|dim|aug|add)?\d*(/[A-G][#b]?)?', t) for t in tokens if t)

def destacar_linha_de_acordes(linha):
    tokens = re.split(r'(\s+)', linha)  # separa mantendo espaços
    linha_formatada = ''
    for token in tokens:
        if re.fullmatch(r'[A-G][#b]?(m|maj|min|sus|dim|aug|add)?\d*(/[A-G][#b]?)?', token):
            linha_formatada += f'<span class="acorde">{token}</span>'
        else:
            linha_formatada += token.replace(' ', '&nbsp;')
    return linha_formatada

def formatar_cifra_html(cifra_texto):
    linhas = cifra_texto.strip().split('\n')
    saida_html = ''
    for linha in linhas:
        if linha_so_de_acordes(linha):
            saida_html += destacar_linha_de_acordes(linha) + '<br>'
        else:
            saida_html += linha.replace(' ', '&nbsp;') + '<br>'
    return saida_html

# ---------- ARQUIVOS ----------
PASTA_CIFRAS = "cifras"
arquivos = [f for f in os.listdir(PASTA_CIFRAS) if f.endswith(".txt")]
titulos = [f.replace(".txt", "").replace("-", " ").title() for f in arquivos]

# ---------- UI ----------
st.markdown('<div class="titulo">🎼 Selecione uma música:</div>', unsafe_allow_html=True)
selecionada = st.selectbox("Músicas disponíveis", titulos)

# Carregar cifra selecionada
arquivo = arquivos[titulos.index(selecionada)]
with open(os.path.join(PASTA_CIFRAS, arquivo), 'r', encoding='utf-8') as f:
    cifra_texto = f.read()

# Gerar HTML da cifra
html_formatado = formatar_cifra_html(cifra_texto)

# Exibir cifra formatada
st.markdown(f'<div class="cifra-box">{html_formatado}</div>', unsafe_allow_html=True)

# HTML bruto para cópia
with st.expander("🔧 Mostrar código HTML gerado"):
    st.code(html_formatado, language='html')
