import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from covid import tracker
from PySide6 import QtCore, QtWidgets, QtGui        # Faz as importações necessárias.


class test(QtWidgets.QWidget):      # Uma classe para abrir uma janela após apertar um botão. Apenas testando.
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()     # Define o tipo de caixa da interface
        self.label = QtWidgets.QLabel("Outra Janela")    # Cria uma label
        self.layout.addWidget(self.label)       # Adiciona um widget no layout, definido antes


class main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        """Varáveis"""
        self.hello = "Olá"
        self.items = tracker.lista_cidades      # definindo variáveis acima.

        self.botao = QtWidgets.QPushButton("Clique aqui!")
        self.texto = QtWidgets.QLabel(text=self.hello, alignment=QtCore.Qt.AlignCenter)
        self.layout = QtWidgets.QVBoxLayout(self)  # Cria o layout inicial
        self.layout.addWidget(self.texto)  # Adiciona o texto
        self.layout.addWidget(self.botao)  # Adiciona o botão

        self.lista = QtWidgets.QListWidget()

        self.i = 0
        self.j = len(tracker.lista_cidades)

        while self.i < self.j:      # Um loop simples que pega a lista de cidades e coloca num widget de texto.
            self.lista.addItem(tracker.lista_cidades[self.i])
            self.i += 1

        self.layout.addWidget(self.lista)

        """
        Botões com funções
        """
        self.botao.clicked.connect(self.magic)


    @QtCore.Slot()

    def magic(self):        # Função para abrir a janela quando apertar o botao.
        a = test()
        a.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = main()
    widget.resize(800, 600)
    widget.show()

    app.exec()