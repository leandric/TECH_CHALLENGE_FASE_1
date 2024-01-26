import streamlit as st
import pandas as pd
from paginas import introducao, desempenho_historico

# Configuração para tornar a página widescreen
st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto"  # A barra lateral começa recolhida
)
st.session_state['dataframe'] = pd.read_csv('https://raw.githubusercontent.com/leandric/Exportacao-de-Vinho-e-Derivados/main/base_tratada/base_final_v7.csv')

st.header('Vinícolas Brasileiras: Desempenho e Estratégias (2004 - 2019)', divider=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs(['Introdução',
                                        'Desempenho Hístorico',
                                        'Análise de Mercado Internacional',
                                        'Ações de Melhoria',
                                        'Sobre'])

with tab1:
    introducao.main()

with tab2:
    desempenho_historico.main()

with tab3:
    pass

with tab4:
    pass

with tab5:
    pass