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

aba1, aba2, aba3, aba4 = st.tabs(['Introdução', 'Dashboard & Insights', 'Modelo Preditivo', 'Código do Modelo'])

with aba1:

    st.subheader('Introdução Tech Challenge FIAP - Data Analytics - Fase 4')

    st.write('''
    Este trabalho tem como objetivo a análise e previsão do preço do petróleo utilizando ferramentas e técnicas de análise de dados e modelagem preditiva. A proposta foi desenvolvida como parte do Tech Challenge FIAP - Data Analytics, Fase 4, e aborda a variação do preço do petróleo Brent ao longo do tempo, fornecendo insights valiosos e projeções futuras.

    Para atender a demanda do cliente, criamos uma solução que combina análise visual e previsão de dados. O trabalho foi dividido em três etapas principais:
    
    1. **Análise exploratória e visualização dos dados**: Desenvolvemos um dashboard interativo no Looker Studio, que apresenta informações sobre o comportamento histórico dos preços do petróleo. O dashboard inclui métricas estatísticas, gráficos de variação de preços e filtros para análise de dados por diferentes períodos e eventos históricos que impactaram no preço do petróleo.
    
    2. **Modelo preditivo com a biblioteca Prophet**: Utilizamos a biblioteca Prophet para prever os preços futuros do petróleo, baseando-nos em dados históricos. O modelo gerado permite aos usuários inserir um número de dias para prever o preço do petróleo, gerando estimativas com base em dados passados e exibindo gráficos interativos e tabelas com os resultados da previsão.
    
    3. **Código do modelo**: O código em Python que implementa o modelo preditivo com Prophet está disponível, permitindo a reprodução dos resultados e a realização de ajustes personalizados no modelo.

    A seguir, você encontrará o dashboard com os insights sobre a variação dos preços do petróleo, a previsão do modelo e o código utilizado para a construção do modelo preditivo. Esperamos que esta análise seja útil para compreender melhor as flutuações nos preços do petróleo e suas tendências futuras.
    ''')


with aba2:
    
    st.subheader('Dashboard Looker com Insights Sobre Variação do Preço do Petróleo')

    st.write('''Para atender ao pedido do cliente, optamos por desenvolver o dashboard no Looker Studio, uma ferramenta online que transforma dados em dashboards interativos e personalizáveis.
               
O primeiro elemento incluído no dashboard foram as métricas estatísticas, que oferecem uma visão geral do comportamento dos preços do petróleo, destacando o preço máximo, mínimo e médio históricos.
               
Em seguida, adicionamos gráficos sob duas perspectivas:
               
- A primeira (ver primeiro gráfico de linhas) mostra um registro diário dos preços do petróleo Brent, permitindo a visualização das variações ao longo do tempo, com dados exclusivamente na granularidade diária.
               
- A segunda (ver segundo gráfico de linhas) também exibe registros diários dos preços do Brent, mas segmenta-os por eventos históricos relevantes, como a pandemia de COVID-19. Neste gráfico, habilitamos a funcionalidade "Detalhar", que possibilita ao usuário explorar dados em diferentes níveis de granularidade ao clicar na seta acima do gráfico.
               
Por fim, adicionamos filtros que permitem aos usuários pesquisar não apenas por períodos específicos, mas também por eventos históricos que impactaram significativamente os preços do petróleo.

Em resumo, nosso objetivo foi desenvolver um dashboard em uma plataforma intuitiva, proporcionando aos clientes uma experiência simples e direta, com opções de filtros úteis e um design visualmente agradável.
''')
    
    # The Google Looker Studio embed URL
    looker_studio_url = "https://lookerstudio.google.com/embed/reporting/f28ef11e-27fe-4ceb-b1d1-5fc5060a4db8/page/0yVWE"
    components.iframe(looker_studio_url, width=1000, height=1280)

with aba3:
    st.subheader('Previsão do Preço de Petróleo (US$) Utilizando a Biblioteca Prophet')

    st.write('''Este projeto utiliza a biblioteca Prophet para prever o preço diário em US$ do barril de Petróleo. O modelo
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



with aba4:

    st.write('''Abaixo segue o código em python da construção do modelo utilizando a biblioteca Prophet. Para ter acesso ao código na integra, acessar o jupyter notebook (TechChallenge_prophet_v2.ipynb) disponibilizado.''')

    code = '''
    import pandas as pd
    import plotly.express as px
    import numpy as np
    from prophet import Prophet
    import matplotlib.pyplot as plt
    from sklearn.metrics import mean_squared_error, mean_absolute_error

    url = "https://raw.githubusercontent.com/pedrowebster/Prophet_alura/refs/heads/main/df.csv"

    df = pd.read_csv(url)
    df = df.drop(df.columns[0], axis=1)
    df.columns = ["Data", "Preco"]
    df["Preco"] = pd.to_numeric(df["Preco"], errors="coerce").astype("Int64")
    df["Preco"] = df["Preco"]/100
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y", errors="coerce")
    df = df.sort_index(ascending=False).reset_index()
    df.drop(df.columns[0], axis = 1, inplace=True)

    df_prophet = pd.DataFrame()
    df_prophet['ds'] = df['Data']
    df_prophet['y'] = df['Preco']

    data_de_corte = df_prophet['ds'].max()
    data_de_corte = data_de_corte - pd.DateOffset(years=1)

    df_prophet_2 = df_prophet[df_prophet['ds'] >= data_de_corte]
    df_prophet_2.reset_index(inplace=True)
    fig = px.line(df_prophet_2, x='ds', y='y')

    tamanho_treino = int(len(df_prophet_2)* 0.8)
    tamanho_teste = int(len(df_prophet_2) * 0.2)

    df_treino = pd.DataFrame()
    df_treino['ds'] = df_prophet_2['ds'][:tamanho_treino]
    df_treino['y'] = df_prophet_2['y'][:tamanho_treino]

    df_teste = pd.DataFrame()
    df_teste['ds'] = df_prophet_2['ds'][tamanho_treino:]
    df_teste['y'] = df_prophet_2['y'][tamanho_treino:]

    # CRIANDO O MODELO
    # Definir um seed
    np.random.seed(4587)

    # Instanciar o modelo Prophet
    modelo = Prophet(yearly_seasonality=True)

    # Treinar o modelo
    modelo.fit(df_treino)

    # Criar um dataframe para previsões futuras
    futuro = modelo.make_future_dataframe(periods = tamanho_teste, freq='B')
    previsao = modelo.predict(futuro)

    # AVALIANDO MÉTRICAS DE ACURÁRIA
    mse = mean_squared_error(df_comparacao['y'], df_comparacao['yhat']).round(2)
    rmse = np.sqrt(mse).round(2)
    mape = mean_absolute_error(df_comparacao['y'], df_comparacao['yhat']).round(2)'''
    st.code(code, language="python")
    st.caption('''Também foi construído um modelo secundário, presente no jupyter notebook TechChallengeXGBoost.ipynb, no entanto, este não foi escolhido pois apresentou métricas de acurácia menores.''')
