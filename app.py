import streamlit as st
import pandas as pd
from tabs import sobre, introducao, desempenho_hist, analise_internacional, melhorias

# Configurações do Streamlit
st.set_page_config(
    layout='wide',
    page_title='Vinicolas Brasileiras'
)

def transform(df):
    filtro = df['Continente'] != 'Outros'
    df_filtered = df[filtro].copy()
    return df_filtered

# Armazena o dataframe no cash do navegador
st.session_state['dataframe'] = transform(pd.read_csv('https://raw.githubusercontent.com/leandric/Exportacao-de-Vinho-e-Derivados/main/base_tratada/base_final_v7.csv'))

# Conteudo
st.header('Vinícolas Brasileiras: Analise de Mercado Internacional (2004 - 2019)', divider=True)
tab1, tab2, tab3, tab4 = st.tabs(['Introdução',
                                        'Desempenho Hístorico',
                                        'Análise de Mercado Internacional',
                                        'Análise SWOT'
                                        ])
with tab1:
    introducao.main()

with tab2:
    desempenho_hist.main()

with tab3:
    analise_internacional.main()

with tab4:
    melhorias.main()

#with tab5:
#    sobre.main()
