import pandas as pd
import tkinter as tk
import locale

NaN_Value = float("NaN")  # Retira os valores em erro

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

file = pd.read_csv('caso_full.csv')  # Executa a leitura do arquivo.csv - "file" é apenas o nome que dei a variável.

df = pd.DataFrame(data=file, columns=['city', 'state', 'new_deaths'])  # transforma o arquivo csv em um dataframe
df = df.rename(columns={"city": "Cidade", 'state': 'estado', 'new_deaths': 'mortes'})
df = df.loc[df['estado'] == 'SP']
df = df.append(df.sum(numeric_only=True).rename('Total'))  # Deve ficar próximo do final da manipulação dos dados.
df = df.fillna(value="")

total_mortes = df['mortes'].loc[df['estado'] == 'SP'].sum()  # Calula o total de mortes do estado de SP

print(total_mortes)

cidade_a = str(input("Digite o nome da cidade:"))  # Pega uma cidade, definida pelo usuario, e faz a soma das mortes da mesma.


total_city = df['mortes'].loc[df['Cidade'] == cidade_a].sum()  # Calcula o total de mortes da cidade citada pelo usuário

print(total_city)


def MainWindow():
    front = tk.Tk()  # inicia a interface gráfica.
    front.title = "Covid Tracker"  # Da um nome a janela.
    front.geometry('1060x450')  # Define o tamanho da interface.
    total = tk.Label(front, font=("Courier", 15), text="Total de Mortes: " + str(total_mortes))  # Cria uma caixa de texto
    total.pack()
    cidade = tk.Label(front, font=("Courier", 15), text="Mortes na cidade de " + cidade_a + ":" + str(total_city))
    cidade.pack()
    b = tk.Button(front, text="Ok")
    b.pack()
    front.mainloop()


MainWindow()
