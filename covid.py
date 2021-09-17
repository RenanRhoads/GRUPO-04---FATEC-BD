import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class tracker:
    """Tratamento de Dados"""

    file = pd.read_csv('caso_full.csv')  # Executa a leitura do arquivo.csv - "file" é apenas o nome que dei a variável.

    df = pd.DataFrame(data=file,
                      columns=['city', 'date', 'state', 'last_available_deaths', 'place_type',
                               'new_deaths'])  # transforma o arquivo csv em um dataframe e seleciona as colunas
    # necessárias
    df = df.rename(
        columns={"city": "cidade", 'state': 'estado',
                 'last_available_deaths': 'mortes confirmadas', 'place_type': 'tipo',
                 'new_deaths': 'mortes', 'date': 'data'})  # renomeia as colunas.

    df = df.loc[df['estado'] == 'SP'].loc[
        df['tipo'] == 'city']  # Filtra apenas o estado de SP na coluna 'estado', e apenas o cálculo por tipo "state"

    # df = df.append(df.sum(numeric_only=True).rename('Total'))  # Adicina um linha 'total' no fim da tabela.

    df = df.fillna(value="")  # altera os valores de NaN para valor em branco.

    df = df.drop_duplicates()  # retira valores duplicados.
    df['data'] = pd.to_datetime(df['data'])
    df['ano'] = pd.DatetimeIndex(df['data']).year

    '''Variáveis'''

    df_by_cidade = df.loc[df['cidade'] != ''].groupby(by=['cidade'])

    total_mortes = df['mortes'].loc[df['estado'] == 'SP'].sum()  # Soma somente as mortes do estado de SP

    lista_cidades = df['cidade'].loc[df['estado'] == 'SP'].loc[df['cidade'] != ''].drop_duplicates().sort_values() \
        .tolist()  # Transforma os valores em lista, e coloca em ordem alfabética.

    mortes_media = df['mortes'].loc[df['estado'] == 'SP'].loc[df['mortes'] > 0].mean()

    mortes_max = df['mortes'].loc[df['estado'] == 'SP'].loc[df['tipo'] == 'city'].sum()
    mortes_max_array = df['mortes'].loc[df['estado'] == 'SP'].loc[df['tipo'] == 'city']

    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x="ano", y="mortes", data=df)
    plt.show()
