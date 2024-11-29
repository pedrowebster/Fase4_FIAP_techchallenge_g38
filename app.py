import streamlit as st
import json 
from prophet.serialize import model_from_json
import pandas as pd
from prophet.plot import plot_plotly
import streamlit.components.v1 as components

def load_model():
    with open('modelo_json_prophet.json', 'r') as file_in:
        modelo = model_from_json(json.load(file_in))
        return modelo

modelo = load_model()

st.title("Tech Challenge Fase 4 - Pós-Tech FIAP")

membros = ["Pedro Henrique Webster Carneiro", "Renata Oliveira de Jesus", "Alessandra Renata Brunelli", "Guilherme Rodrigues Deizeppe", "Flavia Vieira da Silva"]

# Construção do texto formatado
texto = "**Pós Tech - 4DTAT (G38):**\n" + "\n".join(f"- {membro}" for membro in sorted(membros))

# Exibição no Streamlit
st.markdown(texto)


## Visualizacao no streamlit
aba1, aba2 = st.tabs(['Modelo Preditivo', 'Insights & Dashboard'])

with aba1:
    st.subheader('Previsão do Preço de Petróleo (US$) Utilizando a Biblioteca Prophet')

    st.caption('''Este projeto utiliza a biblioteca Prophet para prever o preço diário em US$ do barril de Petróleo. O modelo
            criado foi treinado com dados do ano de 2024 (até o dia 9 de Setembro) e possui as seguintes métricas de acurária (MSE: 11.92, RMSE: 3.45 e MAPE: 2.82 %).
            O usuário pode inserir o número de dias para os quais deseja a previsão, e o modelo gerará um gráfico
            interativo contendo as estimativas baseadas em dados históricos de preço.
            Além disso, uma tabela será exibida com os valores estimados para cada dia.''')

    st.subheader('Insira o número de dias para previsão:')

    dias = st.number_input('', min_value=1, max_value=30, value=1, step=1)

    if 'previsao_feita' not in st.session_state:
        st.session_state['previsao_feita'] = False
        st.session_state['dados_previsao'] = None

    if st.button('Prever'):
        st.session_state.previsao_feita = True
        futuro = modelo.make_future_dataframe(periods=dias, freq='B')
        previsao = modelo.predict(futuro)
        st.session_state['dados_previsao'] = previsao

    if st.session_state.previsao_feita:
        fig = plot_plotly(modelo, st.session_state['dados_previsao'])
        fig.update_layout({
            'plot_bgcolor': 'rgba(255, 255, 255, 1)',  # Define o fundo da área do gráfico como branco
            'paper_bgcolor': 'rgba(255, 255, 255, 1)', # Define o fundo externo ao gráfico como branco
            'title': {'text': "Previsão do Preço do Petróleo", 'font': {'color': 'black'}},
            'xaxis': {'title': 'Data', 'title_font': {'color': 'black'}, 'tickfont': {'color': 'black'}},
            'yaxis': {'title': 'US$', 'title_font': {'color': 'black'}, 'tickfont': {'color': 'black'}}
        })
        st.plotly_chart(fig)

        previsao = st.session_state['dados_previsao']
        tabela_previsao = previsao[['ds', 'yhat']].tail(dias)
        tabela_previsao.columns = ['Data (Dia/Mês/Ano)', 'Preço US$']
        tabela_previsao['Data (Dia/Mês/Ano)'] = tabela_previsao['Data (Dia/Mês/Ano)'].dt.strftime('%d-%m-%Y')
        tabela_previsao['Preço US$'] = tabela_previsao['Preço US$'].round(2)
        tabela_previsao.reset_index(drop = True, inplace = True)
        st.write('Tabela contendo a previsão do preço do petróleo para os próximos {} dias:'.format(dias))
        st.dataframe(tabela_previsao, height=300)

        csv = tabela_previsao.to_csv(index=False)
        st.download_button(label='Baixar tabela como .csv', data = csv, file_name = 'previsao_petroleo_{}dias.csv'.format(dias), mime = 'text/csv')

with aba2:
    # The Google Looker Studio embed URL
    looker_studio_url = "https://lookerstudio.google.com/embed/reporting/f28ef11e-27fe-4ceb-b1d1-5fc5060a4db8/page/0yVWE"
    components.iframe(looker_studio_url, width=1000, height=1280)