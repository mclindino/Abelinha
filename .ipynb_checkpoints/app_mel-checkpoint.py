import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Explorador de Mel Jataí", layout="wide")

st.title("🍯 Explorador de Assinaturas Químicas do Mel")
st.markdown("Selecione os parâmetros abaixo para visualizar como as amostras se agrupam com base na sua composição química (FTIR).")

opcoes_freq = [
    "Todas", "3800_3015", "3015_2450", 
    "1770_1530", "1520_1200", "1200_905", "905_700"
]

col1, col2, col3, col4 = st.columns(4)

with col1:
    abelha_selecionada = st.selectbox("Abelhinha:", ['Jataí', 'Mandaçaia'])

with col2:
    metodo_selecionado = st.selectbox("Método de Análise:", ['PCA', 'UMAP'])

with col3:
    dim = st.selectbox("Dimensões:", ['2D', '3D'])

with col4:
    freq_selecionada = st.selectbox("Faixa de Frequência (cm⁻¹):", opcoes_freq)

if metodo_selecionado == 'UMAP':
    st.markdown("#### Configurações Avançadas do UMAP")
    
    col_umap1, col_umap2, col_umap3 = st.columns(3)
    
    with col_umap1:
        metrica_selecionada = st.selectbox("Métrica de Comparação:", ['cosine', 'euclidean'])

    with col_umap2:
        nn_selecionado = st.selectbox("Tamanho da Vizinhança (N):", [3, 4, 5])

    with col_umap3:
        md_selecionado = st.selectbox("Espalhamento (Min Dist):", [0.1, 0.8])

st.divider() 

if metodo_selecionado == 'PCA':
    nome_arquivo = f"graficos/{abelha_selecionada}/PCA_{dim}_{freq_selecionada}.html"
else:
    nome_arquivo = f"graficos/{abelha_selecionada}/UMAP_{dim}_{freq_selecionada}_{metrica_selecionada}_nn{nn_selecionado}_md{md_selecionado}.html"

if os.path.exists(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        html_data = f.read()
    
    components.html(html_data, height=850)
else:
    st.error(f"⚠️ Gráfico não encontrado! O arquivo procurado foi: {nome_arquivo}")
    st.info("Verifique se você gerou essa combinação específica ou se a pasta 'graficos' está no lugar certo.")
