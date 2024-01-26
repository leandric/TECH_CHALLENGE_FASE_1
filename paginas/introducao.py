import streamlit as st
from textos import *
import pandas as pd
import matplotlib.pyplot as plt



def main():
    # DADOS ======================
    df = st.session_state['dataframe'].copy()
    df = df[df['Continente'] != 'Outros'].copy()

    filtro = df['Tipo'] != 'Uva'
    df_menos_uva = df[filtro].copy()
    del df_menos_uva['Dolares']
    df_menos_uva = df_menos_uva.groupby(['Ano', 'Tipo'])[['Litros']].sum().reset_index().copy()




    # Calcular a soma total de litros por ano
    total_litros_por_ano = df_menos_uva.groupby('Ano')['Litros'].sum()
    df_menos_uva['Percentual'] = df_menos_uva.apply(lambda row: (row['Litros'] / total_litros_por_ano[row['Ano']]) * 100 if total_litros_por_ano[row['Ano']] != 0 else 0, axis=1)


    # Filtrando os dados para o intervalo de 2004 a 2019
    df_filtrado = df_menos_uva.query('Ano >= 2004 and Ano <= 2019')

    # Filtrando os dados para cada tipo
    espumantes_data = df_filtrado[df_filtrado['Tipo'] == 'Espumantes']
    suco_data = df_filtrado[df_filtrado['Tipo'] == 'Suco']
    vinho_data = df_filtrado[df_filtrado['Tipo'] == 'Vinho de Mesa']

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

        # Adicionando legendas
        ax.legend(['Percentual'])

    # Ajustando o layout
    plt.tight_layout()







    #LAYOUT ===========================
    st.markdown('# Objetivo')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(introducao)
        st.image('https://i0.wp.com/www.wine.com.br/winepedia/wp-content/uploads/2022/04/181788-post-de-3000-descubra-x-uvas-para-vinhos-que-voce-nao-conhecia.jpg')
        
    with col2:
        st.markdown(texto_grafico_introducao, unsafe_allow_html=True)
        st.pyplot(fig)
