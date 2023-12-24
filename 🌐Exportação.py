# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import plotly.express as px
from textos import *  # Importando um módulo personalizado chamado "textos"

# Configurações do tema e layout do Streamlit
st.set_page_config(
    page_title="Exportação",
    page_icon="🍷",
    layout="wide",  # ou "centered" para centralizar o conteúdo
    initial_sidebar_state="expanded",  # ou "collapsed"
)

# Definindo o título da barra lateral
st.sidebar.title("Meu Novo Título na Barra Lateral")

# Colunas a serem carregadas no DataFrame
COLUNAS_CARREGAR = ['Ano', 'Tipo', 'País', 'Litros', 'Dolares']

# Carregando o DataFrame diretamente em st.session_state['dados']
st.session_state['dados'] = pd.read_csv('https://raw.githubusercontent.com/leandric/Exportacao-de-Vinho-e-Derivados/main/base_tratada/base_final.csv',
                                        usecols=COLUNAS_CARREGAR)

# Título principal
st.markdown('# Base de exportação')

#-----------------------------------------------------------------------------
# Filtros para o Gráfico 1

# Criando dois contêineres de coluna no Streamlit
col1, col2 = st.columns(2)

# Na primeira coluna (col1), criando um seletor de múltipla escolha para o tipo
with col1:
    _tipos = st.session_state['dados']['Tipo'].unique()
    tipo_selecionado = st.multiselect(label='Tipo', options=_tipos, default=_tipos)

# Na segunda coluna (col2), criando um seletor para o país
with col2:
    _paises = st.session_state['dados']['País'].unique()
    pais_selecionado = st.selectbox(label='País', options=_paises)

# Copiando o DataFrame original para aplicar os filtros
df = st.session_state['dados'].copy()
filtro_global = df['Tipo'].isin(tipo_selecionado)
filtro_pais = (df['Tipo'].isin(tipo_selecionado)) & (df['País'] == pais_selecionado)
df_global = df[filtro_global].copy()
df_pais = df[filtro_pais].copy()

# Agrupando por ano e somando os litros para criar DataFrames globais e por país
df_global = df_global.groupby(['Ano'])['Litros'].sum().reset_index().copy()
df_pais = df_pais.groupby(['Ano'])['Litros'].sum().reset_index().copy()

# Criando gráficos de linha para o DataFrame global e por país
fig = px.line(df_global, x='Ano', y='Litros', markers=True,
              title='Quantidade de Litros Exportados ao Longo dos Anos',
              labels={'Litros': 'Litros Exportados'})

fig2 = px.line(df_pais, x='Ano', y='Litros', markers=True,
               title=f'Quantidade de Litros Exportados ao Longo dos Anos ({pais_selecionado})',
               labels={'Litros': 'Litros Exportados'})

# Exibindo os gráficos no Streamlit, dividindo a tela em duas colunas
col1, col2 = st.columns(2)

col1.plotly_chart(fig)
col2.plotly_chart(fig2)

# Adicionando um bloco de texto abaixo dos gráficos
st.markdown(texto1)
