import locale
import pandas as pd
import seaborn as sns
import os
from datetime import date, timedelta

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
                               'new_deaths'])  # transforma o arquivo csv em um dataframe e seleciona as colunas

    df = df.rename(
        columns={"city": "cidade", 'state': 'estado',
                 'last_available_deaths': 'mortes confirmadas', 'place_type': 'tipo',
                 'new_deaths': 'mortes', 'date': 'data'})
    """Renomeia as colunas"""

    df = df.loc[df['estado'] == 'SP'].loc[
        df['tipo'] == 'city']
    """Filtra apenas o estado de SP na coluna 'estado', e apenas o cálculo por tipo "state"""

    df = df.fillna(value="")
    """altera os valores de NaN para valor em branco."""

    df = df.drop_duplicates()  # retira valores duplicados.
    df['data'] = pd.to_datetime(df['data'])
    df['ano'] = pd.DatetimeIndex(df['data']).year
    df['mes'] = pd.DatetimeIndex(df['data']).month
    df['mes_nome'] = df['data'].dt.strftime('%B')  # transforma o numero da coluna 'mes' para nome do mes
    df['mes/ano'] = df['mes_nome'].astype(str) + "-" + df['ano'].astype(str)

    '''Variáveis'''

    df_by_cidade = df.loc[df['cidade'] != ''].groupby(by=['cidade'])

    dia_1 = date.today() - timedelta(days=1)
    dia_1.strftime("%Y-%m-%d")

    total_mortes = df['mortes'].loc[df['estado'] == 'SP'].sum()  # Soma somente as mortes do estado de SP
    total_mortes_dia = df['mortes'].loc[df['data'] == str(dia_1)].sum()

    lista_cidades = df['cidade'].loc[df['estado'] == 'SP'].loc[df['cidade'] != ''].drop_duplicates().sort_values() \
        .tolist()
    """Transforma os valores em lista, e coloca em ordem alfabética."""

    mortes_media = df['mortes'].loc[df['estado'] == 'SP'].loc[df['mortes'] > 0].mean()
    mortes_max = df['mortes'].loc[df['estado'] == 'SP'].loc[df['tipo'] == 'city'].sum()
    mortes_max_array = df['mortes'].loc[df['estado'] == 'SP'].loc[df['tipo'] == 'city']

    cidade_sel = df[df.cidade == 'São Paulo']
    mortes_data = df[df.data == str(dia_1)].sum()

    print(dia_1)
    print(total_mortes)
    print(total_mortes_dia)

    sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
