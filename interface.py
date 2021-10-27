from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtCore import QRunnable
from matplotlib import pyplot as plt
from covid import tracker
from PyQt5.QtWidgets import *
from datetime import date, timedelta
from css import css
import os
import requests
import shutil
import gzip
import logging
import sys
import random
import threading


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
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.figure = plt.figure()
        # transforma o gráfico em uma figure.
        self.canvas = FigureCanvas(self.figure)
        # abaixo, opção de zoom e salvar uma imagem do gráfico.
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        self.hello = "Seja bem-vindo ao Covid Tracker!"
        self.select_texto = "Digite o nome de sua cidade:"
        self.texto = QLabel(self.hello, self)

        self.data = str(date.today().strftime("%d/%m/%Y"))

        self.data_less_1 = date.today() - timedelta(days=1)
        self.data_string = self.data_less_1.strftime("%y-%m-%d")

        self.data_1 = QLabel(self.data, self)
        # self.data_1.move(950, 520)

        self.atualizarButton = QPushButton(self)
        # self.atualizarButton.clicked.connect(self.atualizar_dados)
        self.atualizarButton.setText("Atualizar dados.")

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

        self.lista_ano.setEditable(True)

        self.cidade = self.lista.currentText()
        self.ano = self.lista_ano.currentText()

        self.valor_cidade = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].loc[tracker.df['ano'] == self.ano].sum()

        """Filtro se altera com base na cidade que o usuário seleciona"""
        self.valor_dia = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].loc[tracker.df['data'] == self.data_string].sum()

        """Calcula a data atual - 1 para saber a quantidade de novas mortes """

        self.mortes = QLabel("   Número total de Mortes: " + str(self.valor_cidade), self)
        self.mortes_dia = QLabel("   Novas mortes: " + str(self.valor_dia), self)


        """
        Botões com funções
        """
        self.lista.activated.connect(self.item_usuario)

        layout = QGridLayout()
        layout.addWidget(self.texto)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addWidget(self.atualizarButton)
        layout.addWidget(self.grafButton)
        layout.addWidget(self.data_1)
        layout.addWidget(self.lista_header, 0, 1)
        layout.addWidget(self.lista, 1, 1)
        layout.addWidget(self.lista_ano, 1, 2)
        layout.addWidget(self.mortes_dia, 3, 1)
        layout.addWidget(self.mortes, 4, 1)
        self.setLayout(layout)

    def plot(self):
        """ gera um gráfico aleatório só para testes """
        data = [random.random() for i in range(10)]

        self.figure.clear()

        ax = self.figure.add_subplot(111)

        ax.plot(data, '*-')

        self.canvas.draw()

    def item_usuario(self):
        self.cidade_selected = self.lista.currentText()
        self.valor_cidade_selected = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
            tracker.df['tipo'] == 'city'].sum()  # Realiza a filtragem de acordo com a cidade selecionada.

        self.mortes.setText("   Número total de Mortes: " + str(int(self.valor_cidade_selected)))
        """Altera o valor dos números de mortes que podemos ver."""

    def atualizar_dados(self):
        formato = "%(asctime)s: %(message)s"
        logging.basicConfig(format=formato, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Main    : Inicializando a thread para atualizar o arquivo.")
        x = threading.Thread(target=Updating.atualizar, args=(1,))
        x.start()

    def showGraf(self):
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
