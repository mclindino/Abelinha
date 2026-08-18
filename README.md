# Explorador de Assinaturas Químicas do Mel

Aplicação web desenvolvida em Streamlit para análise exploratória e redução de dimensionalidade de dados de espectroscopia no infravermelho de amostras de mel (abelhas Jataí e Mandaçaia).

## Funcionalidades

* **Redução de Dimensionalidade:** Implementa Análise de Componentes Principais (PCA) e Uniform Manifold Approximation and Projection (UMAP).
* **Visualização:** Gráficos de dispersão em 2D e 3D gerados com Matplotlib.
* **Filtragem Espectral:** Recorte dinâmico da faixa de frequência (650 a 4000 cm⁻¹).
* **Agrupamento Dinâmico:** Separação e coloração de dados baseada em Dia de Coleta, Espécie da Abelha ou Índice do Produtor.
* **Personalização de Gráficos:** Controle em tempo real sobre títulos, rótulos dos eixos, tamanho da figura, cores dos agrupamentos e ângulos de visualização (elevação e azimute em 3D).
* **Exportação:** Download direto dos gráficos processados em formato PNG de alta resolução.

## Estrutura do Projeto

A execução correta depende da seguinte estrutura de diretórios:

```text
├── app.py                  # Interface principal do Streamlit
├── README.md
├── src/
│   ├── config.py           # Definição de constantes (ex: DATA_DIR, SEED)
│   ├── data.py             # Lógica de leitura e tratamento dos arquivos Excel (.xlsx)
│   ├── run_pca.py          # Módulo de execução e plotagem do PCA
│   ├── run_umap.py         # Módulo de execução e plotagem do UMAP
│   └── utils.py            # Funções utilitárias (ex: formatação de rótulos)
└── data/                   # Diretório apontado pelo config.DATA_DIR
    ├── jatai_infravermelho.xlsx
    └── mandacaia_infravermelho.xlsx