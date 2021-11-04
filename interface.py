import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import QRunnable
from matplotlib import pyplot as plt
from covid import tracker
from PyQt5.QtWidgets import *
from datetime import date, timedelta
from matplotlib.figure import Figure
import requests
import shutil
import gzip
import logging
import sys
import random
import threading
import seaborn as sns
import tkinter as tk

# código simples para verificar o tamanho da tela do usuário.
root = tk.Tk()

_x = root.winfo_screenwidth()
_y = root.winfo_screenheight()

print(_x)
print(_y)


class Updating(QRunnable):
    """Função para atualizar os dados do programa."""

    def __init__(self, n):
        super().__init__()

    def atualizar(self):
        logging.info(f"Trabalhando no processo")
        path = os.path.expanduser('~\Documents\caso_full.csv.gz')
        output = os.path.expanduser('~\Documents\caso_full.csv')
        print("Iniciando o download do arquivo.")
        url = 'https://data.brasil.io/dataset/covid19/caso_full.csv.gz'  # link para o arquivo fornecido pelo site Brasil.IO
        r = requests.get(url, allow_redirects=True)

        with open(path, 'wb') as f:
            f.write(r.content)
            logging.info("Main    : Inicializando a thread para atualizar o arquivo.")
            """Após o download do arquivo, salva na pasta documentos"""

        with gzip.open(path, 'rb') as f_in:
            with open(output, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            """Extrai o arquivo da fila .GZ na pasta Documentos do usuário"""
            logging.info("Main    : Download e extração finalizados.")


class Window(QDialog):
    ano_selected: str
    cidade_selected: str

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setFixedSize(_x, _y)
        self.figure = plt.figure()
        # transforma o gráfico em uma figure.
        self.canvas = FigureCanvas(self.figure)
        # abaixo, opção de zoom e salvar uma imagem do gráfico.
        self.toolbar = NavigationToolbar(self.canvas, self)

        # botão que ativa a função plot, apenas para testes
        self.button = QPushButton('Gráfico por Mês')
        self.button.clicked.connect(self.item_usuario)

        self.hello = "Seja bem-vindo ao Covid Tracker!"
        self.select_texto = "Digite o nome de sua cidade:"
        self.texto = QLabel(self.hello, self)

        self.data = str(date.today().strftime("%d/%m/%Y"))

        self.data_less_1 = date.today() - timedelta(days=1)
        self.data_string = self.data_less_1.strftime("%y-%m-%d")

        self.data_1 = QLabel(self.data, self)

        self.atualizarButton = QPushButton(self)
        self.atualizarButton.clicked.connect(self.atualizar_dados)
        self.atualizarButton.setText("Atualizar dados.")

        self.chartUpdate = QPushButton(self)
        self.chartUpdate.setText("Gerar gráfico por dia (apenas mês atual).")

        self.grafButton = QPushButton(self)
        self.grafButton.clicked.connect(self.showGraf)
        self.grafButton.setText("Top 10 cidades")

        self.lista_header = QLabel(self.select_texto, self)

        self.lista = QComboBox(self)
        self.i = 0
        self.j = len(tracker.lista_cidades)

        while self.i < self.j:  # Um loop simples que pega a lista de cidades e coloca num widget de texto.
            self.lista.addItem(tracker.lista_cidades[self.i])
            self.i += 1
        self.lista.setEditable(True)

        self.lista_ano = QComboBox(self)
        self.r = 0
        self.s = len(tracker.lista_ano)

        while self.r < self.s:
            self.lista_ano.addItem(tracker.lista_ano[self.r])
            self.r += 1

        self.lista_ano.setEditable(False)

        self.cidade = self.lista.currentText()
        self.ano = self.lista_ano.currentText()

        self.valor_cidade = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].loc[tracker.df['ano'] == int(self.ano)].sum()

        """Filtro se altera com base na cidade que o usuário seleciona"""
        self.valor_dia = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].loc[tracker.df['data'] == self.data_string].sum()

        """Calcula a data atual - 1 para saber a quantidade de novas mortes """

        self.valor_mortes_sp = tracker.df['mortes'].sum()

        """ Total de óbitos em SP"""

        self.confirmados = tracker.df['confirmados'].loc[tracker.df['estado'] == 'SP'].sum()

        """ Total de casos confirmados em SP"""

        self.mortes = QLabel("Número total de Mortes: " + str(self.valor_cidade), self)
        self.mortes_dia = QLabel("Novas mortes: " + str(self.valor_dia), self)
        self.mortes_sp = QLabel("Total de óbitos em SP: " + str(self.valor_mortes_sp), self)
        self.confirmados_sp = QLabel("Total de confirmados em SP: " + str(self.confirmados), self)

        """
        Botões com funções
        """
        self.lista.activated.connect(self.item_usuario)
        self.lista_ano.activated.connect(self.item_usuario)

        layout = QGridLayout()
        layout.addWidget(self.texto)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.atualizarButton)
        layout.addWidget(self.chartUpdate)
        layout.addWidget(self.grafButton)
        layout.addWidget(self.data_1)
        layout.addWidget(self.lista_header, 0, 1)
        layout.addWidget(self.lista, 1, 1)
        layout.addWidget(self.lista_ano, 1, 2)
        layout.addWidget(self.mortes_dia, 3, 1)
        layout.addWidget(self.mortes, 4, 1)
        layout.addWidget(self.mortes_sp, 5, 1)
        layout.addWidget(self.confirmados_sp, 6, 1)
        self.setLayout(layout)

    def item_usuario(self):
        
        self.cidade_selected = self.lista.currentText()
        print(self.cidade_selected)
        self.ano_selected = self.lista_ano.currentText()
        print(self.ano_selected)
        self.valor_cidade_selected = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
            tracker.df['tipo'] == 'city'].loc[tracker.df['ano'] == int(self.ano_selected)].sum()

        # Realiza a filtragem de acordo com a cidade selecionada.

        self.mortes.setText("Número total de Mortes: " + str(int(self.valor_cidade_selected)))
        """Altera o valor dos números de mortes que podemos ver."""

        plt.clf()  # vai limpar o gráfico anterior para que não gere um em cima do outro.

        user_select_city = self.cidade_selected
        city_sel = user_select_city
        user_select_year = self.ano_selected
        ano_sel = user_select_year
        cidade_sel = tracker.df[tracker.df.cidade == str(city_sel)].loc[tracker.df.ano == int(ano_sel)]

        # Gráfico por mês da cidade selecionada
        sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
        ax = self.figure.add_subplot(111)
        sns.set_color_codes("pastel")
        sns.barplot(x="mes_nome", y="mortes", data=cidade_sel,
                    color="b", ci=None, estimator=sum)
        # Configurando título e rótulos dos eixos.
        plt.title('Evolução de morte por mês', fontsize=14)
        plt.xlabel('Mês', fontsize=12)
        plt.ylabel('Mortes', fontsize=12)
        for container in ax.containers:
            ax.bar_label(container)
        ax.plot()

        self.canvas.draw()

    def atualizar_dados(self):
        formato = "%(asctime)s: %(message)s"
        logging.basicConfig(format=formato, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Main    : Inicializando a thread para atualizar o arquivo.")
        x = threading.Thread(target=Updating.atualizar, args=(1,))
        x.start()

    def showGraf(self):

        plt.clf()

        sns.set_theme(style="darkgrid")  # faz o gráfico aparecer.
        ax = self.figure.add_subplot(111)
        ax.clear()
        sns.set_color_codes("pastel")
        sns.barplot(x="mortes", y="cidade", data=tracker.df,
                    label="Total", color="b", estimator=sum, ci=None, order=tracker.total_mortes_cidade.index)

        # Configurando título e rótulos dos eixos.
        plt.title('Total de mortes', fontsize=14)
        plt.xlabel('Mortes', fontsize=12)
        plt.ylabel('Cidades', fontsize=12)
        for container in ax.containers:
            ax.bar_label(container)
        ax.plot()

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.setWindowTitle('CovidTracker')
    main.show()

    sys.exit(app.exec_())
