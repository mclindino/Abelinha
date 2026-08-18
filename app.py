import io
import streamlit as st

from src.run_pca import main as run_pca_main
from src.run_umap import main as run_umap_main

st.set_page_config(page_title="Explorador de Mel", layout="wide")

if "fig" not in st.session_state:
    st.session_state.fig = None
    st.session_state.n_groups = 0

# --- BARRA LATERAL ESQUERDA (Configurações do Modelo) ---
with st.sidebar:
    st.header("Parâmetros da Análise")
    
    abelha_selecionada = st.selectbox("Abelha:", ['Jataí', 'Mandaçaia', 'Ambas'])
    bee_map = {'Jataí': 'jatai', 'Mandaçaia': 'mandacaia', 'Ambas': 'ambas'}
    bee_val = bee_map[abelha_selecionada]

    metodo_selecionado = st.selectbox("Método de Análise:", ['PCA', 'UMAP'])
    
    dim = st.radio("Dimensões:", ['2D', '3D'], horizontal=True)
    dim_val = 2 if dim == '2D' else 3

    agrupar_por = st.selectbox("Agrupar dados por:", ['Dia', 'Abelha', 'Produtor'])
    group_map = {'Dia': 'Collection_day', 'Abelha': 'Bee', 'Produtor': 'Producer_idx'}
    group_val = group_map[agrupar_por]

    prefixo_marcador = st.text_input("Prefixo no ponto (antes do IDX):", value="Produtor ")

    st.markdown("---")
    st.subheader("Frequência (cm⁻¹)")
    lim_inf, lim_sup = st.slider(
        "Limites espectrais:", 
        min_value=650, 
        max_value=4000, 
        value=(650, 4000),
        step=10
    )

    if metodo_selecionado == 'UMAP':
        st.markdown("---")
        st.subheader("Configurações UMAP")
        
        metrica_selecionada = st.selectbox("Métrica:", ['cosine', 'correlation', 'euclidean', 'manhattan'])
        
        max_nn = 15 if abelha_selecionada == 'Ambas' else 7
        nn_selecionado = st.slider("n_neighbors:", min_value=2, max_value=max_nn, value=3)
        
        md_selecionado = st.slider("min_dist:", min_value=0.0, max_value=0.99, value=0.10, step=0.05)

    st.markdown("---")
    executar = st.button("Executar Análise", type="primary")
    download_placeholder = st.empty()


# --- EXECUÇÃO BASE ---
if executar:
    with st.spinner("Processando dados..."):
        if metodo_selecionado == 'PCA':
            fig_base = run_pca_main(
                bee=bee_val, 
                limit_lower=lim_inf, 
                limit_upper=lim_sup, 
                dimensions=dim_val,
                marker_prefix=prefixo_marcador,
                group_by=group_val
            )
        else:
            fig_base = run_umap_main(
                bee=bee_val, 
                limit_lower=lim_inf, 
                limit_upper=lim_sup, 
                dimensions=dim_val, 
                n_neighbors=nn_selecionado, 
                min_dist=md_selecionado, 
                metric=metrica_selecionada,
                marker_prefix=prefixo_marcador,
                group_by=group_val
            )
        st.session_state.fig = fig_base
        st.session_state.n_groups = len(fig_base.axes[0].collections)

# --- ÁREA PRINCIPAL DIVIDIDA ---
st.title("Explorador de Assinaturas Químicas do Mel")

col_grafico, col_ferramentas = st.columns([3, 1], gap="large")

# --- MENU À DIREITA ---
with col_ferramentas:
    st.markdown("### 🛠️ Ferramentas do Gráfico")
    largura_cm = st.number_input("Largura (cm):", min_value=10.0, max_value=60.0, value=20.0, step=1.0)
    altura_cm = st.number_input("Altura (cm):", min_value=10.0, max_value=60.0, value=15.0, step=1.0)
    
    st.markdown("#### Textos e Eixos")
    titulo_custom = st.text_input("Título:", value=f"{dim} {metodo_selecionado} - {abelha_selecionada}")
    eixo_x_custom = st.text_input("Eixo X:", value="Componente Principal 1" if metodo_selecionado == 'PCA' else "Componente 1")
    eixo_y_custom = st.text_input("Eixo Y:", value="Componente Principal 2" if metodo_selecionado == 'PCA' else "Componente 2")
    
    eixo_z_custom = ""
    elev = 20
    azim = 45
    if dim_val == 3:
        eixo_z_custom = st.text_input("Eixo Z:", value="Componente Principal 3" if metodo_selecionado == 'PCA' else "Componente 3")
        st.markdown("#### Visão 3D")
        elev = st.slider("Elevação (Eixo Y):", min_value=-90, max_value=90, value=20)
        azim = st.slider("Azimute (Rotação Z):", min_value=-180, max_value=180, value=45)
        
    if st.session_state.fig is not None:
        st.markdown("#### Legenda e Cores")
        titulo_legenda = st.text_input("Título da Legenda:", value=agrupar_por)
        
        ax_temp = st.session_state.fig.axes[0]
        leg_temp = ax_temp.get_legend()
        default_labels = ", ".join([t.get_text() for t in leg_temp.texts]) if leg_temp else ""
        
        rotulos_legenda = st.text_input("Rótulos (separados por vírgula):", value=default_labels)
        
        cores_customizadas = []
        n_groups = st.session_state.n_groups
        c_cols = st.columns(2)
        paleta_default = ["#2A9D8F", "#E76F51", "#E9C46A", "#264653", "#F4A261", "#8D99AE", "#EF233C", "#2B2D42"]
        
        for i in range(n_groups):
            with c_cols[i % 2]:
                cor_sugerida = paleta_default[i % len(paleta_default)]
                cores_customizadas.append(st.color_picker(f"Grupo {i+1}:", cor_sugerida, key=f"cor_{i}"))

# --- APLICAÇÃO VISUAL EM TEMPO REAL E EXIBIÇÃO ---
with col_grafico:
    if st.session_state.fig is not None:
        fig = st.session_state.fig
        
        fig.set_size_inches(largura_cm / 2.54, altura_cm / 2.54)
        ax = fig.axes[0]
        
        ax.set_title(titulo_custom, pad=15)
        ax.set_xlabel(eixo_x_custom, labelpad=10)
        ax.set_ylabel(eixo_y_custom, labelpad=10)
        
        if dim_val == 3:
            if eixo_z_custom:
                ax.set_zlabel(eixo_z_custom, labelpad=10)
            ax.view_init(elev=elev, azim=azim)
            
        for collection, color in zip(ax.collections, cores_customizadas):
            collection.set_facecolor(color)
            collection.set_edgecolor('#333333')

        leg = ax.get_legend()
        if leg:
            handles = leg.legend_handles
            labels_list = [l.strip() for l in rotulos_legenda.split(',')]
            
            for handle, color in zip(handles, cores_customizadas):
                handle.set_facecolor(color)
                handle.set_edgecolor('#333333')
                
            ax.legend(handles=handles, labels=labels_list[:len(handles)], title=titulo_legenda, title_fontsize=12, fontsize=11, loc='best')
        
        st.pyplot(fig, use_container_width=False)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches="tight", transparent=False)
        buf.seek(0)
        
        download_placeholder.download_button(
            label="📥 Baixar Imagem PNG",
            data=buf,
            file_name=f"{metodo_selecionado}_{bee_val}_{lim_inf}_{lim_sup}.png",
            mime="image/png"
        )
    else:
        st.info("Execute a análise no painel à esquerda para gerar o gráfico.")