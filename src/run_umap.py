import argparse
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from umap import UMAP

from .config import *
from .data import read_excel
from .utils import _format_collection_labels

matplotlib.use("Agg")

def main(bee: str, limit_lower: int, limit_upper: int, dimensions: int, n_neighbors: int, min_dist: float, metric: str,
         custom_colors: list = None, custom_title: str = None, 
         custom_xlabel: str = "Componente 1", custom_ylabel: str = "Componente 2", custom_zlabel: str = "Componente 3",
         marker_prefix: str = "Produtor ", group_by: str = "Collection_day"):
    
    df = read_excel(DATA_DIR, bee)

    meta_cols = ['Bee', 'Collection_day', 'Producer_idx']
    freq_cols = [col for col in df.columns if col not in meta_cols]

    if limit_lower > limit_upper:
        raise ValueError('O limite inferior não pode ser maior que o superior.')

    freq_cols = [col for col in freq_cols if limit_lower <= int(col) <= limit_upper]
    filtered_df = df[freq_cols].values

    producer_idx = df['Producer_idx'].astype(str).to_numpy()

    if group_by == 'Collection_day':
        group_array = df['Collection_day'].astype(int).to_numpy()
        unique_groups = np.unique(group_array)
        group_labels = _format_collection_labels(unique_groups)
    elif group_by == 'Bee':
        group_array = df['Bee'].astype(str).to_numpy()
        unique_groups = np.unique(group_array)
        group_labels = [str(g).capitalize() for g in unique_groups]
    elif group_by == 'Producer_idx':
        group_array = df['Producer_idx'].astype(str).to_numpy()
        unique_groups = np.unique(group_array)
        group_labels = [f"{g}" for g in unique_groups]
    else:
        raise ValueError("Agrupamento inválido selecionado.")

    umap = UMAP(n_neighbors=n_neighbors, min_dist=min_dist, metric=metric, n_components=dimensions, random_state=SEED, n_jobs=1)
    umap_result = umap.fit_transform(filtered_df)

    plt.style.use('seaborn-v0_8-paper')
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'axes.titleweight': 'bold',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.frameon': False,
        'figure.facecolor': '#ffffff',
        'axes.facecolor': '#ffffff'
    })

    if custom_colors and len(custom_colors) >= len(unique_groups):
        colors = custom_colors[:len(unique_groups)]
    else:
        colors = ['#2A9D8F', '#E76F51'] 
        if len(unique_groups) > 2:
            colors = plt.cm.Set2(np.linspace(0, 1, len(unique_groups)))

    title_str = custom_title if custom_title else f'{dimensions}D UMAP - {bee.capitalize()}'

    if dimensions == 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        
        for grp, label, color in zip(unique_groups, group_labels, colors):
            idx = group_array == grp
            ax.scatter(
                umap_result[idx, 0],
                umap_result[idx, 1],
                color=color,
                label=label,
                s=80,
                alpha=0.85,
                edgecolors='#333333',
                linewidths=0.8,
            )
            
            for x, y, p_idx in zip(umap_result[idx, 0], umap_result[idx, 1], producer_idx[idx]):
                text_lbl = f"{marker_prefix}{p_idx}"
                ax.annotate(text_lbl, (x, y), textcoords="offset points", xytext=(0, 7), ha='center', fontsize=8, color='#333333', weight='bold')

        ax.legend(title='Grupos', title_fontsize=12, fontsize=11, loc='best')
        ax.set_title(title_str, pad=15)
        ax.set_xlabel(custom_xlabel)
        ax.set_ylabel(custom_ylabel)
        ax.grid(True, linestyle='-', color='#EBEBEB', linewidth=0.7, zorder=0)
        ax.set_axisbelow(True)
        fig.tight_layout()

    elif dimensions == 3:
        fig = plt.figure(figsize=(9, 7))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.xaxis._axinfo["grid"]['color'] = '#EBEBEB'
        ax.yaxis._axinfo["grid"]['color'] = '#EBEBEB'
        ax.zaxis._axinfo["grid"]['color'] = '#EBEBEB'

        for grp, label, color in zip(unique_groups, group_labels, colors):
            idx = group_array == grp
            ax.scatter(
                umap_result[idx, 0],
                umap_result[idx, 1],
                umap_result[idx, 2],
                color=color,
                label=label,
                s=60,
                alpha=0.9,
                edgecolors='#333333',
                linewidths=0.6,
            )
            
            for x, y, z, p_idx in zip(umap_result[idx, 0], umap_result[idx, 1], umap_result[idx, 2], producer_idx[idx]):
                text_lbl = f"{marker_prefix}{p_idx}"
                ax.text(x, y, z + 0.1, text_lbl, size=8, color='#333333', weight='bold', ha='center', va='bottom')

        ax.legend(title='Grupos', title_fontsize=12, fontsize=11, loc='best')
        ax.set_title(title_str, pad=15)
        ax.set_xlabel(custom_xlabel, labelpad=10)
        ax.set_ylabel(custom_ylabel, labelpad=10)
        ax.set_zlabel(custom_zlabel, labelpad=10)
        ax.view_init(elev=20, azim=45)
        fig.tight_layout()
    else:
        raise ValueError('Apenas visualizações UMAP 2D e 3D são suportadas.')

    return fig