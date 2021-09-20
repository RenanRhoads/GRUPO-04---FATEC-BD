from PyQt5.QtCore import QRunnable
from covid import tracker
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from datetime import date, timedelta
from css import css
import os
import requests
import shutil
import gzip
import logging
import sys
import threading


# Este arquivo foi criado e modificado por Renan Moreira Pereira (Grupo 4 - FATEC 2021)

# TODO: Adicionar gráficos nas visualizações.
# TODO: Todos os Widgets devem ter a cor alterado ao selecionar o modo escuro.
# TODO: Novas variáveis para melhores visualizações de dados.
# TODO: Utilizar Matplotlib e Seaborn para utilzar os gráficos.


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


class InterfacePrincipal(QMainWindow):
    cidade_selected: str

    def __init__(self):
        super().__init__()

        self.setStyleSheet(css.blueish)  # Define para o tema escuro.

        self.DarkModeStatus = 0

        self.hello = "Seja bem-vindo ao Covid Tracker!"

        self.items = tracker.lista_cidades  # definindo variáveis acima.

        self.select_texto = "Digite o nome de sua cidade:"

        self.data = str(date.today().strftime("%d/%m/%Y"))

        self.data_less_1 = date.today() - timedelta(days=1)
        self.data_string = self.data_less_1.strftime("%y-%m-%d")

        self.data_1 = QtWidgets.QLabel(self.data, self)
        self.data_1.move(950, 525)

        self.atualizarButton = QtWidgets.QPushButton(self)
        self.atualizarButton.clicked.connect(self.atualizar_dados)
        self.atualizarButton.setGeometry(650, 525, 200, 25)
        self.atualizarButton.setText("Atualizar dados.")

        self.texto = QtWidgets.QLabel(self.hello, self)
        self.texto.setStyleSheet(css.default)
        self.texto.setGeometry(25, 5, 450, 20)

        """Loop criado para inserir as citadel no display inicial"""

        self.lista_header = QtWidgets.QLabel(self.select_texto, self)
        self.lista_header.setGeometry(800, 5, 175, 25)
        self.lista_header.setStyleSheet(css.blueish_text)

        self.lista = QtWidgets.QComboBox(self)
        self.i = 0
        self.j = len(tracker.lista_cidades)

        while self.i < self.j:  # Um loop simples que pega a lista de cidades e coloca num widget de texto.
            self.lista.addItem(tracker.lista_cidades[self.i])
            self.i += 1
        self.lista.setGeometry(800, 35, 165, 30)
        self.lista.setEditable(True)

        self.cidade = self.lista.currentText()

        self.valor_cidade = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].sum()
        """Filtro se altera com base na cidade que o usuário seleciona"""
        self.valor_dia = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].loc[tracker.df['data'] == self.data_string].sum()
        """Calcula a data atual - 1 para saber a quantidade de novas mortes """

        self.mortes = QtWidgets.QLabel("Número total de mortes: " + str(self.valor_cidade), self)
        self.mortes.setStyleSheet(css.blueish_label)
        self.mortes.setGeometry(25, 200, 250, 150)

        self.mortes_dia = QtWidgets.QLabel("Novas mortes: " + str(self.valor_dia), self)
        self.mortes_dia.setStyleSheet(css.blueish_label)
        self.mortes_dia.setGeometry(25, 300, 250, 150)

        """
        Botões com funções
        """
        self.lista.activated.connect(self.item_usuario)

    def item_usuario(self):
        self.cidade_selected = self.lista.currentText()

        self.valor_cidade_selected = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
            tracker.df['tipo'] == 'city'].sum()  # Realiza a filtragem de acordo com a cidade selecionada.

        self.mortes.setText("Número total de Mortes: " + str(int(self.valor_cidade_selected)))
        """Altera o valor dos números de mortes que podemos ver."""

    def atualizar_dados(self):
        formato = "%(asctime)s: %(message)s"
        logging.basicConfig(format=formato, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("Main    : Inicializando a thread para atualizar o arquivo.")
        x = threading.Thread(target=Updating.atualizar, args=(1,))
        x.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    widget = InterfacePrincipal()
    widget.setFixedSize(1024, 550)
    widget.show()
    app.exec()
