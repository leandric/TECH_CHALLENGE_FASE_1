import streamlit as st
from datetime import datetime
import json
import plotly.express as px
import pandas as pd
from tabs.textos import textos_analise_internacional

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
    format="YYYY", key=541351)
    periodo = [start_time[0].year, start_time[1].year]
    periodo = [str(x) for x in range(periodo[0], periodo[1]+1)]
    filtro = df['Ano'].isin(periodo)
    df_filtered = df[filtro].copy()
    return df_filtered

def filter_continente(df):
    continentes = df['Continente'].unique()
    continentes = list(continentes)
    continentes.append('Todos')
    continente = st.multiselect('Continente', options= continentes, default='Todos', key=546512)

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
    pais = st.multiselect('País', options=paises, default='Todos', key=44544)

    if 'Todos' in pais or pais == None:
        return df
    else:
        filtro = df['País'].isin(pais)
        df_filtered = df[filtro].copy()
        return df_filtered
    
def filter_uva(df):
    excluir_uva = st.toggle('Remover Unidade Quilos (Uva)', value=True, key=87489)
    if excluir_uva:
        filtro = df['Tipo'] != 'Uva'
        df_filtered = df[filtro].copy()
        return df_filtered, excluir_uva
    else:
        return df, excluir_uva

#==================== Graficos ========================
def mapa_dolar_continente(df):
    continentes_map = {
        'África': 'Africa',
        'Europa': 'Europe',
        'América do Norte': 'North America',
        'América do Sul': 'South America',
        'Oceania': 'Oceania',
        'Ásia': 'Asia'}
    df_filtered = df.copy()
    df_filtered['continente_key'] = df['Continente'].map(continentes_map)

    df_filtered = df_filtered.groupby(['continente_key'])['Dolares'].sum().reset_index()
    with open('continents.geojson', 'r') as arquivo:
        dados_json = json.load(arquivo)

    fig = px.choropleth(df_filtered, geojson=dados_json, color='Dolares',
                        locations='continente_key', featureidkey='properties.CONTINENT',
                        projection='mercator',
                        labels={'Dolares': 'Dolares'},
                        color_continuous_scale='Reds')  # Escala de cores
    fig.update_geos(fitbounds='geojson', visible=True)
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return fig

def mapa_litro_por_dolar_continente(df):
    continentes_map = {
        'África': 'Africa',
        'Europa': 'Europe',
        'América do Norte': 'North America',
        'América do Sul': 'South America',
        'Oceania': 'Oceania',
        'Ásia': 'Asia'}
    df_filtered = df.copy()
    df_filtered['continente_key'] = df['Continente'].map(continentes_map)

    df_filtered = df_filtered.groupby(['continente_key'])[['Dolares', 'Litros']].sum().reset_index()

    df_filtered['Litro/Dolar'] = df_filtered['Litros'] / df_filtered['Dolares']

    with open('continents.geojson', 'r') as arquivo:
        dados_json = json.load(arquivo)

    fig = px.choropleth(df_filtered, geojson=dados_json, color='Litro/Dolar',
                        locations='continente_key', featureidkey='properties.CONTINENT',
                        projection='mercator',
                        labels={'Litro/Dolar': 'Litro/Dolar'},
                        color_continuous_scale='Reds')  # Escala de cores
    fig.update_geos(fitbounds='geojson', visible=True)
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    return fig

#======================= Tabelas ==========================

def top_dez_paises_dolar(df, filtro_uva_ativo):
    # Agrupar por país e somar os valores
    df_agrupado = df.groupby('País').sum().reset_index()

    if filtro_uva_ativo:
        # Calcular a soma dos dólares para cada país
        df_agrupado['Soma Dolares'] = df_agrupado[['Espumante ($)', 'Suco ($)', 'Vinho de Mesa ($)']].sum(axis=1)

        # Calcular os percentuais de cada tipo de bebida em relação ao total de dólares gastos em bebidas para cada país
        df_agrupado['Percentual Espumantes Dolares'] = (df_agrupado['Espumante ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Suco Dolares'] = (df_agrupado['Suco ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Vinho de Mesa Dolares'] = (df_agrupado['Vinho de Mesa ($)'] / df_agrupado['Soma Dolares']) * 100

        # Selecionar apenas as colunas necessárias
        result_df = df_agrupado[['País', 'Soma Dolares', 'Percentual Espumantes Dolares', 'Percentual Suco Dolares', 'Percentual Vinho de Mesa Dolares']]
        result_df = result_df.sort_values(by='Soma Dolares', ascending=False).round(0)
        return result_df.head(11).round(0)
    else:
        # Calcular a soma dos dólares para cada país
        df_agrupado['Soma Dolares'] = df_agrupado[['Espumante ($)', 'Suco ($)', 'Vinho de Mesa ($)', 'Uva ($)']].sum(axis=1)

        # Calcular os percentuais de cada tipo de bebida em relação ao total de dólares gastos em bebidas para cada país
        df_agrupado['Percentual Espumantes Dolares'] = (df_agrupado['Espumante ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Suco Dolares'] = (df_agrupado['Suco ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Vinho de Mesa Dolares'] = (df_agrupado['Vinho de Mesa ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Uva Dolares'] = (df_agrupado['Uva ($)'] / df_agrupado['Soma Dolares']) * 100

        # Selecionar apenas as colunas necessárias
        result_df = df_agrupado[['País', 'Soma Dolares', 'Percentual Espumantes Dolares', 'Percentual Suco Dolares', 'Percentual Vinho de Mesa Dolares','Percentual Uva Dolares']]
        result_df = result_df.sort_values(by='Soma Dolares', ascending=False).round(0)
        print(result_df)
        return result_df.head(11).round(0)

def top_dez_paises_dolar_2019(df, filtro_uva_ativo):
    df_filtered = df.copy()
    filtro = df_filtered['Ano'] == '2019'
    # Agrupar por país e somar os valores
    df_agrupado = df[filtro].groupby('País').sum().reset_index()

    if filtro_uva_ativo:
        # Calcular a soma dos dólares para cada país
        df_agrupado['Soma Dolares'] = df_agrupado[['Espumante ($)', 'Suco ($)', 'Vinho de Mesa ($)']].sum(axis=1)

        # Calcular os percentuais de cada tipo de bebida em relação ao total de dólares gastos em bebidas para cada país
        df_agrupado['Percentual Espumantes Dolares'] = (df_agrupado['Espumante ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Suco Dolares'] = (df_agrupado['Suco ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Vinho de Mesa Dolares'] = (df_agrupado['Vinho de Mesa ($)'] / df_agrupado['Soma Dolares']) * 100

        # Selecionar apenas as colunas necessárias
        result_df = df_agrupado[['País', 'Soma Dolares', 'Percentual Espumantes Dolares', 'Percentual Suco Dolares', 'Percentual Vinho de Mesa Dolares']]
        result_df = result_df.sort_values(by='Soma Dolares', ascending=False).round(0)
        return result_df.head(11).round(0)
    else:
        # Calcular a soma dos dólares para cada país
        df_agrupado['Soma Dolares'] = df_agrupado[['Espumante ($)', 'Suco ($)', 'Vinho de Mesa ($)', 'Uva ($)']].sum(axis=1)

        # Calcular os percentuais de cada tipo de bebida em relação ao total de dólares gastos em bebidas para cada país
        df_agrupado['Percentual Espumantes Dolares'] = (df_agrupado['Espumante ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Suco Dolares'] = (df_agrupado['Suco ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Vinho de Mesa Dolares'] = (df_agrupado['Vinho de Mesa ($)'] / df_agrupado['Soma Dolares']) * 100
        df_agrupado['Percentual Uva Dolares'] = (df_agrupado['Uva ($)'] / df_agrupado['Soma Dolares']) * 100

        # Selecionar apenas as colunas necessárias
        result_df = df_agrupado[['País', 'Soma Dolares', 'Percentual Espumantes Dolares', 'Percentual Suco Dolares', 'Percentual Vinho de Mesa Dolares','Percentual Uva Dolares']]
        result_df = result_df.sort_values(by='Soma Dolares', ascending=False).round(0)
        return result_df.head(11).round(0)

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



        return pivot_df      

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


        return pivot_df




def main():
    df = st.session_state['dataframe'].copy()
    df = transform(df)

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

    with col1:
        st.markdown(textos_analise_internacional.grafico1, unsafe_allow_html=True)
        st.plotly_chart(mapa_dolar_continente(df))
    with col2:
        st.markdown(textos_analise_internacional.grafico2, unsafe_allow_html=True)
        st.plotly_chart(mapa_litro_por_dolar_continente(df))
    st.markdown(textos_analise_internacional.texto1, unsafe_allow_html=True)
    st.markdown('')
    st.markdown('')
 #   with col3:
 #       st.plotly_chart(mapa_dolar_continente(df))
        
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(textos_analise_internacional.tabela1, unsafe_allow_html=True)
        st.dataframe(top_dez_paises_dolar(table_pivot(df,filtro_uva_ativo), filtro_uva_ativo), hide_index=True)
    with col2:
        st.markdown(textos_analise_internacional.tabela2, unsafe_allow_html=True)
        st.dataframe(top_dez_paises_dolar_2019(table_pivot(df,filtro_uva_ativo), filtro_uva_ativo), hide_index=True)

    st.markdown(textos_analise_internacional.texto2, unsafe_allow_html=True)