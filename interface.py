import PySide6.QtCharts
import sys
from covid import tracker
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import *
PySide6.QtCore.QRect

class test(QtWidgets.QWidget):  # Uma classe para abrir uma janela após apertar um botão. Apenas testando.
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()  # Define o tipo de caixa da interface
        self.label = QtWidgets.QLabel("Outra Janela")  # Cria uma label
        self.layout.addWidget(self.label)  # Adiciona um widget no layout, definido antes


class main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        """Variáveis"""
        self.hello = "Olá"
        self.items = tracker.lista_cidades  # definindo variáveis acima.

        """Widgets"""
        self.lista = QtWidgets.QComboBox()
        self.botao = QtWidgets.QPushButton("Clique aqui!")
        self.texto = QtWidgets.QLabel(text=self.hello, alignment=QtCore.Qt.AlignCenter)
        self.caixaLista = QtWidgets.QListWidget(self)

        """Layouts"""
        self.layout = QtWidgets.QGridLayout(self)  # Cria o layout inicial
        self.layout.addWidget(self.texto, 0, 0)  # Adiciona o texto
        self.layout.addWidget(self.botao, 0, 1)  # Adiciona o botão
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addWidget(self.lista, 0, 2)  # Adiciona o list

        self.layout_lista = QtWidgets.QVBoxLayout(self)

        """Loop criado para inserir as citadel no display inicial"""

        self.i = 0
        self.j = len(tracker.lista_cidades)

        print(type(self.j))

        while self.i < self.j:  # Um loop simples que pega a lista de cidades e coloca num widget de texto.
            self.lista.addItem(tracker.lista_cidades[self.i])
            self.i += 1

        """
        Botões com funções
        """
        self.botao.clicked.connect(self.magic)
        self.lista.activated.connect(self.item_usuario)

    def item_usuario(self):
        self.cidade = self.lista.currentText()
        print(self.cidade)

    def magic(self):  # Função para abrir a janela quando apertar o botao.
        self.a = test()
        self.a.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = main()
    widget.resize(1024, 720)
    widget.show()

    app.exec()