import streamlit as st
from tabs.textos import textos_desempenho_hist
from datetime import datetime
import plotly.express as px
import pandas as pd

def transform(df):
    df['Ano'] = df['Ano'].astype(str)
    filtro = df['Dolares'] != 0
    df = df[filtro].copy()
    return df

# ==================== Filtros ====================
def filter_periodo(df):
    start_time = st.slider(
    "Período",
    value=(datetime(2004, 1, 1, 9, 30),(datetime(2019, 1, 1, 9, 30))),
    format="YYYY")
    periodo = [start_time[0].year, start_time[1].year]
    periodo = [str(x) for x in range(periodo[0], periodo[1]+1)]
    filtro = df['Ano'].isin(periodo)
    df_filtered = df[filtro].copy()
    return df_filtered

def filter_continente(df):
    continentes = df['Continente'].unique()
    continentes = list(continentes)
    continentes.append('Todos')
    continente = st.multiselect('Continente', options= continentes, default='Todos')

    if 'Todos' in continente or continente ==None:
        return df
    else:
        filtro = df['Continente'].isin(continente)
        df_filtered = df[filtro].copy()
        return df_filtered

def filter_pais(df):
    paises = df['País'].unique()
    paises = list(paises)
    paises.append('Todos')
    pais = st.multiselect('País', options=paises, default='Todos')

    if 'Todos' in pais or pais == None:
        return df
    else:
        filtro = df['País'].isin(pais)
        df_filtered = df[filtro].copy()
        return df_filtered
    
def filter_uva(df):
    excluir_uva = st.toggle('Remover Unidade Quilos (Uva)', value=True)
    if excluir_uva:
        filtro = df['Tipo'] != 'Uva'
        df_filtered = df[filtro].copy()
        return df_filtered, excluir_uva
    else:
        return df, excluir_uva
# ==================== Tabelas ====================
def table_pivot(df, filtro_uva_ativo):
    # Obtendo os valores únicos da coluna 'Tipo'
    tipos_unicos = df['Tipo'].unique()
    df.rename(columns={'Dolares': 'Valor $', 'Litros': 'Litros'}, inplace=True)

    # Pivotando o DataFrame
    pivot_df = df.pivot_table(index=['Ano', 'Continente', 'País'], columns='Tipo', values=['Litros', 'Valor $'], aggfunc='sum', fill_value=0)

    # Resetando o índice
    pivot_df.reset_index(inplace=True)

    # Corrigindo o nome das colunas
    pivot_df.columns = [f'{col[0]} ({col[1]})' if col[1] else col[0] for col in pivot_df.columns]
    pivot_df['Ano'] = pivot_df['Ano'].astype(str)

    if filtro_uva_ativo:
        pivot_df.rename(columns={'Litros (Espumantes)': 'Espumante (L)',
                                        'Valor $ (Espumantes)':'Espumante ($)',
                                        'Litros (Suco)': 'Suco (L)',
                                        'Valor $ (Suco)':'Suco ($)',
                                        'Litros (Vinho de Mesa)': 'Vinho de Mesa (L)',
                                        'Valor $ (Vinho de Mesa)':'Vinho de Mesa ($)'}, inplace=True)

        ordem_de_colunas = ['Ano', 'Continente', 'País',
                                        'Espumante (L)',
                                        'Espumante ($)',
                                        'Suco (L)',
                                        'Suco ($)',
                                        'Vinho de Mesa (L)',
                                        'Vinho de Mesa ($)']
        # Calculando os totais
        total = pivot_df.sum(axis=0)
        total['País'] = '-'
        total['Continente'] = '-'
        total['Ano'] = 'Total'
        pivot_df = pd.concat([pd.DataFrame(total).transpose(), pivot_df], ignore_index=True)



        return [pivot_df, ordem_de_colunas]        

    else:
        pivot_df.rename(columns={'Litros (Espumantes)': 'Espumante (L)',
                                        'Valor $ (Espumantes)':'Espumante ($)',
                                        'Litros (Suco)': 'Suco (L)',
                                        'Valor $ (Suco)':'Suco ($)',
                                        'Litros (Vinho de Mesa)': 'Vinho de Mesa (L)',
                                        'Valor $ (Vinho de Mesa)':'Vinho de Mesa ($)',
                                        'Litros (Uva)':'Uva (Kg)',
                                        'Valor $ (Uva)':'Uva ($)'}, inplace=True)
        
        ordem_de_colunas = ['Ano', 'Continente', 'País',
                                        'Espumante (L)',
                                        'Espumante ($)',
                                        'Suco (L)',
                                        'Suco ($)',
                                        'Vinho de Mesa (L)',
                                        'Vinho de Mesa ($)',
                                        'Uva (Kg)',
                                        'Uva ($)']
        # Calculando os totais
        total = pivot_df.sum(axis=0)
        total['País'] = '-'
        total['Continente'] = '-'
        total['Ano'] = 'Total'

        pivot_df = pd.concat([pd.DataFrame(total).transpose(), pivot_df], ignore_index=True)


        return [pivot_df, ordem_de_colunas]


# ==================== Graficos ====================
def graph_litros_anual(df):
    df_soma = df.groupby(['Ano', 'Tipo'])['Litros'].sum().reset_index()

    # Dividir os valores por 1000
    df_soma['Litros'] = df_soma['Litros'] / 1000

    # Arredondar os valores para uma casa decimal
    df_soma['Litros'] = round(df_soma['Litros'], 1)

    # Criar gráfico de linha com Plotly Express
    fig = px.line(df_soma, x='Ano', y='Litros', color='Tipo',
                labels={'Litros': 'Soma dos Litros (em milhares)', 'Ano': 'Ano'},
                hover_data={'Litros': ':,.1f'}, hover_name='Tipo')
    
    return fig

def graph_receita_anual(df):
    df_soma = df.groupby(['Ano', 'Tipo'])['Valor $'].sum().reset_index()

    # Dividir os valores por 1000
    df_soma['Valor $'] = df_soma['Valor $'] / 1000

    # Arredondar os valores para uma casa decimal
    df_soma['Valor $'] = round(df_soma['Valor $'], 1)

    # Criar gráfico de linha com Plotly Express
    fig = px.line(df_soma, x='Ano', y='Valor $', color='Tipo',
                labels={'Valor $': 'Valor $ (em milhares)', 'Ano': 'Ano'},
                hover_data={'Valor $': ':,.1f'}, hover_name='Tipo')
    
    return fig



def graph_continente_litros(df):
    mapeamento = {
        'África':'Africa',
        'Ásia':'Asia',
        'Europa':'Europe',
        'Oceania':'Oceania',
        'América do Norte':'North America',
        'América do Sul':'South America',
        'Europa/Ásia':'Europe'
    }

    #df['Continente'] = df['Continente'].map(mapeamento)

    df_grouped = df.groupby('Continente')['Litros'].sum().reset_index()

    # Plotar o gráfico de mapa
    fig = px.choropleth(df_grouped, 
                        locations='Continente', 
                        locationmode='country names',
                        color='Litros',
                        hover_name='Continente',
                        color_continuous_scale='Viridis',
                        title='Soma de Litros por Continente')
    st.plotly_chart(fig)



def main():
    df = transform(st.session_state['dataframe'].copy())
    st.image('tabela_6.png')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        df = filter_periodo(df)
    with col2:
        df = filter_continente(df)
    with col3:
        df = filter_pais(df)
    with col4:
        df, filtro_uva_ativo = filter_uva(df)

    col1, col2 = st.columns(2)



    st.markdown('### Tabela de Comparação')
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(table_pivot(df, filtro_uva_ativo)[0], hide_index=True, column_order=table_pivot(df, filtro_uva_ativo)[1])
    with col2:
        st.markdown(textos_desempenho_hist.text_lateral)

    st.markdown('')
    st.markdown('')
    st.markdown('')

    st.markdown(textos_desempenho_hist.grafico_titulo_global, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(textos_desempenho_hist.grafico1, unsafe_allow_html=True)
        st.plotly_chart(graph_litros_anual(df))

    with col2:
        st.markdown(textos_desempenho_hist.grafico2, unsafe_allow_html=True)
        st.plotly_chart(graph_receita_anual(df))