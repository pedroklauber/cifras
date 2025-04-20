import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Cifras por Categoria", layout="wide")

# Mantém a tela ativa em dispositivos compatíveis
components.html("""
<script>
let wakeLock = null;

async function requestWakeLock() {
  try {
    wakeLock = await navigator.wakeLock.request('screen');
    wakeLock.addEventListener('release', () => {
      console.log('Wake Lock liberado');
    });
    console.log('Wake Lock ativo!');
  } catch (err) {
    console.error(`${err.name}, ${err.message}`);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  if ('wakeLock' in navigator) {
    requestWakeLock();
  } else {
    console.warn('Wake Lock API não suportada');
  }
});
</script>
""", height=0)


import os
import pathlib

# Caminhos
BASE_DIR = pathlib.Path(__file__).parent
PASTA_CIFRAS = BASE_DIR / "cifras"
ARQUIVO_LISTA = BASE_DIR / "lista.txt"
os.makedirs(PASTA_CIFRAS, exist_ok=True)

# Categorias
#categorias = ["Clássico", "Libertação", "Festivo", "Oração", "Adoração"]
categorias = ["Quarta", "Domingo"]
cifras_por_categoria = {cat: [] for cat in categorias}

# Verifica lista.txt
if not ARQUIVO_LISTA.exists():
    st.warning("Arquivo 'lista.txt' não encontrado.")
    st.stop()

# Lê a lista
with open(ARQUIVO_LISTA, "r", encoding="utf-8") as f:
    for linha in f:
        if "|" not in linha:
            continue
        titulo, categoria, arquivo = [x.strip() for x in linha.strip().split("|")]
        if categoria in cifras_por_categoria:
            cifras_por_categoria[categoria].append((titulo, arquivo))

# Estilo HTML (fundo adaptável)
st.markdown("""
    <style>
        .cifra {
            font-family: monospace;
            font-size: 13px;
            background-color: var(--background-color);
            color: var(--text-color);
            padding: 10px;
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

# Título da página
st.markdown("## Cifras por Estilo")

# Colunas por categoria
colunas = st.columns(len(categorias))
for i, cat in enumerate(categorias):
    with colunas[i]:
        st.markdown(f"### {cat}")
        for titulo, arquivo in cifras_por_categoria[cat]:
            if st.button(titulo, key=f"{cat}-{titulo}"):
                st.session_state["cifra_selecionada"] = (titulo, arquivo)

# Exibe cifra selecionada com estilo HTML
if "cifra_selecionada" in st.session_state:
    titulo, arquivo = st.session_state["cifra_selecionada"]
    st.markdown(f"---\n### 📄 {titulo}")

    path = PASTA_CIFRAS / arquivo
    if not path.exists():
        st.error(f"O arquivo '{arquivo}' não foi encontrado na pasta 'cifras'.")
        st.stop()

    with open(path, "r", encoding="utf-8") as f:
        linhas = f.read().splitlines()

    # Processamento estilo visual
    html = ""
    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("//"):
            html += "<br>"
        elif linha.startswith("#"):
            html += f'<div class="secao">{linha[1:].strip()}</div><br>'
        elif linha.startswith(">"):
            html += f'<span class="acorde">{linha[1:].replace(" ", "&nbsp;")}</span><br>'
        else:
            html += linha.replace(" ", "&nbsp;") + "<br>"

    st.markdown(f'<div class="cifra">{html}</div>', unsafe_allow_html=True)
