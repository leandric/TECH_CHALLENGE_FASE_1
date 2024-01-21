import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Desempenho Historico",
    page_icon="",
    layout="wide",
    initial_sidebar_state="auto",
)

df = st.session_state['dataframe'].copy()


st.header('Desempenho Historico', divider=True)
col1, col2, col3 = st.columns(3)

with col1:
    start_time = st.slider(
    "Período",
    value=(datetime(2004, 1, 1, 9, 30),(datetime(2019, 1, 1, 9, 30))),
    format="YYYY")
    periodo = [start_time[0].year, start_time[1].year]
    periodo = [x for x in range(periodo[0], periodo[1]+1)]

with col2:
    filtro = df['Ano'].isin(periodo)

    df_filtered = df[filtro].copy()
    continente = st.multiselect('Continente', options= df_filtered['Continente'].unique(), default='Europa')
    

with col3:
    filtro = df_filtered['Continente'].isin(continente)
    df_filtered = df_filtered[filtro]
    pais = st.multiselect('País', options=df_filtered['País'].unique())

# Criando uma tabela dinâmica (pivot_table)

filtro = df_filtered['País'].isin(pais)
df_filtered = df_filtered[filtro].copy()

pivot_df = df_filtered.pivot_table(index=['Continente', 'Ano'], columns='Tipo', values='Litros', aggfunc='sum', fill_value=0)

# Reorganizando as colunas conforme o layout desejado
pivot_df = pivot_df[['Vinho de Mesa', 'Suco', 'Espumantes', 'Uva']]

# Resetando o índice para torná-lo em colunas
pivot_df = pivot_df.reset_index()
pivot_df['Ano'] = pivot_df['Ano'].astype(str)
pivot_df