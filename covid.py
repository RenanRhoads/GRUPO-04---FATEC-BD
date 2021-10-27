import locale
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date, timedelta

# 21/09/2021 - Matheus Lourenço - Adicionado gráfico de top 10 cidades mortes por Covid.

locale.setlocale(locale.LC_ALL, 'pt_BR')  # Define a localidade de como o programa deve ser utilizado.


class tracker:
    arquivo = os.path.expanduser('~\Documents\caso_full.csv')  # Local na pasta documentos onde o arquivo estará

    if os.path.isfile(arquivo):
        print("Arquivo encontrado.")
        pass
    else:
        from update import atualizar
        print("Arquivo não encotrado, realizando o download...")
        atualizar()

        """Verifica se o arquivo csv existe, caso a condição seja falsa, irá realizar o download do arquivo."""

    file = pd.read_csv(arquivo)
    """Executa a leitura do arquivo.csv - "file" é apenas o nome que dei a variável."""

    df = pd.DataFrame(data=file,
                      columns=['city', 'date', 'state', 'last_available_deaths', 'place_type',
                               'new_deaths',
                               'ast_available_confirmed'])  # transforma o arquivo csv em um dataframe e seleciona as colunas

    df = df.rename(
        columns={"city": "cidade", 'state': 'estado',
                 'last_available_deaths': 'mortes confirmadas', 'place_type': 'tipo',
                 'new_deaths': 'mortes', 'date': 'data', 'ast_available_confirmed': 'novos casos'})
    """Renomeia as colunas"""

    df = df.loc[df['estado'] == 'SP'].loc[
        df['tipo'] == 'city']
    """Filtra apenas o estado de SP na coluna 'estado', e apenas o cálculo por tipo "state"""

    df = df.fillna(value="")
    """altera os valores de NaN para valor em branco."""

    df = df.drop_duplicates()  # retira valores duplicados.
    df['data'] = pd.to_datetime(df['data'])  # cria uma coluna de data
    df['ano'] = pd.DatetimeIndex(df['data']).year  # cria uma coluna de ano
    df['mes'] = pd.DatetimeIndex(df['data']).month  # cria uma coluna de mes
    df['mes_nome'] = df['data'].dt.strftime('%B')  # transforma o numero da coluna 'mes' para nome do mes
    df['mes/ano'] = df['mes_nome'].astype(str) + "-" + df['ano'].astype(str)  # concatena mes e ano

    '''Variáveis'''

    dia_1 = date.today() - timedelta(days=1)
    dia_1.strftime("%Y-%m-%d")

    total_mortes_sp = df['mortes'].loc[df['estado'] == 'SP'].loc[
        df['data'] == str(dia_1)].sum()  # Soma somente as mortes do estado de SP

    novos_casos = df['novos casos'].loc[df['estado'] == 'SP'].loc[df['data'] == str(dia_1)].sum()  # Soma os casos novos

    total_mortes_dia = df['mortes'].loc[df['data'] == '2020-09-18'].sum()

    lista_cidades = df['cidade'].loc[df['estado'] == 'SP'].loc[df['cidade'] != ''].drop_duplicates().sort_values() \
        .tolist()

    lista_ano = ['2020', '2021']

    """Transforma os valores em lista, e coloca em ordem alfabética."""

    total_mortes_cidade = df[['cidade', 'mortes']].groupby('cidade').sum().sort_values(by='mortes', ascending=False) \
        .iloc[:10]
    # Ordena as cidades de forma decrescente e mostra as 10 cidades com maior numero de morte
    # print(total_mortes_cidade)

    ####################################################################################################################

    print(lista_ano)
    """Solicita Input de cidade para o usuário."""
    user_select_city = input("Digite o nome da cidade: \n")
    city_sel = user_select_city
    user_select_year = int(input('Digite o Ano desejado: '))
    ano_sel = user_select_year
    cidade_sel = df[df.cidade == str(city_sel)]

    """Gráfico para as 10 cidades com mais mortes"""
    sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
    f, ax = plt.subplots(figsize=(6, 15))
    sns.set_color_codes("pastel")
    sns.barplot(x="mortes", y="cidade", data=df,
                label="Total", color="b", estimator=sum, order=total_mortes_cidade.index)

    """Gráfico por mês da cidade selecionada"""
    sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
    f2, ax2 = plt.subplots(figsize=(6, 15))
    sns.set_color_codes("pastel")
    sns.lineplot(x="mes_nome", y="mortes", data=cidade_sel,
                label="Total", color="b", estimator=sum)

