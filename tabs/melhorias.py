import streamlit as st

text = '''
Forças (Strengths):
Qualidade dos Vinhos: O Brasil tem ganhado reconhecimento internacional pela qualidade dos vinhos produzidos em diferentes regiões.

Diversidade de Variedades: A diversidade de uvas cultivadas no Brasil permite a produção de uma variedade de vinhos, atendendo a diferentes preferências de consumidores.

Crescimento do Setor: Ao longo dos anos, o setor de exportação de vinhos do Brasil tem demonstrado crescimento, indicando uma demanda crescente.

Clima Favorável: O clima brasileiro oferece condições favoráveis para o cultivo de uvas, contribuindo para a produção de vinhos de alta qualidade.

Fraquezas (Weaknesses):
Baixa Concorrência Internacional: Em comparação com tradicionais produtores de vinho, o Brasil ainda enfrenta desafios para competir no mercado internacional.

Desafios Logísticos: A infraestrutura de transporte e logística pode ser uma limitação para a exportação eficiente.

Desconhecimento no Mercado Internacional: A falta de reconhecimento global pode dificultar a penetração nos mercados internacionais.

Oportunidades (Opportunities):
Exploração de Mercados Emergentes: Identificar e explorar novos mercados emergentes pode proporcionar oportunidades de crescimento.

Parcerias Internacionais: Estabelecer parcerias com distribuidores e varejistas internacionais pode facilitar a entrada em novos mercados.

Marketing e Promoção: Investir em estratégias eficazes de marketing e promoção pode aumentar a visibilidade dos vinhos brasileiros no cenário internacional.

Ameaças (Threats):
Concorrência Global: A concorrência de países com tradição vinícola estabelecida pode representar uma ameaça à participação no mercado.

Flutuações Cambiais: As flutuações nas taxas de câmbio podem afetar a competitividade dos preços dos vinhos brasileiros.

Regulamentações e Tarifas: Barreiras comerciais, tarifas e regulamentações podem representar desafios ao comércio internacional.

'''

def main():
    st.markdown(
        """
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                width: 80%;
                margin: 20px auto;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .section {
                margin-bottom: 40px;
            }
            .strengths, .weaknesses, .opportunities, .threats {
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .strengths h3, .weaknesses h3, .opportunities h3, .threats h3 {
                color: #4CAF50;
            }
            .strengths ul, .weaknesses ul, .opportunities ul, .threats ul {
                list-style-type: square;
            }
            .strengths li, .weaknesses li, .opportunities li, .threats li {
                margin-bottom: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write("<h1>Análise SWOT</h1>", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("Forças (Strengths)", expanded=True):
                st.write(
                    """
                    <ul>
                        <li><strong>Qualidade dos Vinhos:</strong> O Brasil tem ganhado reconhecimento internacional pela qualidade dos vinhos produzidos em diferentes regiões.</li>
                        <li><strong>Diversidade de Variedades:</strong> A diversidade de uvas cultivadas no Brasil permite a produção de uma variedade de vinhos, atendendo a diferentes preferências de consumidores.</li>
                        <li><strong>Crescimento do Setor:</strong> Ao longo dos anos, o setor de exportação de vinhos do Brasil tem demonstrado crescimento, indicando uma demanda crescente.</li>
                        <li><strong>Clima Favorável:</strong> O clima brasileiro oferece condições favoráveis para o cultivo de uvas, contribuindo para a produção de vinhos de alta qualidade.</li>
                    </ul>
                    """
                , unsafe_allow_html=True)
        with col2:
            with st.expander("Fraquezas (Weaknesses)" , expanded=True):
                st.write(
                    """
                    <ul>
                        <li><strong>Baixa Concorrência Internacional:</strong> Em comparação com tradicionais produtores de vinho, o Brasil ainda enfrenta desafios para competir no mercado internacional.</li>
                        <li><strong>Desafios Logísticos:</strong> A infraestrutura de transporte e logística pode ser uma limitação para a exportação eficiente.</li>
                        <li><strong>Desconhecimento no Mercado Internacional:</strong> A falta de reconhecimento global pode dificultar a penetração nos mercados internacionais.</li>
                    </ul>
                    """
                , unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            with st.expander("Oportunidades (Opportunities)", expanded=True):
                st.write(
                    """
                    <ul>
                        <li><strong>Exploração de Mercados Emergentes:</strong> Identificar e explorar novos mercados emergentes pode proporcionar oportunidades de crescimento.</li>
                        <li><strong>Parcerias Internacionais:</strong> Estabelecer parcerias com distribuidores e varejistas internacionais pode facilitar a entrada em novos mercados.</li>
                        <li><strong>Marketing e Promoção:</strong> Investir em estratégias eficazes de marketing e promoção pode aumentar a visibilidade dos vinhos brasileiros no cenário internacional.</li>
                    </ul>
                    """
                , unsafe_allow_html=True)
        with col2:
            with st.expander("Ameaças (Threats)", expanded=True):
                st.write(
                    """
                    <ul>
                        <li><strong>Concorrência Global:</strong> A concorrência de países com tradição vinícola estabelecida pode representar uma ameaça à participação no mercado.</li>
                        <li><strong>Flutuações Cambiais:</strong> As flutuações nas taxas de câmbio podem afetar a competitividade dos preços dos vinhos brasileiros.</li>
                        <li><strong>Regulamentações e Tarifas:</strong> Barreiras comerciais, tarifas e regulamentações podem representar desafios ao comércio internacional.</li>
                    </ul>
                    """
                , unsafe_allow_html=True)