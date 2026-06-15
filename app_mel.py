import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Explorador de Mel Jataí", layout="wide")

st.title("🍯 Explorador de Assinaturas Químicas do Mel")

st.markdown("""
Este painel transforma os espectros de infravermelho (FTIR) das amostras de mel em visualizações interativas.

### 📉 PCA (Análise de Componentes Principais)
Resume os dados preservando as maiores variações globais entre as amostras. 
* **Configuração:** Não há parâmetros para alterar.

### 🌌 UMAP (Aproximação e Projeção de Variedades Uniformes)
Uma técnica não-linear, focada em agrupar amostras com assinaturas semelhantes (preservando a vizinhança local). O UMAP possue 3 parâmetros principais:

* **`n_neighbors` (Número de Vizinhos):** Valores baixos focam em separar detalhes finos e pequenos grupos. Valores mais altos forçam o algoritmo a focar no panorama geral.
* **`metric` (Métrica de Distância):** Recomenda-se manter em **Cosseno**. Aavalia o *formato* das bandas, ignorando ruídos de linha de base.
* **`min_dist` (Distância Mínima):** Controla a dispersão dos pontos. Recomenda-se manter o **0.1**.

---
**Selecione os parâmetros abaixo para visualizar como as amostras se agrupam com base na sua composição química.**
""")

opcoes_freq = [
    "Todas", "3800_3015", "3015_2450", 
    "1770_1530", "1520_1200", "1500_700", "1200_905", "905_700"
]



col1, col2, col3, col4 = st.columns(4)

with col1:
    abelha_selecionada = st.selectbox("Abelhinha:", ['Jataí', 'Mandaçaia', 'Ambas'])

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
        metrica_selecionada = st.selectbox("Métrica de Comparação:", ['Cosseno', 'Euclidiano'])
        metrica_selecionada = 'cosine' if metrica_selecionada == 'Cosseno' else 'euclidean'
    with col_umap2:
        if abelha_selecionada == 'Ambas':
            nn_selecionado = st.selectbox("Tamanho da Vizinhança (N):", [5, 7, 10, 15])
        else:
            nn_selecionado = st.selectbox("Tamanho da Vizinhança (N):", [3, 4, 5])

    with col_umap3:
        md_selecionado = st.selectbox("Espalhamento (Min Dist):", [0.1, 0.8])

opcoes_agrupamento = ["Produtor", "Coleta"]
if abelha_selecionada == 'Ambas':
    opcoes_agrupamento.append("Bee")

agrupamento_selecionado = st.radio("Se for salvar a imagem, agrupar por:", opcoes_agrupamento, horizontal=True)

st.divider()

if abelha_selecionada != 'Ambas':
    
    if not st.toggle("Resultado PCA/UMAP"):
        if not st.toggle("Salvar Imagem"):
            nome_arquivo = f"graficos/{abelha_selecionada}/Frequencias_visualizacao.html"
            
            if os.path.exists(nome_arquivo):
                with open(nome_arquivo, 'r', encoding='utf-8') as f:
                    html_data = f.read()
                
                components.html(html_data, height=800)
            else:
                st.error(f"⚠️ Gráfico não encontrado! O arquivo procurado foi: {nome_arquivo}")
                st.info("Verifique se você gerou essa combinação específica ou se a pasta 'graficos' está no lugar certo.")
        else:
            nome_arquivo = f"graficos/{abelha_selecionada}/Frequencias_salvar.html"
            
            if os.path.exists(nome_arquivo):
                with open(nome_arquivo, 'r', encoding='utf-8') as f:
                    html_data = f.read()
                
                components.html(html_data, height=800)
            else:
                st.error(f"⚠️ Gráfico não encontrado! O arquivo procurado foi: {nome_arquivo}")
                st.info("Verifique se você gerou essa combinação específica ou se a pasta 'graficos' está no lugar certo.")
        
        #st.divider()
    
    else:
        if metodo_selecionado == 'PCA':
            if not st.toggle("Salvar Imagem"):
                nome_arquivo = f"graficos/{abelha_selecionada}/PCA_{dim}_{freq_selecionada}_visualizar.html"
            else:
                nome_arquivo = f"graficos/{abelha_selecionada}/PCA_{dim}_{freq_selecionada}_{agrupamento_selecionado}_salvar.html"
        else:
            if not st.toggle("Salvar Imagem"):
                nome_arquivo = f"graficos/{abelha_selecionada}/UMAP_{dim}_{freq_selecionada}_{metrica_selecionada}_nn{nn_selecionado}_md{md_selecionado}_visualizar.html"
            else:
                nome_arquivo = f"graficos/{abelha_selecionada}/UMAP_{dim}_{agrupamento_selecionado}_{freq_selecionada}_{metrica_selecionada}_nn{nn_selecionado}_md{md_selecionado}_salvar.html"
        
        if os.path.exists(nome_arquivo):
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                html_data = f.read()
            
            components.html(html_data, height=850)
        else:
            st.error(f"⚠️ Gráfico não encontrado! O arquivo procurado foi: {nome_arquivo}")
            st.info("Verifique se você gerou essa combinação específica ou se a pasta 'graficos' está no lugar certo.")
else:
    if metodo_selecionado == 'PCA':
        if not st.toggle("Salvar Imagem"):
            nome_arquivo = f"graficos/{abelha_selecionada}/PCA_{dim}_{freq_selecionada}_visualizar.html"
        else:
            nome_arquivo = f"graficos/{abelha_selecionada}/PCA_{dim}_{freq_selecionada}_{agrupamento_selecionado}_salvar.html"
    else:
        if not st.toggle("Salvar Imagem"):
            nome_arquivo = f"graficos/{abelha_selecionada}/UMAP_{dim}_{freq_selecionada}_{metrica_selecionada}_nn{nn_selecionado}_md{md_selecionado}_visualizar.html"
        else:
            nome_arquivo = f"graficos/{abelha_selecionada}/UMAP_{dim}_{agrupamento_selecionado}_{freq_selecionada}_{metrica_selecionada}_nn{nn_selecionado}_md{md_selecionado}_salvar.html"
            
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            html_data = f.read()
        
        components.html(html_data, height=850)
    else:
        st.error(f"⚠️ Gráfico não encontrado! O arquivo procurado foi: {nome_arquivo}")
        st.info("Verifique se você gerou essa combinação específica ou se a pasta 'graficos' está no lugar certo.")
