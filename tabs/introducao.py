import streamlit as st
import matplotlib.pyplot as plt
from tabs.textos import textos_introducao


def transform(df):
    filtro = df['Tipo'] != 'Uva'
    df_filtered = df[filtro].copy()
    df_filtered = df_filtered.query('Ano >= 2004 and Ano <= 2019').copy()
    df_filtered = df_filtered.groupby(['Ano', 'Tipo'])[['Litros']].sum().reset_index().copy()
    total_litros_por_ano = df_filtered.groupby('Ano')['Litros'].sum() # Calcular a soma total de litros por ano
    df_filtered['Percentual'] = df_filtered.apply(lambda row: (row['Litros'] / total_litros_por_ano[row['Ano']]) * 100 if total_litros_por_ano[row['Ano']] != 0 else 0, axis=1)
    return df_filtered

import matplotlib.pyplot as plt

def graphs_anual(df):
    # Filtrando os dados para cada tipo
    espumantes_data = df[df['Tipo'] == 'Espumantes']
    suco_data = df[df['Tipo'] == 'Suco']
    vinho_data = df[df['Tipo'] == 'Vinho de Mesa']

    # Criando gráficos de barras para cada tipo com cores personalizadas
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))

    # Configurações gerais
    bar_width = 0.8
    colors = ['#8C8D90', '#A5A6AA', '#B7B8BC']

    for ax, data, title, color in zip(axes, [espumantes_data, suco_data, vinho_data], ['Espumantes', 'Suco', 'Vinho de Mesa'], colors):
        bars = ax.bar(data['Ano'], data['Percentual'], color=color, width=bar_width)
        ax.set_title(title)
        
        # Adicionando rótulos nas barras
        for bar, label in zip(bars, data['Percentual']):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{label:.2f}%', ha='center', va='bottom')

        # Adicionando rótulos aos eixos
        ax.set_xlabel('Ano')
        ax.set_ylabel('Percentual (%)')

        # Definindo os limites da escala do eixo y
        ax.set_ylim(0, 100)

        # Adicionando legendas
        ax.legend(['Percentual'])

    # Ajustando o layout
    plt.tight_layout()
    return fig


def main():
    df = transform(st.session_state['dataframe'].copy())
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('## Objetivo')
        st.markdown(textos_introducao.introducao)
        st.image('capa.jpg')

    with col2:
        st.markdown(textos_introducao.grafico_introducao, unsafe_allow_html=True)
        st.pyplot(graphs_anual(df))
        st.markdown(textos_introducao.texto_abaixo_grafico)
    