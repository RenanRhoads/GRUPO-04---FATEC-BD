from covid import tracker
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import *

# Este arquivo foi criado e modificado por Renan Moreira Pereira (Grupo 4 - FATEC 2021)

# TODO: Adicionar gráficos nas visualizações.
# TODO: Todos os Widgets devem ter a cor alterado ao selecionar o modo escuro.
# TODO: Novas variáveis para melhores visualizações de dados.
# TODO: Utilizar Matplotlib e Seaborn para utilzar os gráficos.

class InterfacePrincipal(QMainWindow):
    cidade_selected: str

    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #336B87;")  # Define para o tema escuro.

        self.DarkModeStatus = 0
        self.hello = "Seja bem-vindo ao Covid Tracker!"
        self.items = tracker.lista_cidades  # definindo variáveis acima.
        self.select_texto = "Digite o nome de sua cidade:"

        self.dark = QtWidgets.QPushButton("Modo Escuro")

        self.texto = QtWidgets.QLabel(self.hello, self)
        self.texto.setStyleSheet("""
            color: #FFFFFF;
            font-family: Comic Sans MS;
            font-size: 18px;
            """)
        self.texto.setGeometry(25, 5, 450, 20)

        """Loop criado para inserir as citadel no display inicial"""

        self.lista_header = QtWidgets.QLabel(self.select_texto, self)
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
        self.lista.setEditable(True)

        self.cidade = self.lista.currentText()
        self.valor_cidade = tracker.df['mortes'].loc[tracker.df['cidade'] == self.cidade].loc[
            tracker.df['tipo'] == 'city'].sum()
        self.mortes = QtWidgets.QLabel("Número total de mortes: " + str(self.valor_cidade), self)
        self.mortes.setStyleSheet("""
            color: #FFFFFF;
            font-family: Comic Sans MS;
            font: bold 15px;
            background-color: #90AFC5;
            border-width: 2px;
            border-radius: 10px;
            font-size: 15px;
            """)
        self.mortes.setGeometry(25, 200, 250, 150)

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


if __name__ == "__main__":
    app = QApplication()
    app.setStyle('Fusion')
    widget = InterfacePrincipal()
    widget.resize(1024, 550)
    widget.show()
    app.exec()
