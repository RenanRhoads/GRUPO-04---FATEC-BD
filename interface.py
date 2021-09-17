import qdarkstyle
import os
from PySide6.QtCore import QTimer, QRect
from qdarkstyle import DarkPalette, LightPalette
from covid import tracker
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import *


# Este arquivo foi criado e modificado por Renan Moreira Pereira (Grupo 4 - FATEC 2021)

# TODO: Adicionar gráficos nas visualizações.
# TODO: Todos os Widgets devem ter a cor alterado ao selecionar o modo escuro.
# TODO: Novas variáveis para melhores visualizações de dados.
# TODO: Utilizar Matplotlib e Seaborn para utilzar os gráficos.

class InterfacePrincipal(QtWidgets.QWidget):
    cidade_selected: str

    def __init__(self):
        super().__init__()

        app.setStyleSheet(qdarkstyle.load_stylesheet(palette=DarkPalette))  # Define para o tema escuro.

        self.DarkModeStatus = 0
        self.hello = "Seja bem-vindo ao Covid Tracker!"
        self.items = tracker.lista_cidades  # definindo variáveis acima.
        self.select_texto = "Selecione sua cidade:"

        self.dark = QtWidgets.QPushButton("Modo Escuro")

        self.texto = QLabel(self.hello, self)
        self.texto.setStyleSheet("""
            color: #FFFFFF;
            font-family: Comic Sans MS;
            font-size: 18px;
            """)

        """Loop criado para inserir as citadel no display inicial"""

        self.lista_header = QLabel(self.select_texto, self)
        self.lista_header.move(800, 5)
        self.lista_header.setStyleSheet("""
        color: #FFFFFF;
        font-family: Comic Sans MS;
        font-seize: 15px;
        """)

        self.lista = QtWidgets.QComboBox(self)
        self.i = 0
        self.j = len(tracker.lista_cidades)

        while self.i < self.j:  # Um loop simples que pega a lista de cidades e coloca num widget de texto.
            self.lista.addItem(tracker.lista_cidades[self.i])
            self.i += 1
        self.lista.setGeometry(800, 35, 165, 30)

        self.cidade = self.lista.currentText()
        self.valor_cidade = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].sum()
        self.mortes = QLabel("Número total de mortes: " + str(self.valor_cidade), self)
        self.mortes.setStyleSheet("""
            color: #FFFFFF;
            font-family: Comic Sans MS;
            font-size: 15px;
            """)
        self.mortes.move(25, 200)

        """
        Botões com funções
        """
        self.dark.clicked.connect(self.darkmode)
        self.lista.activated.connect(self.item_usuario)

    def item_usuario(self):
        self.cidade_selected = self.lista.currentText()
        self.valor_cidade_selected = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade_selected].loc[
            tracker.df['tipo'] == 'city'].sum()  # Realiza a filtragem de acordo com a cidade selecionada.

        self.mortes.setText("Número total de Mortes: " + str(int(self.valor_cidade_selected)))
        """Altera o valor dos números de mortes que podemos ver."""

    """Função para alterar a cor do background"""

    def darkmode(self):  # Função para alterar o tema para escuro.

        """ Define o aplicativo em modo 'Escuro' """
        if self.DarkModeStatus == 0:
            app.setStyleSheet(qdarkstyle.load_stylesheet(palette=DarkPalette))  # Define para o tema escuro.

            self.texto.setStyleSheet("""
            color: #FFFFFF;
            font-family: Comic Sans MS;
            font-size: 18px;
            """)

            self.mortes.setStyleSheet("""
            color: #FFFFFF;
            font-family: Comic Sans MS;
            font-size: 18px;
            """)

            self.DarkModeStatus += 1
        else:
            app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette))  # Define para o tema claro.
            self.texto.setStyleSheet("""
                        color: #090002;
                        font-family: Comic Sans MS;
                        font-size: 18px;
                        """)
            self.mortes.setStyleSheet("""
                        color: #090002;
                        font-family: Comic Sans MS;
                        font-size: 18px;
                        """)

            self.DarkModeStatus -= 1
            """ Define o aplicativo em modo 'Claro' """


if __name__ == "__main__":
    app = QApplication()
    app.setStyleSheet(qdarkstyle.load_stylesheet(palette=LightPalette))
    widget = InterfacePrincipal()
    widget.resize(1024, 550)
    widget.show()

    app.exec()
