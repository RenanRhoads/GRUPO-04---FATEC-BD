from PySide6.QtCore import Qt
from covid import tracker
from PySide6 import QtWidgets, QtCore, QtGui  # Faz as importações necessárias.
from PySide6.QtWidgets import *

import pandas as pd


class info(QWidget):  # Uma classe para abrir uma janela após apertar um botão. Apenas testando.
    def __init__(self):
        super().__init__()

        # self.InfoHorizontal = QtWidgets.QHBoxLayout(self)  # Define o tipo de caixa da interface


class main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        """Varáveis"""

        self.dataframe = tracker.df


        """Cria a listagem das cidades."""
        self.lista = QtWidgets.QComboBox()  # Declaração da lista.
        self.items = tracker.lista_cidades  # definindo variáveis acima.

        self.botao = QtWidgets.QPushButton("Informações")

        self.texto = QtWidgets.QLabel(text="Informações da cidade de ")
        self.texto.setAlignment(Qt.AlignCenter)

        self.infoH = QtWidgets.QHBoxLayout(self)  # Cria o layout inicial
        self.infoH.addWidget(self.texto, 0)  # Adiciona o texto
        self.infoH.addWidget(self.botao, 1)  # Adiciona o botão
        self.infoH.setAlignment(Qt.AlignTop)

        self.frameVertical = QtWidgets.QVBoxLayout(self)

        """Loop"""
        self.i = 0
        self.j = len(tracker.lista_cidades)
        while self.i < self.j:  # Um loop simples que pega a lista de cidades e coloca num widget de texto.
            self.lista.addItem(tracker.lista_cidades[self.i])
            self.i += 1

        self.infoH.addWidget(self.lista, 1)

        self.lista.activated.connect(self.getCidade)  # Quando clicado em uma cidade, irá pegar o valor.

        """
        Botões com funções
        """
        self.botao.clicked.connect(self.openNewWindow)

    def getCidade(self):
        """Adquiri a cidade selecionada na ComboBox acima."""
        self.cidade = self.lista.currentText()  # Opção selecionada na lista.
        self.texto.setText("Informações da cidade de " + self.cidade)
        self.max_mortes_cidade = self.dataframe['mortes'].loc[self.dataframe["Cidade"] == self.cidade].loc[self.dataframe['estado'] == 'SP'].max()
        print(self.max_mortes_cidade)
        print(self.cidade)

    def valores(self):  # Função para abrir a janela quando apertar o botao.
        print(":D")

    def openNewWindow(self):
        self.a = info()
        self.a.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Breeze')

    widget = main()
    widget.resize(800, 600)
    widget.show()

    app.exec()
