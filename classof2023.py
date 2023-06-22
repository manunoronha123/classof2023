# classof2023
#Importar as bibliotecas necessárias
import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

#Definir o link para fazer o scraping, usar o comando requests para obter o conteúdo do link, criar a variável "soup" para analizar o conteúdo usando o BeautifulSoup
url = "https://www.earj.com.br/university-acceptances/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

#Filtrar o conteúdo do site para identificar elementos que contém a tag 'h2', e o texto 'Class of 2023 Acceptances'
text = 'Class of 2023 Acceptances'
for i in soup.find_all('h2'):
    if(i.string == text):
        pointer = i
        break

#Criar um dicionário para armazenar os dados nas categorias país e universidade 
dict_universidades = {'País':[], 'Universidade':[]}
# encontra os países apenas da seção depois de 2023
for paises in pointer.find_all_next("a", {'role': 'button'}):
    tabela = paises['href'][1:]
    pais = paises.text
    div = paises.find_next('div', {'id': tabela})
    for universidade in div.find_all("li"):
        dict_universidades['País'].append(pais)
        dict_universidades['Universidade'].append(universidade.text)
#Organizar em um data frame do pandas, que organiza os dados em estrutura de tabela
df = pd.DataFrame.from_dict(dict_universidades)

if df is not None:
    if "País" in df.columns:  # Verifica se a coluna "País" existe no DataFrame
        regiões_especificas = ['United States', 'United Kingdom', 'Europe', 'Canada', 'Brazil']
        região_selecionada = st.selectbox("Pick a region", regiões_especificas)
        df_filtrado = df[df['País'] == região_selecionada]
        if not df_filtrado.empty:
            st.write("Dados Filtrados")
            st.dataframe(df_filtrado)
            st.write("Chart")
            region_counts = df['País'].value_counts()
            region_counts.plot.pie(autopct='%1.1f%%', startangle=90) #comando para criar gráfico pizza no streamlit 
            plt.axis('equal')  # Para manter o aspecto de um círculo
            st.pyplot()
        else:
            st.write("Dado não encontrado")
    else:
        st.write("Coluna 'País' não encontrada no Data Frame")
