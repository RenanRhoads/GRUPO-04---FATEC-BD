import pandas as pd


class tracker:
    file = pd.read_csv('caso_full.csv')  # Executa a leitura do arquivo.csv - "file" é apenas o nome que dei a variável.

    df = pd.DataFrame(data=file,
                      columns=['city', 'state', 'new_deaths'])  # transforma o arquivo csv em um dataframe
    df = df.rename(
        columns={"city": "Cidade", 'state': 'estado', 'new_deaths': 'mortes'})  # Seleciona as colunas que utilizaremos.
    df = df.loc[df['estado'] == 'SP']  # Filtra apenas o estado de SP na coluna 'estado'
    df = df.append(df.sum(numeric_only=True).rename('Total'))  # Adicina um linha 'total' no fim da tabela.
    df = df.fillna(value="")  # altera os valores de NaN para valor em branco.
    df = df.drop_duplicates()  # teste, excluir

    lista_cidades = df['Cidade'].loc[df['estado'] == 'SP'].drop_duplicates().tolist()  # Transforma os valores em lista.
    total_mortes = df['mortes'].loc[df['estado'] == 'SP'].sum()  # Soma somente as mortes do estado de SP

    mortes_min = df['mortes'].loc[(df['estado'] == 'SP') & (df['mortes'] > 0)].min()
    mortes_max = df['mortes'].loc[df['estado'] == 'SP'].max()
    """cidade = input("Digite o nome da cidade:")
    total_city = df['mortes'].loc[df['Cidade'] == cidade].sum()"""


def counter():
    i = 0
    j = len(tracker.lista_cidades)

    while i < j:
        print(tracker.lista_cidades[i])
        i += 1