import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.express as px
from textos import *



def grafico1(df_filtered):
    df_soma = df_filtered.groupby(['Ano', 'Tipo'])['Litros'].sum().reset_index()

    # Criar gráfico de linha com Plotly Express
    fig = px.line(df_soma, x='Ano', y='Litros', color='Tipo',
                labels={'Litros': 'Soma dos Litros', 'Ano': 'Ano'})
    
    return fig

def main():

    df = st.session_state['dataframe'].copy()


    st.header('Desempenho Historico', divider=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        excluir_uva = st.toggle('Remover Uva', value=True)
        df_filtered = df.copy()
        filtro_uva = df_filtered['Tipo'] != 'Uva'
        if excluir_uva:
            df_filtered = df_filtered[filtro_uva].copy()

    with col2:
        start_time = st.slider(
        "Período",
        value=(datetime(2004, 1, 1, 9, 30),(datetime(2019, 1, 1, 9, 30))),
        format="YYYY")
        periodo = [start_time[0].year, start_time[1].year]
        periodo = [x for x in range(periodo[0], periodo[1]+1)]

    with col3:
        filtro_ano = df_filtered['Ano'].isin(periodo)

        df_filtered = df_filtered[filtro_ano].copy()
        continente = st.multiselect('Continente', options= df_filtered['Continente'].unique(), default='Europa')
        

    with col4:
        filtro_continente = df_filtered['Continente'].isin(continente)
        df_filtered = df_filtered[filtro_continente]
        paises = df_filtered['País'].unique()
        paises = list(paises)
        paises.append('Todos')
        pais = st.multiselect('País', options=paises, default='Todos')

    # Criando uma tabela dinâmica (pivot_table)
        
    if 'Todos' in pais or pais == None:
        pass
    else:
        filtro = df_filtered['País'].isin(pais)
        df_filtered = df_filtered[filtro].copy()

    # Obtendo os valores únicos da coluna 'Tipo'
    tipos_unicos = df_filtered['Tipo'].unique()

    # Pivotando o DataFrame
    pivot_df = df_filtered.pivot_table(index=['Ano', 'Continente', 'País'], columns='Tipo', values=['Litros', 'Dolares'], aggfunc='sum', fill_value=0)

    # Resetando o índice
    pivot_df.reset_index(inplace=True)

    # Corrigindo o nome das colunas
    pivot_df.columns = [f'{col[0]} ({col[1]})' if col[1] else col[0] for col in pivot_df.columns]
    pivot_df['Ano'] = pivot_df['Ano'].astype(str)

    #============================================== Pagina =========================================================

    st.markdown('### Tabela de Comparação')
    st.dataframe(pivot_df, hide_index=True)
    st.markdown(info_uva)
    col1, col2 = st.columns(2)

    with col1:
            
        # Calcular a soma dos litros por ano e tipo
        df_filtered = st.session_state['dataframe'].copy()

            #=============================== Uva ==========================================
        if excluir_uva:
            df_filtered = df_filtered[filtro_uva].copy()

        # Aplica os Filtros =========================================================
            # =========================== Ano ===========================================
        df_filtered = df_filtered[filtro_ano].copy()

            # =========================== Continente ===========================================
        df_filtered = df_filtered[filtro_continente]

            # ============================== País ============================================
        if 'Todos' in pais or pais == None:
            pass
        else:
            filtro = df_filtered['País'].isin(pais)
            df_filtered = df_filtered[filtro].copy()


        st.markdown(titulo_grafico1_desempenho, unsafe_allow_html=True)
        



        st.plotly_chart(grafico1(df_filtered))

    with col2:
        # Calcular a soma dos litros por ano e tipo
        df_filtered = st.session_state['dataframe'].copy()

            #=============================== Uva ==========================================
        if excluir_uva:
            df_filtered = df_filtered[filtro_uva].copy()

        # Aplica os Filtros =========================================================
            # =========================== Ano ===========================================
        df_filtered = df_filtered[filtro_ano].copy()

            # =========================== Continente ===========================================
        df_filtered = df_filtered[filtro_continente]

            # ============================== País ============================================
        if 'Todos' in pais or pais == None:
            pass
        else:
            filtro = df_filtered['País'].isin(pais)
            df_filtered = df_filtered[filtro].copy()

        st.markdown(titulo_grafico1_desempenho2, unsafe_allow_html=True)
        st.plotly_chart(grafico1(df_filtered))