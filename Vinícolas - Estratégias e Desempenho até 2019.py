import streamlit as st
import pandas as pd

# Configuração para tornar a página widescreen
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto"  # A barra lateral começa recolhida
)
st.session_state['dataframe'] = pd.read_csv('https://raw.githubusercontent.com/leandric/Exportacao-de-Vinho-e-Derivados/main/base_tratada/base_final_v7.csv')

st.header('Vinícolas Brasileiras: Estratégias e Desempenho (2004 - 2019)', divider=True)
